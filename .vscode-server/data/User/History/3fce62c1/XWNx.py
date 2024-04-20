import L1_ina
import L1_log

def getVoltage(): 
    while True:
        var_volt = L1_ina.readVolts()
        L1_log.tmpFile(var_volt, "Volt_NodeRED")
        sleep(1)