import unittest

from parameterized import parameterized
from utils.channel_access import ChannelAccess
from utils.ioc_launcher import get_default_ioc_dir
from utils.test_modes import TestModes
from utils.testing import get_running_lewis_and_ioc

DEVICE_PREFIX = "PS300_01"


IOCS = [
    {
        "name": DEVICE_PREFIX,
        "directory": get_default_ioc_dir("PS300"),
        "macros": {"MODEL": "350_pos"},
        "emulator": "Ps300",
    },
]

# Only test in devsim due to PINI records.
TEST_MODES = [TestModes.DEVSIM]


class Ps300Tests(unittest.TestCase):
    """
    Tests for the Ps300 IOC.
    """

    def setUp(self):
        self._lewis, self._ioc = get_running_lewis_and_ioc("Ps300", DEVICE_PREFIX)
        self.ca = ChannelAccess(device_prefix=DEVICE_PREFIX)
        self._lewis.backdoor_run_function_on_device("set_current", [0])
        self.ca.set_pv_value("HV:SP", "Turn Off")
        self.ca.set_pv_value("TripClear", 1)

    @parameterized.expand(
        [
            ("_0_case", "Turn Off", 0, 0, 0, "Off", "No limit", "Not tripped", "Not tripped"),
            ("_hv_only_case", "Turn On", 0, 0, 128, "On", "No limit", "Not tripped", "Not tripped"),
            (
                "_Limit_only_case",
                "Turn Off",
                0,
                0.002,
                8,
                "Off",
                "Limited",
                "Not tripped",
                "Not tripped",
            ),
            (
                "_Current_Trip_case",
                "Turn Off",
                0,
                0.006,
                12,
                "Off",
                "Limited",
                "Tripped",
                "Not tripped",
            ),
            (
                "_Voltage_Trip_case",
                "Turn Off",
                101,
                0,
                2,
                "Off",
                "No limit",
                "Not tripped",
                "Tripped",
            ),
            (
                "_Voltage_Trip_and_limit_off_case",
                "Turn Off",
                101,
                0.002,
                10,
                "Off",
                "Limited",
                "Not tripped",
                "Tripped",
            ),
            (
                "_Voltage_Trip_and_limit_on_case",
                "Turn On",
                101,
                0.002,
                138,
                "On",
                "Limited",
                "Not tripped",
                "Tripped",
            ),
            (
                "_off_all_Trip_case",
                "Turn Off",
                101,
                0.006,
                14,
                "Off",
                "Limited",
                "Tripped",
                "Tripped",
            ),
            (
                "_on_all_Trip_case",
                "Turn On",
                101,
                0.006,
                142,
                "On",
                "Limited",
                "Tripped",
                "Tripped",
            ),
        ]
    )
    def test_WHEN_status_set_THEN_properly_split(
        self,
        _,
        hv_on,
        voltage,
        current,
        status,
        hv_status,
        current_limit,
        current_trip,
        voltage_limit,
    ):
        self.ca.set_pv_value("HV:SP", hv_on)
        self.ca.set_pv_value("VOLTAGE:SP", voltage)
        self._lewis.backdoor_run_function_on_device("set_current", [current])
        self.ca.assert_that_pv_is("STATUS", status)
        self.ca.assert_that_pv_is("HV:STATUS", hv_status)
        self.ca.assert_that_pv_is("CURRENT:LIMIT:STATUS", current_limit)
        self.ca.assert_that_pv_is("CURRENT:TRIP:STATUS", current_trip)
        self.ca.assert_that_pv_is("VOLTAGE:TRIP:STATUS", voltage_limit)
