import L2_vector
import L1_log
import L1_lidar
import pysicktim as lidar 
from time import sleep



while True:
    data = L2_vector.getNearest()
    L2_vector.sumVec(data[0],data[1])
    L1_log.tmpFile(cart[0], "Cart_X")
    L1_log.tmpFile(vcart[1], "Cart_Y")
    print("X is: ", cart[0])
    print("Y is: ", cart[1])
    sleep(1)