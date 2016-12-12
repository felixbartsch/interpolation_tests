#!/usr/bin/env python
import sys
import numpy as np
import scipy as sp
import matplotlib
import matplotlib.pyplot as plt
import interpolation
import multiprocessing
from inspect import getmembers, isfunction
#integer numbers!
cfg = {"lb_interpolation_window" : 6,
       "ub_interpolation_window" : 30,
       "acquisitions" : 0 }

def correlation_wrapper(tp):
    interp_method = tp[0]
    return interp_method(tp[1],tp[2],tp[3])[1]

if __name__ == "__main__":
    
    f_samples = open("./samples_20_09_16-17:54:35.txt","r")
    samples_list = []
    interp_types =[o for o in getmembers(interpolation,isfunction)]
    
    for line_number, line in enumerate(f_samples.readlines()):  
        if cfg["acquisitions"] != 0:
            if line_number >= cfg["acquisitions"]:
                break
        acquisition_samples = eval(eval(line))
        receivers_samples = np.array(acquisition_samples[0])
        samples_list.append(receivers_samples)
    if cfg["acquisitions"] == 0:
        cfg["acquisitions"] = len(samples_list)
    num_cores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=num_cores)
    delay_tensor= np.ndarray(shape=(len(interp_types), len(receivers_samples)-1, cfg['ub_interpolation_window'] - cfg['lb_interpolation_window'] , cfg["acquisitions"] ))
    
    for window_interest in range(cfg['lb_interpolation_window'] ,cfg['ub_interpolation_window'] ):
        
        #for idx2,receivers_samples in enumerate(samples_list):
        for receiver in range(len(receivers_samples)):
            if receiver != 0:
                for idx,interp_method in enumerate(interp_types):
                    #check storing of delays!
                    #correlation , delay = interp_method[1](np.array([receivers_samples[receiver]]),np.array([receivers_samples[0]]),window_interest)
                    #print cfg["acquisitions"]
                    delay_tensor[idx, receiver-1, window_interest-cfg['lb_interpolation_window'], :] = pool.map(correlation_wrapper,[(interp_method[1], np.array([samples_list[k][receiver]]),np.array([samples_list[k][0]]),window_interest) for k in range(cfg["acquisitions"])])
        print window_interest
    cov_tensor= np.ndarray(shape=(len(interp_types), len(receivers_samples)-1, cfg['ub_interpolation_window'] - cfg['lb_interpolation_window'] ))
    for window_interest in range(cfg['lb_interpolation_window'] ,cfg['ub_interpolation_window'] ):  
        for receiver in range(len(receivers_samples)):
            for idx,interp_method in enumerate(interp_types):
                cov_tensor[idx, receiver-1, window_interest-cfg['lb_interpolation_window']] = np.cov(delay_tensor[idx, receiver-1, window_interest-cfg['lb_interpolation_window'], :])
    f, axarr = plt.subplots(2, sharex=True)
    plt.hold(True)
    
    handles_0 = []
    handles_0.append(axarr[0].plot(np.arange(cfg["lb_interpolation_window"],cfg["ub_interpolation_window"],1), cov_tensor[0,0,:], label="no interpolation"))
    handles_0.append(axarr[0].plot(np.arange(cfg["lb_interpolation_window"],cfg["ub_interpolation_window"],1), cov_tensor[1,0,:], label="sample interpolation"))
    handles_0.append(axarr[0].plot(np.arange(cfg["lb_interpolation_window"],cfg["ub_interpolation_window"],1), cov_tensor[2,0,:], label="spline interpolation"))
    axarr[0].legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    axarr[0].set_xlabel('interpolation window')
    axarr[0].set_ylabel('covariance')
    axarr[0].set_title('covariances for different kinds of intepolation')
    print handles_0
    handles_1 = []
    handles_1.append(axarr[1].plot(np.arange(cfg["lb_interpolation_window"],cfg["ub_interpolation_window"],1), cov_tensor[0,1,:], label="no interpolation"))
    handles_1.append(axarr[1].plot(np.arange(cfg["lb_interpolation_window"],cfg["ub_interpolation_window"],1), cov_tensor[1,1,:], label="sample interpolation"))
    handles_1.append(axarr[1].plot(np.arange(cfg["lb_interpolation_window"],cfg["ub_interpolation_window"],1), cov_tensor[2,1,:], label="spline interpolation"))
    axarr[1].set_xlabel('interpolation window')
    axarr[1].set_ylabel('covariance')
    axarr[1].legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.autoscale()
    plt.show()
    

    print cov_tensor
    #print delay_tensor.shape
