import L2_vector
import L1_log
import L1_lidar as lidar
from time import sleep



while True:
    scan = lidar.polarScan() 
    cart = L2_vector.polar2cart(scan)
    L1_log.tmpFile(cart[0], "Cart_X")
    L1_log.tmpFile(vcart[1], "Cart_Y")
    print("X is: ", cart[0])
    print("Y is: ", cart[1])
    sleep(1)