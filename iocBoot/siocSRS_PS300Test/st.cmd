#!../../bin/linux-x86_64/SRS_PS300Test

###############################################################################
# Set up environment
epicsEnvSet("MODEL","$(MODEL=370)")
epicsEnvSet("P","$(P=SRS_PS$(MODEL):)")
epicsEnvSet("R","$(R=1:)")
epicsEnvSet("SRSPS300_ADDRESS","$(SRSPS300_ADDRESS=serialapex01:4003)")
< envPaths
epicsEnvSet("STREAM_PROTOCOL_PATH","${TOP}/db")
cd "${TOP}"

###############################################################################
# Register all support components
dbLoadDatabase "dbd/SRS_PS300Test.dbd"
SRS_PS300Test_registerRecordDeviceDriver pdbbase

###############################################################################
# Set up ASYN port
# SRS PS300 supplies support only 9600-8N1
# drvAsynIPPortConfigure port ipInfo priority noAutoconnect noProcessEos
drvAsynIPPortConfigure("L0","$(SRSPS300_ADDRESS) COM",0,0,0)
asynSetTraceIOMask("L0",-1,0x2)
#asynSetTraceMask("L0",-1,0x9)
asynSetOption("L0", -1, "baud", "9600")
asynSetOption("L0", -1, "bits", "8")
asynSetOption("L0", -1, "parity", "none")
asynSetOption("L0", -1, "stop", "1")
asynSetOption("L0", -1, "crtscts", "N")

###############################################################################
# Load record instances
dbLoadRecords "db/devSRS_PS$(MODEL).db" "P=$(P),R=$(R),PORT=L0,A=-1"
dbLoadRecords "db/asynRecord.db" "P=$(P),R=asyn,PORT=L0,ADDR=-1,OMAX=0,IMAX=0"

###############################################################################
# Start IOC
cd "${TOP}/iocBoot/${IOC}"
iocInit
