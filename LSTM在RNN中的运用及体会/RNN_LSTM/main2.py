import numpy as np
import random
import time
from test4 import cllm_utils

data = open('dinos.txt', 'r').read().lower()
chars = list(set(data))

char_to_ix = {ch: i for i, ch in enumerate(sorted(chars))}
ix_to_char = {i: ch for i, ch in enumerate(sorted(chars))}


def clip(gradients, maxvalue):
    dWaa, dWax, dWya, db, dby = gradients['dWaa'], gradients['dWax'], gradients['dWya'], gradients['db'], gradients[
        'dby']
    for gradient in [dWaa, dWax, dWya, db, dby]:
        np.clip(gradient, -maxvalue, maxvalue, out=gradient)



def sample(parameters, char_to_ix, seed):
    Waa, Wax, Wya, by, b = parameters['Waa'], parameters['Wax'], parameters['Wya'], parameters['by'], parameters['b']
    vocab_size = by.shape[0]
    n_a = Waa.shape[1]

    x = np.zeros((vocab_size, 1))
    a_prev = np.zeros((n_a, 1))
    indices = []
    idx = -1
    counter = 0
    newline_char = char_to_ix['\n']
    while (idx != newline_char and counter < 50):
        a = np.tanh(np.dot(Wax, x) + np.dot(Waa, a_prev) + b)
        a_prev = a
        z = np.dot(Wya, a) + by
        y = cllm_utils.softmax(z)
        np.random.seed(counter + seed)
        idx = np.random.choice(list(range(vocab_size)), p=y.ravel())
        indices.append(idx)
        x = np.zeros((vocab_size, 1))
        x[idx] = 1
        seed += 1
        counter += 1
    if counter == 50:
        indices.append(char_to_ix['\n'])
    return indices


def optimize(X, Y, a_prev, parameters, learning_rate=0.01):
    loss, cache = cllm_utils.rnn_forward(X, Y, a_prev, parameters)
    gradients, a = cllm_utils.rnn_backward(X, Y, parameters, cache)
    clip(gradients, 5)
    cllm_utils.update_parameters(parameters, gradients, learning_rate)
    return loss, a[len(X) - 1]


def model(ix_to_char, char_to_ix, num_iterations=3500, n_a=50, dino_names=7, vocab_size=27):
    n_x, n_y = vocab_size, vocab_size
    parameters = cllm_utils.initialize_parameters(n_a, n_x, n_y)
    loss = cllm_utils.get_initial_loss(vocab_size, dino_names)
    with open('dinos.txt', 'r') as f:
        examples = f.readlines()
    examples = [x.lower().strip() for x in examples]
    np.random.seed(0)
    np.random.shuffle(examples)
    a_prev = np.zeros((n_a, 1))

    for j in range(num_iterations):
        index = j % len(examples)
        X = [None] + [char_to_ix[ch] for ch in examples[index]]
        Y = X[1:] + [char_to_ix["\n"]]
        curr_loss, a_prev = optimize(X, Y, a_prev, parameters)
        loss = cllm_utils.smooth(loss, curr_loss)
        if j % 2000 == 0:
            print("第" + str(j + 1) + "次迭代，损失值为：" + str(loss))
            seed = 0
            for name in range(dino_names):
                indices = sample(parameters, char_to_ix, seed)
                cllm_utils.print_sample(indices, ix_to_char)
                seed += 1
    return parameters


parameters = model(ix_to_char, char_to_ix, num_iterations=3500)

