#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import scipy as sp
from scipy import sparse
from scipy.sparse import linalg

def pipe_pr_master_cg(A,b,x0,max_iter,variant='',callbacks=[],**kwargs):
    '''
    master template for pipelined predict-and-recompute conjugate gradients
    '''
    
    # get size of problem
    n = len(b)
    
    # initialize
    output = {}
    output['name'] = f"pipe_{variant}_cg"
    output['max_iter'] = max_iter
    
    x_k    =  np.copy(x0)
    r_k    =  np.copy(b - A @ x_k)
    p_k    =  np.copy(r_k)
    nu_k   =  r_k   @ r_k
    s_k    =  A     @ p_k
    w_k    =  np.copy(s_k)
    u_k    =  A     @ w_k
    mu_k   =  p_k   @ s_k
    a_k    =  nu_k / mu_k
    a_k1   =  0
    a_k2   =  0
    b_k    =  0
    b_k1   =  0
    del_k  =  r_k   @ s_k
    gam_k  =  s_k   @ s_k

    k=0
    for callback in callbacks:
        callback(**locals())
    
    # run main optimization
    for k in range(1,max_iter):

        # update indexing
        a_k2   =  a_k1
        a_k1   =  a_k
        b_k1   =  b_k
        nu_k1  =  nu_k
        del_k1 =  del_k
        gam_k1 =  gam_k
        
        x_k1   =  np.copy(x_k)
        r_k1   =  np.copy(r_k)
        w_k1   =  np.copy(w_k)
        p_k1   =  np.copy(p_k)
        s_k1   =  np.copy(s_k)
        u_k1   =  np.copy(u_k)
        
        # main loop
        x_k    =  x_k1  +   a_k1 * p_k1
        r_k    =  r_k1  -   a_k1 * s_k1
        w_k    =  w_k1  -   a_k1 * u_k1
        nu_k   = - nu_k1 + a_k1**2 * gam_k1 if variant[-1:] == 'm' else \
                 nu_k1 - 2 * a_k1 * del_k1 + a_k1**2 * gam_k1
        b_k    =  nu_k / nu_k1
        p_k    =  r_k   +   b_k * p_k1
        s_k    =  w_k   +   b_k * s_k1
        u_k    =  A     @ s_k
        w_k    =  A     @ r_k if variant[:2] == 'pr' else w_k
        mu_k   =  p_k   @ s_k
        del_k  =  r_k   @ s_k
        gam_k  =  s_k   @ s_k
        nu_k   =  r_k   @ r_k 
        a_k    =  nu_k / mu_k
    
        # call callback functions
        for callback in callbacks:
            callback(**locals())
            
    return output

def pipe_p_cg(A,b,x0,max_iter,callbacks=[],**kwargs):
    '''
    pipelined predict conjugate gradient
    '''
    return pipe_pr_master_cg(A,b,x0,max_iter,callbacks=callbacks,variant='p',**kwargs)

def pipe_pr_cg(A,b,x0,max_iter,callbacks=[],**kwargs):
    '''
    pipelined predict-and-recompute conjugate gradient
    '''
    return pipe_pr_master_cg(A,b,x0,max_iter,callbacks=callbacks,variant='pr',**kwargs)

def pipe_p_m_cg(A,b,x0,max_iter,callbacks=[],**kwargs):
    '''
    pipelined predict Meurant conjugate gradient
    '''
    return pipe_pr_master_cg(A,b,x0,max_iter,callbacks=callbacks,variant='p_m',**kwargs)

def pipe_pr_m_cg(A,b,x0,max_iter,callbacks=[],**kwargs):
    '''
    pipelined predict-and-recompute Meurant conjugate gradient
    '''
    return pipe_pr_master_cg(A,b,x0,max_iter,callbacks=callbacks,variant='pr_m',**kwargs)



def pipe_pr_master_pcg(A,b,x0,max_iter,variant='',preconditioner=lambda x:x,callbacks=[],**kwargs):
    '''
    master template for pipelined predict-and-recompute conjugate gradients (preconditioned)
    '''
    
    # get size of problem
    n = len(b)
    
    # initialize
    output = {}
    output['name'] = f"pipe_{variant}_pcg"
    output['max_iter'] = max_iter
    
    x_k    =  np.copy(x0)
    r_k    =  np.copy(b - A @ x_k)
    rt_k   =  preconditioner(r_k)
    p_k    =  np.copy(rt_k)
    nu_k   =  rt_k   @ r_k
    s_k    =  A     @ p_k
    st_k   =  preconditioner(s_k)
    w_k    =  np.copy(s_k)
    wt_k   =  np.copy(st_k)
    u_k    =  A     @ st_k
    ut_k   =  preconditioner(u_k)
    mu_k   =  p_k   @ s_k
    a_k    =  nu_k / mu_k
    a_k1   =  0
    a_k2   =  0
    b_k    =  0
    b_k1   =  0
    del_k  =  r_k   @ st_k
    gam_k  =  st_k  @ s_k

    k=0
    for callback in callbacks:
        callback(**locals())
    
    # run main optimization
    for k in range(1,max_iter):

        # update indexing
        a_k2   =  a_k1
        a_k1   =  a_k
        b_k1   =  b_k
        nu_k1  =  nu_k
        del_k1 =  del_k
        gam_k1 =  gam_k
        
        x_k1   =  np.copy(x_k)
        r_k1   =  np.copy(r_k)
        rt_k1  =  np.copy(rt_k)
        w_k1   =  np.copy(w_k)
        wt_k1  =  np.copy(wt_k)
        p_k1   =  np.copy(p_k)
        s_k1   =  np.copy(s_k)
        st_k1  =  np.copy(st_k)
        u_k1   =  np.copy(u_k)
        ut_k1  =  np.copy(ut_k)
        
        # main loop
        x_k    =  x_k1  +   a_k1 * p_k1
        r_k    =  r_k1  -   a_k1 * s_k1
        rt_k   =  rt_k1 -   a_k1 * st_k1
        w_k    =  w_k1  -   a_k1 * u_k1
        wt_k   =  wt_k1 -   a_k1 * ut_k1
        nu_k   = - nu_k1 + a_k1**2 * gam_k1 if variant[-1:] == 'm' else nu_k1 - 2 * a_k1 * del_k1 + a_k1**2 * gam_k1
        b_k    =  nu_k / nu_k1
        p_k    =  rt_k  +   b_k * p_k1
        s_k    =  w_k   +   b_k * s_k1
        st_k   =  wt_k  +   b_k * st_k1
        u_k    =  A     @ st_k 
        ut_k   =  preconditioner(u_k)
        w_k    =  A     @ rt_k if variant[:2] == 'pr' else w_k
        wt_k   =  preconditioner(w_k) if variant[:2] == 'pr' else wt_k
        mu_k   =  p_k   @ s_k
        del_k  =  r_k   @ st_k # or rt_k @ s_k or p_k @ s_k
        gam_k  =  st_k  @ s_k 
        nu_k   =  rt_k  @ r_k 
        a_k    =  nu_k / mu_k
        
        # call callback functions
        for callback in callbacks:
            callback(**locals())
            
    return output

def pipe_p_pcg(A,b,x0,max_iter,preconditioner=lambda x:x,callbacks=[],**kwargs):
    '''
    pipelined predict conjugate gradient (preconditioned)
    '''
    return pipe_pr_master_pcg(A,b,x0,max_iter,preconditioner=preconditioner,callbacks=callbacks,variant='p',**kwargs)

def pipe_pr_pcg(A,b,x0,max_iter,preconditioner=lambda x:x,callbacks=[],**kwargs):
    '''
    pipelined predict-and-recompute conjugate gradient (preconditioned)
    '''
    return pipe_pr_master_pcg(A,b,x0,max_iter,preconditioner=preconditioner,callbacks=callbacks,variant='pr',**kwargs)

def pipe_p_m_pcg(A,b,x0,max_iter,preconditioner=lambda x:x,callbacks=[],**kwargs):
    '''
    pipelined predict Meurant conjugate gradient (preconditioned)
    '''
    return pipe_pr_master_pcg(A,b,x0,max_iter,preconditioner=preconditioner,callbacks=callbacks,variant='p_m',**kwargs)

def pipe_pr_m_pcg(A,b,x0,max_iter,preconditioner=lambda x:x,callbacks=[],**kwargs):
    '''
    pipelined predict-and-recompute Meurant conjugate gradient (preconditioned)
    '''
    return pipe_pr_master_pcg(A,b,x0,max_iter,preconditioner=preconditioner,callbacks=callbacks,variant='pr_m',**kwargs)


