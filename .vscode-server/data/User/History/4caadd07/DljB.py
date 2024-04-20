import L2_compass_heading

def getCompassHeading():
    head = L2_compass_heading.get_heading()
    print(head)

def headToCardinal(head):
    directions = ["North", "North East", "East", "South East", "South", "South West", "West", "North West", "North"]
    index = round(float(head) / 45) % 8
    return directions[index]


while True:
    var_degree = getCompassHeading()
    var_dir = headToCardinal(var_degree)
    #L1_log.tmpFile(var_degree, var_dir,"Volt_NodeRED")
    #sleep(1)
    print(var_degree)
    print(var_dir)
    