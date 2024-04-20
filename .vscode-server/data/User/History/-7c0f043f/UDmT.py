import L2_vector
import L1_log
from time import sleep



while True:
    cart = L2_vector.polar2cart(getNearest())
    L1_log.tmpFile(cart[0], "Cart_X")
    L1_log.tmpFile(vcart[1], "Cart_Y")
    print("X is: ", cart[0])
    print("Y is: ", cart[1])
    sleep(1)