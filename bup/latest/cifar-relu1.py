import theano
import theano.tensor as T
import sys
import numpy

def ReLU(z): return T.maximum(0.0, z)

from NN.NN import NNet
from NN.Layers.FullyConnected import FullyConnectedLayer
from NN.Layers.Convolutional import ConvolutionalLayer
from NN.Layers.Pooling import PoolingLayer
from NN.Layers.Softmax import SoftmaxLayer
from NN.CifarLoader import load_data

# CONFIG
try: theano.config.device = 'gpu'
except: pass
theano.config.floatX = 'float32'
numpy.random.seed(0)

# HYPER PARAMETERS
mini_batch_size = 100
epochs = 60
learning_rate = 0.001

net = NNet([ConvolutionalLayer(image_shape=(mini_batch_size, 3, 32, 32),
                      filter_shape=(32, 3, 5, 5), activation_fn=ReLU),
            PoolingLayer(image_shape=(mini_batch_size,32, 28, 28),
                        poolsize=(2,2)),
            ConvolutionalLayer(image_shape=(mini_batch_size, 32, 14, 14),
                      filter_shape=(64, 32, 5, 5), activation_fn=ReLU),
            PoolingLayer(image_shape=(mini_batch_size,64, 10, 10),
                        poolsize=(2,2)),
            # ConvolutionalLayer(image_shape=(mini_batch_size, 64, 5, 5),
            #           filter_shape=(64, 64, 5, 5), activation_fn=ReLU),
            FullyConnectedLayer(n_in=64*5*5, n_out=1000, activation_fn=ReLU),
            SoftmaxLayer(n_in=1000, n_out=10)],
            mini_batch_size)

training_data, validation_data, test_data = load_data()

net.train(training_data, epochs, mini_batch_size, learning_rate,
            validation_data, test_data, lmbda=0.1)
