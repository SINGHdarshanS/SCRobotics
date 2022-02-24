# driver code for exercise 1, project 1
from sim import *

# simxFinish(-1)
# clientID = simxStart('127.0.0.1', 19997, True, True, 3000, 1)
# # print(clientID)
# if clientID != -1:
#     print('success')
#     simxLoadScene(clientID, 'p1-e1.ttt', True, simx_opmode_blocking)
#     simxStartSimulation(clientID, simx_opmode_oneshot)
#     simxStopSimulation(clientID, simx_opmode_oneshot_wait)
#     simxFinish(clientID)



# workflow: set scene -> get handles -> get initial positions and orientations -> compute path (36:00)
# -> visualize path -> follow path

simxFinish(-1)
cid = simxStart('127.0.0.1', 19997, True, True, 3000, 1)
simxLoadScene(cid, 'p1-e1.ttt', True, simx_opmode_blocking)
simxStartSimulation(cid, simx_opmode_oneshot)

retcode, robot = simxGetObjectHandle(cid, 'lumibot', simx_opmode_blocking)
retcode, lmotor = simxGetObjectHandle(cid, 'lumibot_leftMotor', simx_opmode_blocking)
retcode, rmotor = simxGetObjectHandle(cid, 'lumibot_rightMotor', simx_opmode_blocking)
retcode, destination = simxGetObjectHandle(cid, 'lumibot_dest', simx_opmode_blocking)

pos_init = simxGetObjectPosition(cid, robot, -1, simx_opmode_blocking)
rot_init = simxGetObjectOrientation(cid, robot, -1, simx_opmode_blocking)

buffer = bytearray()
path = []
a, b, c, d, e = simxCallScriptFunction(cid, 'lumibot', sim_scripttype_childscript, 'pathfind', [], [], [], buffer,
                                       simx_opmode_blocking)


# path is computed here
