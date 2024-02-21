from lewis.adapters.stream import StreamInterface, Cmd
from lewis.utils.command_builder import CmdBuilder
from lewis.core.logging import has_log
from lewis.utils.replies import conditional_reply


@has_log
class Ps300StreamInterface(StreamInterface):
    
    in_terminator = "\r\n"
    out_terminator = "\r\n"

    def __init__(self):
        super(Ps300StreamInterface, self).__init__()
        # Commands that we expect via serial during normal operation
        self.commands = {
            CmdBuilder(self.get_status_register).escape("*ESR?").eos().build(),
            CmdBuilder(self.clear_trip).escape("TCLR").eos().build(),
            CmdBuilder(self.enable_highvoltage).escape("HVON").eos().build(),
            CmdBuilder(self.disable_highvoltage).escape("HVOF").eos().build(),
            CmdBuilder(self.set_voltage).escape("VSET ").float().eos().build(),
            CmdBuilder(self.set_voltage_limit).escape("VLIM ").float().eos().build(),
            CmdBuilder(self.get_voltage_limit).escape("VLIM?").eos().build(),
            CmdBuilder(self.set_current_limit).escape("ILIM ").float().eos().build(),
            CmdBuilder(self.get_current_limit).escape("ILIM?").eos().build(),
            CmdBuilder(self.set_current_trip_limit).escape("ITRP ").float().eos().build(),
            CmdBuilder(self.get_current_trip_limit).escape("ITRP?").eos().build(),
            CmdBuilder(self.get_serial_poll_byte).escape("*STB?").eos().build(),
            CmdBuilder(self.get_voltage).escape("VOUT?").eos().build(),
            CmdBuilder(self.get_current).escape("IOUT?").eos().build(),
        }

    def handle_error(self, request, error):
        """
        If command is not recognised print and error

        Args:
            request: requested string
            error: problem

        """
        self.log.error("An error occurred at request " + repr(request) + ": " + repr(error))

    def get_status_register(self):
        return "00000000"

    def clear_trip(self):
        self.device.clear()

    def enable_highvoltage(self):
        self.device.hv = True

    def disable_highvoltage(self):
        self.device.hv = False

    def set_voltage(self, voltage):
        self.device.voltage = voltage

    def set_voltage_limit(self, limit):
        self.device.voltage_limit = limit

    def get_voltage_limit(self):
        return self.device.voltage_limit

    def set_current_limit(self, limit):
        self.device.current_limit = limit

    def get_current_limit(self):
        return self.device.current_limit

    def set_current_trip_limit(self, limit):
        self.device.current_trip_limit = limit

    def get_current_trip_limit(self):
        return self.device.current_trip_limit

    def get_serial_poll_byte(self):
        return int(f"{0}{int(self.device.get_voltage_tripped)}{int(self.device.get_current_tripped)}"
                   f"{int(self.device.get_limit_exceeded())}{0}{0}{0}{int(self.device.hv)}", 2)

    def get_voltage(self):
        return self.device.voltage

    def get_current(self):
        return self.device.current




