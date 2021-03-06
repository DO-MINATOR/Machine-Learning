import numpy as np
from test4 import rnn_utils


# def rnn_cell_forward(xt, a_prev, parameters):
#     Wax = parameters['Wax']
#     Waa = parameters['Waa']
#     Wya = parameters['Wya']
#     ba = parameters['ba']
#     by = parameters['by']
#
#     a_next = np.tanh(np.dot(Waa, a_prev) + np.dot(Wax, xt) + ba)
#     yt_pred = rnn_utils.softmax(np.dot(Wya, a_next) + by)
#     cache = (a_next, a_prev, xt, parameters)
#     return a_next, yt_pred, cache
#
#
# def rnn_forward(x, a0, parameters):
#     caches = []
#     n_x, m, T_x = x.shape
#     n_y, n_a = parameters['Wya'].shape
#
#     a = np.zeros([n_a, m, T_x])
#     y_pred = np.zeros([n_y, m, T_x])
#
#     a_next = a0
#
#     for t in range(T_x):
#         a_next, yt_pred, cache = rnn_cell_forward(x[:, :, t], a_next, parameters)
#         a[:, :, t] = a_next
#         y_pred[:, :, t] = yt_pred
#         caches.append(cache)
#     caches = (cache, x)
#
#     return a, y_pred, caches


def lstm_cell_forward(xt, a_prev, c_prev, parameters):
    Wf = parameters["Wf"]
    bf = parameters["bf"]
    Wi = parameters["Wi"]
    bi = parameters["bi"]
    Wc = parameters["Wc"]
    bc = parameters["bc"]
    Wo = parameters["Wo"]
    bo = parameters["bo"]
    Wy = parameters["Wy"]
    by = parameters["by"]

    n_x, m = xt.shape
    n_y, n_a = Wy.shape

    contact = np.zeros([n_a + n_x, m])
    contact[:n_a, :] = a_prev
    contact[n_a:, :] = xt
    ft = rnn_utils.sigmoid(np.dot(Wf, contact) + bf)
    it = rnn_utils.sigmoid(np.dot(Wi, contact) + bi)
    cct = np.tanh(np.dot(Wc, contact) + bc)
    c_next = ft * c_prev + it * cct
    ot = rnn_utils.sigmoid(np.dot(Wo, contact) + bo)
    a_next = ot * np.tanh(c_next)
    yt_pred = rnn_utils.softmax(np.dot(Wy, a_next) + by)
    cache = (a_next, c_next, a_prev, c_prev, ft, it, cct, ot, xt, parameters)
    return a_next, c_next, yt_pred, cache


def lstm_forward(x, a0, parameters):
    caches = []
    n_x, m, T_x = x.shape
    n_y, n_a = parameters['Wy'].shape

    a = np.zeros([n_a, m, T_x])
    c = np.zeros([n_a, m, T_x])
    y = np.zeros([n_y, m, T_x])

    a_next = a0
    c_next = np.zeros([n_a,m])

    for t in range(T_x):
        a_next,c_next,yt_pred,cache=lstm_cell_forward(x[:,:,t],a_next,c_next,parameters)
        a[:,:,t] = a_next
        c[:,:,t]=c_next
        y[:,:,t] = yt_pred
        caches.append(cache)
    caches = (caches,x)
    return a,c,y,caches


        
