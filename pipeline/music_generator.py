import pandas as pd
import numpy as np
import re
import random
import sys
import time
import json

import prepare as p

from keras import layers
from keras.models import Sequential
from keras import optimizers
from keras.models import load_model
import tensorflow as tf

num_vals = 14 # we use 0 to 13
def vectorizing_seq (text, maxlen, step):    
    """
    :param maxlen: the length of a sequence to extract as train
    :type  maxlen: int
    :param step: sample a new sequence every n steps
    :type  step: int
    :returns: (Numpy boolean array of shape 
                    (Number of sequences, maxlen, number of distinct character),
               Numpy boolean array of shape 
                    (Number of sequences, number of distinct character),
               dictionary mapping a character to its integer placeholder)
    :rtype:   (numpy.ndarray, 
               numpy.ndarray, 
               dict)     
    """
    sentences = [] # hold extracted sequences
    next_chars = [] # hold next characters for each corresponding sentence

    for i in range(0, len(text) - maxlen, step):
        sentences.append(text[i: i + maxlen])
        next_chars.append(text[i + maxlen])

    print('Number of sequences:', len(sentences))
    print('Vectorization on ({}, {}, {}) dims...'.format(len(sentences), maxlen, num_vals)) 
    #POL WHAT THE FUCK IS THIS ABOVE LINE??? WHY WOULD YOU PUT A PARAMETER OUTSIDE OF THE FUNCTION
    #ARGUMENTS HERE
    
    # one hot encoding the characters into binary arrays
    x = np.zeros((len(sentences), maxlen, num_vals), dtype=np.bool)
    y = np.zeros((len(sentences), num_vals), dtype=np.bool)
    for i, sentence in enumerate(sentences):
        for t, val in enumerate(sentence):
            x[i, t, val] = 1
        y[i, next_chars[i]] = 1
        
    return x, y

def create_model(x, y, maxlen, epochs):
    """
    Creates and trains a model.
    :param x: Numpy boolean array of shape 
                    (Number of sequences, maxlen, number of distinct character)
    :type  x: numpy.ndarray
    :param y: Numpy boolean array of shape 
                    (Number of sequences, number of distinct character)
    :type  y: numpy.ndarray
    :param maxlen: the length of a sequence to extract as train
    :type  maxlen: int
    :param epochs: number of training iterations
    :type  epochs: int
    :param chars: list of unique characters
    :type  chars: list
    :returns: trained keras model
    :rtype:   keras.engine.sequential.Sequential
    """

#     model = Sequential()
#     model.add(layers.GRU(
#         32,
#         return_sequences=True,
#         input_shape=(maxlen, len(chars)))
#     )
#     model.add(layers.GRU(
#         64,
#         input_shape=(maxlen, len(chars)))
#     )
#     model.add(layers.Dense(
#         len(chars), 
#         activation='softmax')
#     )

    # start of my model attempt, it works decently well
    # - try commenting it out and using the previous one
    # - also try removing the Dropout layers
    # --------------------------------------------
    model = Sequential()
    model.add(layers.GRU(
        256,
        return_sequences=True,
        input_shape=(maxlen, num_vals)
    ))
    model.add(layers.Dropout(0.5))
    model.add(layers.GRU(128))
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(
        num_vals,
        activation='softmax')) #alternatively: activation = 'softmax'
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop')
    # --------------------------------------------

    print(model.summary())
    model.fit(x, y, batch_size=128, epochs=epochs)

    return (model)

def train_model_from_text(text, maxlen=6, step=12, epochs=10):
    """
    Given text, train the model.
    
    :param text: A string with all the text together.
    :type  text: str
    :param maxlen: the length of a sequence to extract as train
    :type  maxlen: int
    :param step: sample a new sequence every n steps
    :type  step: int
    :param epochs: number of training iterations
    :type  epochs: int
    :returns: (trained keras model,
               dictionary mapping characters to digit representations)
    :rtype:   (keras.engine.sequential.Sequential,
               dict)
    """
    
    x, y = vectorizing_seq(text, maxlen, step)
    model = create_model(x, y, maxlen, epochs)
    
    return model

def sample(preds, temperature=1.0):
    """
    Compute new probability distribution based on the temperature
    Higher temperature creates more randomness.
    
    :param preds: numpy array of shape (unique chars,), and elements sum to 1
    :type  preds: numpy.ndarray
    :param temperature: characterizes the entropy of probability distribution
    :type  temperature: float
    :returns: a number 0 to the length of preds - 1
    :rtype:   int
    """
    
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

#The real money generating part of this generator
def text_generate(model, text, maxlen=4, temperature=1.0, textlen=10):
    """
    Generate text based on a model.
    
    :param model: trained keras model
    :type  model: keras.engine.sequential.Sequential
    :param text: lyrics
    :type  text: str
    :param maxlen: maximum length of the sequences
    :type  maxlen: int
    :param textlen: Number of characters of generated sequence
    :type  textlen: int
    """

    start_index = random.randint(0, len(text) - maxlen - 1) 
    generated_text = text[start_index: start_index + maxlen]
    outp = generated_text
    print('--- Generating with temperature {}'.format(temperature))
    print(outp)
    
    
    for i in range(textlen):
        sampled = np.zeros((1, maxlen, num_vals))
        for t, char in enumerate(generated_text):
            #print('(t, char) = ({}, {})'.format(t, char))
            sampled[0, t, min(num_vals - 1, char)] = 1
        preds = model.predict(sampled, verbose=0)[0]
        next_char = sample(preds, temperature)
        generated_text.append(next_char)
        generated_text = generated_text[1:]
        outp.append(next_char)
    
    return outp

def text_generate_w(model, text, cutoff, maxlen=4, temperature=1.0, textlen=10):
    """
    Generate text based on a model.
    
    :param model: trained keras model
    :type  model: keras.engine.sequential.Sequential
    :param text: lyrics
    :type  text: str
    :param maxlen: maximum length of the sequences
    :type  maxlen: int
    :param textlen: Number of characters of generated sequence
    :type  textlen: int
    """

    generated_text = text
    outp = generated_text[cutoff:]
    print('--- Generating with temperature {}'.format(temperature))
    print(outp)
    
    
    for i in range(textlen):
        sampled = np.zeros((1, maxlen, num_vals))
        for t, char in enumerate(generated_text):
            #print('(t, char) = ({}, {})'.format(t, char))
            sampled[0, t, min(num_vals - 1, char)] = 1
        preds = model.predict(sampled, verbose=0)[0]
        next_char = sample(preds, temperature)
        generated_text.append(next_char)
        generated_text = generated_text[1:]
        outp.append(next_char)
    
    return outp

def splitz(seq, cut):
    group = []    
    for num in seq:
        if num != cut:
            group.append(num)
        elif group:
            yield group
            group = []

def save_model(trained_model,fname):
    trained_model.save('{}.h5'.format(fname))

def load_ml(save_fname):
    return load_model(save_fname)

# model = load_model('model.h5')

if __name__ == "__main__":
	# print(tf.test.gpu_device_name())
	config = tf.ConfigProto()
	config.gpu_options.allow_growth = True
	sess = tf.Session(config=config)

	#Processing of data
	with open('clean_dataset.json','r') as f:
	    training_data = json.loads(f.read()) #reminder that training_data is a huge ass string

	#training of data
	maxlen = 60 # train on sequences of 60 characters (about 6 chords)

	# model = train_model_from_text(
	#     training_data,
	#     maxlen=maxlen,
	#     step=6, # jump over 10 characters (~ one chord) 
	#     epochs=15
	# )
	# save_model(model,'uncommmon')

	model = load_ml('softmax.h5')
	outp = text_generate(
		    model, 
		    training_data,
		    maxlen=maxlen,
		    temperature=.9,
		    textlen=60)
	
	tempor = list(splitz(outp,12))

	for n1,x in enumerate(tempor): 
		for n2,y in enumerate(x):
			x[n2] = int(y) 

	song = p.write_song(tempor)
