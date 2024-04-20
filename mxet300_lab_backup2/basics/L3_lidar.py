import L2_vector
import L1_log
import L1_lidar
import pysicktim as lidar 
import L1_ina
from time import sleep



while True:
    data = L2_vector.getNearest()
    #print("Data: ", data)
    cart = L2_vector.polar2cart(data[0],data[1])
    #print("Cart: ", cart)
    L1_log.tmpFile(data[0], "sumVec")
    L1_log.tmpFile(data[1], "Heading")
    L1_log.tmpFile(cart[0], "Cart_X")
    L1_log.tmpFile(cart[1], "Cart_Y")
    var_volt = L1_ina.readVolts()
    L1_log.tmpFile(var_volt, "Volt_NodeRED")
    print("r is: ", data[0])
    print("Heading is: ", data[1])
    print("X is: ", cart[0])
    print("Y is: ", cart[1])
    sleep(1)