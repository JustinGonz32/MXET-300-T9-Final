import L2_compass_heading
import L1_log
from time import sleep

def getCompassHeading():
    head = L2_compass_heading.get_heading()
    return head

def headToCardinal(head):
    head = float(head)
    directions = ["North", "North West", "West", "South West", "South", "South East", "East", "North East"]
    if (-22.5 < head < 22.5):
        directions_out = directions[0]
    if (22.5 < head < 67.5):
        directions_out = directions[1]
    if (67.5 < head < 112.5):
        directions_out = directions[2]
    if (112.5 < head < 157.5):
        directions_out = directions[3]        
    if (157.5 < head) | (head < -157.5):
        directions_out = directions[4]   
    if (-112.5 > head > -157.5):
        directions_out = directions[5] 
    if (-67.5 > head > -112.5):
        directions_out = directions[6]         
    if (-22.5 > head > -67.5):
        directions_out = directions[5] 
    return directions_out

while True:
    var_degree = getCompassHeading()
    var_dir = headToCardinal(var_degree)
    L1_log.tmpFile(var_degree, "Deg_NR")
    L1_log.stringTmpFile(var_dir,"Dir_NR")
    sleep(1)
    