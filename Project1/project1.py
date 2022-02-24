# driver code for exercise 1, project 1
from sim import *

simxFinish(-1)
clientID = simxStart('127.0.0.1', 19997, True, True, 3000, 1)
# print(clientID)
if clientID != -1:
    print('success')
    simxLoadScene(clientID, 'p1-e1.ttt', True, simx_opmode_blocking)
    simxStartSimulation(clientID, simx_opmode_oneshot)
    simxStopSimulation(clientID, simx_opmode_oneshot_wait)
    simxFinish(clientID)

