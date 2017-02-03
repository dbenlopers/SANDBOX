#!/usr/bin/env python3
# encoding: utf-8
"""
source : http://iamtrask.github.io/2015/07/12/basic-python-network/
"""

import numpy as np

### ONLY CODE
X = np.array([[0, 0, 1], [0, 1, 1], [1, 0, 1], [1, 1, 1]])
y = np.array([[0, 1, 1, 0]]).T
syn0 = 2 * np.random.random((3, 4)) - 1
syn1 = 2 * np.random.random((4, 1)) - 1
for j in xrange(60000):
    l1 = 1 / (1 + np.exp(-(np.dot(X, syn0))))
    l2 = 1 / (1 + np.exp(-(np.dot(l1, syn1))))
    l2_delta = (y - l2) * (l2 * (1 - l2))
    l1_delta = l2_delta.dot(syn1.T) * (l1 * (1 - l1))
    syn1 += l1.T.dot(l2_delta)
    syn0 += X.T.dot(l1_delta)


# sigmoid function
def nonlin(x, deriv=False):
    if (deriv == True):
        return x * (1 - x)
    return 1 / (1 + np.exp(-x))


# input dataset
X = np.array([[0, 0, 1],
              [0, 1, 1],
              [1, 0, 1],
              [1, 1, 1]])

# output dataset
y = np.array([[0, 0, 1, 1]]).T

# seed random numbers to make calculation
# deterministic (just a good practice)
np.random.seed(1)

# initialize weights randomly with mean 0
syn0 = 2 * np.random.random((3, 1)) - 1

for iter in xrange(10000):
    # forward propagation
    l0 = X
    l1 = nonlin(np.dot(l0, syn0))

    # how much did we miss?
    l1_error = y - l1

    # multiply how much we missed by the
    # slope of the sigmoid at the values in l1
    l1_delta = l1_error * nonlin(l1, True)

    # update weights
    syn0 += np.dot(l0.T, l1_delta)

print("Output After Training:")
print(l1)


def nonlin(x, deriv=False):
    if (deriv == True):
        return x * (1 - x)

    return 1 / (1 + np.exp(-x))


X = np.array([[0, 0, 1],
              [0, 1, 1],
              [1, 0, 1],
              [1, 1, 1]])

y = np.array([[0],
              [1],
              [1],
              [0]])

np.random.seed(1)

# randomly initialize our weights with mean 0
syn0 = 2 * np.random.random((3, 4)) - 1
syn1 = 2 * np.random.random((4, 1)) - 1

for j in xrange(60000):

    # Feed forward through layers 0, 1, and 2
    l0 = X
    l1 = nonlin(np.dot(l0, syn0))
    l2 = nonlin(np.dot(l1, syn1))

    # how much did we miss the target value?
    l2_error = y - l2

    if (j % 10000) == 0:
        print("Error:" + str(np.mean(np.abs(l2_error))))

    # in what direction is the target value?
    # were we really sure? if so, don't change too much.
    l2_delta = l2_error * nonlin(l2, deriv=True)

    # how much did each l1 value contribute to the l2 error (according to the weights)?
    l1_error = l2_delta.dot(syn1.T)

    # in what direction is the target l1?
    # were we really sure? if so, don't change too much.
    l1_delta = l1_error * nonlin(l1, deriv=True)

    syn1 += l1.T.dot(l2_delta)
    syn0 += l0.T.dot(l1_delta)

"""
NN with Gradient descent
source : https://iamtrask.github.io/2015/07/27/python-network-part2/
"""

X = np.array([[0, 0, 1], [0, 1, 1], [1, 0, 1], [1, 1, 1]])
y = np.array([[0, 1, 1, 0]]).T
alpha, hidden_dim = (0.5, 4)
synapse_0 = 2 * np.random.random((3, hidden_dim)) - 1
synapse_1 = 2 * np.random.random((hidden_dim, 1)) - 1
for j in xrange(60000):
    layer_1 = 1 / (1 + np.exp(-(np.dot(X, synapse_0))))
    layer_2 = 1 / (1 + np.exp(-(np.dot(layer_1, synapse_1))))
    layer_2_delta = (layer_2 - y) * (layer_2 * (1 - layer_2))
    layer_1_delta = layer_2_delta.dot(synapse_1.T) * (layer_1 * (1 - layer_1))
    synapse_1 -= (alpha * layer_1.T.dot(layer_2_delta))
    synapse_0 -= (alpha * X.T.dot(layer_1_delta))


# compute sigmoid nonlinearity
def sigmoid(x):
    output = 1 / (1 + np.exp(-x))
    return output


# convert output of sigmoid function to its derivative
def sigmoid_output_to_derivative(output):
    return output * (1 - output)


# input dataset
X = np.array([[0, 1],
              [0, 1],
              [1, 0],
              [1, 0]])

# output dataset
y = np.array([[0, 0, 1, 1]]).T

# seed random numbers to make calculation
# deterministic (just a good practice)
np.random.seed(1)

# initialize weights randomly with mean 0
synapse_0 = 2 * np.random.random((2, 1)) - 1

for iter in xrange(10000):
    # forward propagation
    layer_0 = X
    layer_1 = sigmoid(np.dot(layer_0, synapse_0))

    # how much did we miss?
    layer_1_error = layer_1 - y

    # multiply how much we missed by the
    # slope of the sigmoid at the values in l1
    layer_1_delta = layer_1_error * sigmoid_output_to_derivative(layer_1)
    synapse_0_derivative = np.dot(layer_0.T, layer_1_delta)

    # update weights
    synapse_0 -= synapse_0_derivative

print("Output After Training:")
print(layer_1)

### improved

alphas = [0.001, 0.01, 0.1, 1, 10, 100, 1000]


# compute sigmoid nonlinearity
def sigmoid(x):
    output = 1 / (1 + np.exp(-x))
    return output


# convert output of sigmoid function to its derivative
def sigmoid_output_to_derivative(output):
    return output * (1 - output)


X = np.array([[0, 0, 1],
              [0, 1, 1],
              [1, 0, 1],
              [1, 1, 1]])

y = np.array([[0],
              [1],
              [1],
              [0]])

for alpha in alphas:
    print("\nTraining With Alpha:" + str(alpha))
    np.random.seed(1)

    # randomly initialize our weights with mean 0
    synapse_0 = 2 * np.random.random((3, 4)) - 1
    synapse_1 = 2 * np.random.random((4, 1)) - 1

    for j in xrange(60000):

        # Feed forward through layers 0, 1, and 2
        layer_0 = X
        layer_1 = sigmoid(np.dot(layer_0, synapse_0))
        layer_2 = sigmoid(np.dot(layer_1, synapse_1))

        # how much did we miss the target value?
        layer_2_error = layer_2 - y

        if (j % 10000) == 0:
            print("Error after " + str(j) + " iterations:" + str(np.mean(np.abs(layer_2_error))))

        # in what direction is the target value?
        # were we really sure? if so, don't change too much.
        layer_2_delta = layer_2_error * sigmoid_output_to_derivative(layer_2)

        # how much did each l1 value contribute to the l2 error (according to the weights)?
        layer_1_error = layer_2_delta.dot(synapse_1.T)

        # in what direction is the target l1?
        # were we really sure? if so, don't change too much.
        layer_1_delta = layer_1_error * sigmoid_output_to_derivative(layer_1)

        synapse_1 -= alpha * (layer_1.T.dot(layer_2_delta))
        synapse_0 -= alpha * (layer_0.T.dot(layer_1_delta))

### more

alphas = [0.001, 0.01, 0.1, 1, 10, 100, 1000]


# compute sigmoid nonlinearity
def sigmoid(x):
    output = 1 / (1 + np.exp(-x))
    return output


# convert output of sigmoid function to its derivative
def sigmoid_output_to_derivative(output):
    return output * (1 - output)


X = np.array([[0, 0, 1],
              [0, 1, 1],
              [1, 0, 1],
              [1, 1, 1]])

y = np.array([[0],
              [1],
              [1],
              [0]])

for alpha in alphas:
    print("\nTraining With Alpha:" + str(alpha))
    np.random.seed(1)

    # randomly initialize our weights with mean 0
    synapse_0 = 2 * np.random.random((3, 4)) - 1
    synapse_1 = 2 * np.random.random((4, 1)) - 1

    prev_synapse_0_weight_update = np.zeros_like(synapse_0)
    prev_synapse_1_weight_update = np.zeros_like(synapse_1)

    synapse_0_direction_count = np.zeros_like(synapse_0)
    synapse_1_direction_count = np.zeros_like(synapse_1)

    for j in xrange(60000):

        # Feed forward through layers 0, 1, and 2
        layer_0 = X
        layer_1 = sigmoid(np.dot(layer_0, synapse_0))
        layer_2 = sigmoid(np.dot(layer_1, synapse_1))

        # how much did we miss the target value?
        layer_2_error = y - layer_2

        if (j % 10000) == 0:
            print("Error:" + str(np.mean(np.abs(layer_2_error))))

        # in what direction is the target value?
        # were we really sure? if so, don't change too much.
        layer_2_delta = layer_2_error * sigmoid_output_to_derivative(layer_2)

        # how much did each l1 value contribute to the l2 error (according to the weights)?
        layer_1_error = layer_2_delta.dot(synapse_1.T)

        # in what direction is the target l1?
        # were we really sure? if so, don't change too much.
        layer_1_delta = layer_1_error * sigmoid_output_to_derivative(layer_1)

        synapse_1_weight_update = (layer_1.T.dot(layer_2_delta))
        synapse_0_weight_update = (layer_0.T.dot(layer_1_delta))

        if (j > 0):
            synapse_0_direction_count += np.abs(
                ((synapse_0_weight_update > 0) + 0) - ((prev_synapse_0_weight_update > 0) + 0))
            synapse_1_direction_count += np.abs(
                ((synapse_1_weight_update > 0) + 0) - ((prev_synapse_1_weight_update > 0) + 0))

        synapse_1 += alpha * synapse_1_weight_update
        synapse_0 += alpha * synapse_0_weight_update

        prev_synapse_0_weight_update = synapse_0_weight_update
        prev_synapse_1_weight_update = synapse_1_weight_update

    print("Synapse 0")
    print(synapse_0)

    print("Synapse 0 Update Direction Changes")
    print(synapse_0_direction_count)

    print("Synapse 1")
    print(synapse_1)

    print("Synapse 1 Update Direction Changes")
    print(synapse_1_direction_count)

### improvement 2


alphas = [0.001, 0.01, 0.1, 1, 10, 100, 1000]
hiddenSize = 32


# compute sigmoid nonlinearity
def sigmoid(x):
    output = 1 / (1 + np.exp(-x))
    return output


# convert output of sigmoid function to its derivative
def sigmoid_output_to_derivative(output):
    return output * (1 - output)


X = np.array([[0, 0, 1],
              [0, 1, 1],
              [1, 0, 1],
              [1, 1, 1]])

y = np.array([[0],
              [1],
              [1],
              [0]])

for alpha in alphas:
    print("\nTraining With Alpha:" + str(alpha))
    np.random.seed(1)

    # randomly initialize our weights with mean 0
    synapse_0 = 2 * np.random.random((3, hiddenSize)) - 1
    synapse_1 = 2 * np.random.random((hiddenSize, 1)) - 1

    for j in xrange(60000):

        # Feed forward through layers 0, 1, and 2
        layer_0 = X
        layer_1 = sigmoid(np.dot(layer_0, synapse_0))
        layer_2 = sigmoid(np.dot(layer_1, synapse_1))

        # how much did we miss the target value?
        layer_2_error = layer_2 - y

        if (j % 10000) == 0:
            print("Error after " + str(j) + " iterations:" + str(np.mean(np.abs(layer_2_error))))

        # in what direction is the target value?
        # were we really sure? if so, don't change too much.
        layer_2_delta = layer_2_error * sigmoid_output_to_derivative(layer_2)

        # how much did each l1 value contribute to the l2 error (according to the weights)?
        layer_1_error = layer_2_delta.dot(synapse_1.T)

        # in what direction is the target l1?
        # were we really sure? if so, don't change too much.
        layer_1_delta = layer_1_error * sigmoid_output_to_derivative(layer_1)

        synapse_1 -= alpha * (layer_1.T.dot(layer_2_delta))
        synapse_0 -= alpha * (layer_0.T.dot(layer_1_delta))


# RECURRENT NEURAL NETWORK
# https://iamtrask.github.io/2015/11/15/anyone-can-code-lstm/

import copy
import numpy as np

np.random.seed(0)


# compute sigmoid nonlinearity
def sigmoid(x):
    output = 1 / (1 + np.exp(-x))
    return output


# convert output of sigmoid function to its derivative
def sigmoid_output_to_derivative(output):
    return output * (1 - output)


# training dataset generation
int2binary = {}
binary_dim = 8

largest_number = pow(2, binary_dim)
binary = np.unpackbits(
    np.array([range(largest_number)], dtype=np.uint8).T, axis=1)
for i in range(largest_number):
    int2binary[i] = binary[i]

# input variables
alpha = 0.1
input_dim = 2
hidden_dim = 16
output_dim = 1

# initialize neural network weights
synapse_0 = 2 * np.random.random((input_dim, hidden_dim)) - 1
synapse_1 = 2 * np.random.random((hidden_dim, output_dim)) - 1
synapse_h = 2 * np.random.random((hidden_dim, hidden_dim)) - 1

synapse_0_update = np.zeros_like(synapse_0)
synapse_1_update = np.zeros_like(synapse_1)
synapse_h_update = np.zeros_like(synapse_h)

# training logic
for j in range(10000):

    # generate a simple addition problem (a + b = c)
    a_int = np.random.randint(largest_number / 2)  # int version
    a = int2binary[a_int]  # binary encoding

    b_int = np.random.randint(largest_number / 2)  # int version
    b = int2binary[b_int]  # binary encoding

    # true answer
    c_int = a_int + b_int
    c = int2binary[c_int]

    # where we'll store our best guess (binary encoded)
    d = np.zeros_like(c)

    overallError = 0

    layer_2_deltas = list()
    layer_1_values = list()
    layer_1_values.append(np.zeros(hidden_dim))

    # moving along the positions in the binary encoding
    for position in range(binary_dim):
        # generate input and output
        X = np.array([[a[binary_dim - position - 1], b[binary_dim - position - 1]]])
        y = np.array([[c[binary_dim - position - 1]]]).T

        # hidden layer (input ~+ prev_hidden)
        layer_1 = sigmoid(np.dot(X, synapse_0) + np.dot(layer_1_values[-1], synapse_h))

        # output layer (new binary representation)
        layer_2 = sigmoid(np.dot(layer_1, synapse_1))

        # did we miss?... if so, by how much?
        layer_2_error = y - layer_2
        layer_2_deltas.append((layer_2_error) * sigmoid_output_to_derivative(layer_2))
        overallError += np.abs(layer_2_error[0])

        # decode estimate so we can print it out
        d[binary_dim - position - 1] = np.round(layer_2[0][0])

        # store hidden layer so we can use it in the next timestep
        layer_1_values.append(copy.deepcopy(layer_1))

    future_layer_1_delta = np.zeros(hidden_dim)

    for position in range(binary_dim):
        X = np.array([[a[position], b[position]]])
        layer_1 = layer_1_values[-position - 1]
        prev_layer_1 = layer_1_values[-position - 2]

        # error at output layer
        layer_2_delta = layer_2_deltas[-position - 1]
        # error at hidden layer
        layer_1_delta = (future_layer_1_delta.dot(synapse_h.T) + layer_2_delta.dot(
            synapse_1.T)) * sigmoid_output_to_derivative(layer_1)

        # let's update all our weights so we can try again
        synapse_1_update += np.atleast_2d(layer_1).T.dot(layer_2_delta)
        synapse_h_update += np.atleast_2d(prev_layer_1).T.dot(layer_1_delta)
        synapse_0_update += X.T.dot(layer_1_delta)

        future_layer_1_delta = layer_1_delta

    synapse_0 += synapse_0_update * alpha
    synapse_1 += synapse_1_update * alpha
    synapse_h += synapse_h_update * alpha

    synapse_0_update *= 0
    synapse_1_update *= 0
    synapse_h_update *= 0

    # print out progress
    if (j % 1000 == 0):
        print("Error:" + str(overallError))
        print("Pred:" + str(d))
        print("True:" + str(c))
        out = 0
        for index, x in enumerate(reversed(d)):
            out += x * pow(2, index)
        print(str(a_int) + " + " + str(b_int) + " = " + str(out))
        print("------------")


### DROPOUT FUNCTION
# https://iamtrask.github.io/2015/07/28/dropout/

import numpy as np

X = np.array([[0, 0, 1], [0, 1, 1], [1, 0, 1], [1, 1, 1]])
y = np.array([[0, 1, 1, 0]]).T
alpha, hidden_dim, dropout_percent, do_dropout = (0.5, 4, 0.2, True)
synapse_0 = 2 * np.random.random((3, hidden_dim)) - 1
synapse_1 = 2 * np.random.random((hidden_dim, 1)) - 1
for j in xrange(60000):
    layer_1 = (1 / (1 + np.exp(-(np.dot(X, synapse_0)))))
    if (do_dropout):
        layer_1 *= np.random.binomial([np.ones((len(X), hidden_dim))], 1 - dropout_percent)[0] * (
        1.0 / (1 - dropout_percent))
    layer_2 = 1 / (1 + np.exp(-(np.dot(layer_1, synapse_1))))
    layer_2_delta = (layer_2 - y) * (layer_2 * (1 - layer_2))
    layer_1_delta = layer_2_delta.dot(synapse_1.T) * (layer_1 * (1 - layer_1))
    synapse_1 -= (alpha * layer_1.T.dot(layer_2_delta))
    synapse_0 -= (alpha * X.T.dot(layer_1_delta))
