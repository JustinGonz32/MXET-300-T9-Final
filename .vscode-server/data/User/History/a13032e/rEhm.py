#acquire wheel speed and chassis speed measurements as [PDL, PDR] and [xdot, thetadot]
import L1_encoder
import L2_kinematics
import L1_log
import L1_ina
from time import sleep

while True:
    var_volt = L1_ina.readVolts()
    L1_log.tmpFile(var_volt, "Volt_NodeRED")
    encValues = L1_encoder.readShaftPositions()
    PDL = encValues[0]
    L1_log.tmpFile(PDL, "PDL_NR")
    PDR = encValues[1]
    L1_log.tmpFile(PDR, "PDR_NR")
    C = L2_kinematics.getMotion()
    L1_log.tmpFile(C[0], "XDot")
    L1_log.tmpFile(C[1], "XDot")
    sleep(1)