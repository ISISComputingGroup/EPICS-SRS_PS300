TOP=../..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================

#=============================
# Build the IOC application

PROD_IOC = SRS_PS300Test
# SRS_PS300Test.dbd will be created and installed
DBD += SRS_PS300Test.dbd

# SRS_PS300Test.dbd will be made up from these files:
SRS_PS300Test_DBD += base.dbd

# Include dbd files from all support applications:
SRS_PS300Test_DBD += stream.dbd
SRS_PS300Test_DBD += drvAsynIPPort.dbd

# Add all the support libraries needed by this IOC
SRS_PS300Test_LIBS += stream
SRS_PS300Test_LIBS += asyn

# SRS_PS300Test_registerRecordDeviceDriver.cpp derives from SRS_PS300Test.dbd
SRS_PS300Test_SRCS += SRS_PS300Test_registerRecordDeviceDriver.cpp

# Build the main IOC entry point on workstation OSs.
SRS_PS300Test_SRCS_DEFAULT += SRS_PS300TestMain.cpp
SRS_PS300Test_SRCS_vxWorks += -nil-

# Add support from base/src/vxWorks if needed
#SRS_PS300Test_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary

# Finally link to the EPICS Base libraries
SRS_PS300Test_LIBS += $(EPICS_BASE_IOC_LIBS)

#===========================

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

