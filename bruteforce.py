import scipy.signal
import numpy as np
import multiprocessing
import time

alpha=0.8
beta=19
delta=0.4

processes = []

#start val, end val, res
sim_settings = (0, 50, 0.01)

#range to sim over
t = np.arange(*sim_settings)

#basline value
r0 = 0

#90 degrees in rads
r_s = np.pi/2

#unit step input
r  = np.array([r0 if x < 1 else r_s for x in t])

#start val, end val, res
kp_settings = (0.7, 1.5, 0.001)
ki_settings = (0, 0.3, 0.01)
kd_settings = (0.2, 0.4, 0.001)


def func(kp):
    for kd in np.arange(*kd_settings):
        for ki in np.arange(*ki_settings):
            G_CL = scipy.signal.lti([beta*kp, beta*ki], [1, alpha+beta*kd, delta+beta*kp, beta*ki])
            out = scipy.signal.lsim(G_CL, r, T=t, X0=None, interp=True)
            cache = out[1]*180/np.pi
            #checking specs 
                #overshoot              #                       #steady state error
            if ((max(cache) < 95) and (cache[170] > 82) and (-1 < ((cache[-1]-90)) < 1 )):
                with open(f"{kp=},{kd=},{ki=}.txt", "w+") as txt:
                    #this is done as the code will run in multiple processes and file writing
                    #between multiple processes leads to error without the Global Interpreter Lock
                    txt.write(f"{kp=},{kd=},{ki=}")
                print(f"{kp=},{kd=},{ki=}") #this was a cheaty work around to put all results in to 1 file

def start_force():
    #added all the Processes
    for kp in np.arange(*kp_settings):
        proce = multiprocessing.Process(target=func, args=(kp,))
        processes.append(proce)
    #starting the Processes
    for proce in processes:   
        proce.start()

    #joining the Processes
    for pro in processes:
        pro.join()

start = time.time()
start_force()
end = time.time()

print(f"BRUTE FORCE FINISHED: TIME TAKEN {start - end}")