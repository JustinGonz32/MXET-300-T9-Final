import L2_compass_heading

def getCompassHeading():
    head = L2_compass_heading.get_heading()

def headToCardinal(head):
    directions = ["North", "North East", "East", "South East", "South", "South West", "West", "North West"]
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
    #L1_log.tmpFile(var_degree, var_dir,"Volt_NodeRED")
    #sleep(1)
    print(var_degree)
    print(var_dir)
    