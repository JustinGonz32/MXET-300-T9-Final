import L1_ina
import L1_log
from time import sleep

def getVoltage(): 
    while True:
        var_volt = L1_ina.readVolts()
        L1_log.tmpFile(var_volt, "Volt_NodeRED")
        sleep(1)