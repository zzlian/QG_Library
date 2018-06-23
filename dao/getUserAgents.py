import re

def getUserAgent():
    userAgents = []
    filePath = r"C:\Users\lenovo\Desktop\super_agent.txt"
    file = open(filePath, "r")

    for line in file:
        userAgents.append(re.sub(r"\n", "", line))

    file.close()
    return userAgents