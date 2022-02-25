# driver code for exercise 1, project 1
from time import sleep
from math import dist, atan2, pi, remainder
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
simxLoadScene(cid, 'p1-c1.ttt', True, simx_opmode_blocking)
simxStartSimulation(cid, simx_opmode_oneshot)

retcode, robot = simxGetObjectHandle(cid, 'lumibot', simx_opmode_blocking)
retcode, start = simxGetObjectHandle(cid, 'start', simx_opmode_blocking)
retcode, lmotor = simxGetObjectHandle(cid, 'lumibot_leftMotor', simx_opmode_blocking)
retcode, rmotor = simxGetObjectHandle(cid, 'lumibot_rightMotor', simx_opmode_blocking)
retcode, destination = simxGetObjectHandle(cid, 'lumibot_dest', simx_opmode_blocking)

throwaway, pos_init = simxGetObjectPosition(cid, start, -1, simx_opmode_blocking)
throwaway, rot_init = simxGetObjectOrientation(cid, start, -1, simx_opmode_blocking)

buffer = bytearray()
path = []
a, b, raw, d, e = simxCallScriptFunction(cid, 'lumibot', sim_scripttype_childscript, 'pathfind', [], [], [], buffer,
                                         simx_opmode_blocking)
for p in [a, b, raw, d, e]:
    print(p)
# print(pos_init)
# print(rot_init)

# reformat of raw path data
i = 0
while i < len(raw):
    path.append(((raw[i], raw[i+1], pos_init[2]), (rot_init[0], rot_init[1], raw[i+2])))
    i += 3

d = .0886/2
r = .024738
eps = .08

for xy, angle in path:
    p, curr_pos = simxGetObjectPosition(cid, robot, -1, simx_opmode_blocking)
    p, curr_rot = simxGetObjectPosition(cid, robot, -1, simx_opmode_blocking)
    print(curr_rot[2] - atan2(xy[1] - curr_pos[1], xy[0] - curr_pos[0]))
    while dist(xy, curr_pos) > eps:
        dtheta = remainder(curr_rot[2] - atan2(xy[1] - curr_pos[1], xy[0] - curr_pos[0]) - (0), 2*pi)
        print(dist(xy, curr_pos))
        if abs(dtheta) > pi/16:
            v = .02
        else:
            v = .08
        w = .8 * dtheta
        wright = (v - d * w) / r
        wleft = (v + d * w) / r

        simxSetJointTargetVelocity(cid, lmotor, wleft, simx_opmode_oneshot)
        simxSetJointTargetVelocity(cid, rmotor, wright, simx_opmode_oneshot)

        sleep(.025)
        p, curr_pos = simxGetObjectPosition(cid, robot, -1, simx_opmode_blocking)
        p, curr_rot = simxGetObjectPosition(cid, robot, -1, simx_opmode_blocking)

simxSetJointTargetVelocity(cid, lmotor, 0, simx_opmode_oneshot)
simxSetJointTargetVelocity(cid, rmotor, 0, simx_opmode_oneshot)


sleep(10)
simxStopSimulation(cid, simx_opmode_oneshot_wait)
simxFinish(cid)
