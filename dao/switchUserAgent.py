def switchUserAgent(userAgents,agent_index):
    """更换代理IP"""

    newAgent_index=[]
    agentNumber=len(userAgents)
    #返回当前代理IP的下一个代理IP
    if agent_index[1] != (agentNumber-1) :
        userAgent=userAgents[agent_index[1]+1]
        newAgent_index.append(userAgent)
        newAgent_index.append(agent_index[1]+1)
        return newAgent_index

    #返回第一个代理IP
    else :
        newAgent_index.append(userAgents[0])
        newAgent_index.append(0)
