# -*- coding: utf-8 -*-
"""classification_dog_and_cat_cnn.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16rZUOPWJ_j4Q5aZh7l3kQx9tdcg0IYgw
"""

# Code to read csv file into Colaboratory:


ls ./cat_and_dog/training_set/training_set/

import cv2
import os
import pandas as pd
import numpy as np

import os
folders=os.listdir('./cat_and_dog/training_set/training_set/')
print(folders)
imgs=[]
labels=[]
for folder in folders:
  files=os.listdir('./cat_and_dog/training_set/training_set/'+folder)
  for file in files:
    img=cv2.imread('./cat_and_dog/training_set/training_set/'+folder+'/'+file)
    if img is None:
      print('./cat_and_dog/training_set/training_set/'+folder+'/'+file)
      continue
    imgs.append(cv2.resize(img,(200,200)))
    if 'dog' in file:
      labels.append(0)
    else:
      labels.append(1)

imgs=np.array(imgs)
labels=np.array(labels)

imgs.shape

labels.shape

import tensorflow as tf
import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test=train_test_split(imgs,labels,test_size=0.2, random_state=42)

print(type(X_train))
X_train.shape

print(type(y_train))
y_train.shape
y_train[15]

num_classes = 2

x_placeholder = tf.placeholder(tf.float32,[None,200,200,3])
y_placeholder = tf.placeholder(tf.int32,[None])

conv1 = tf.layers.conv2d(x_placeholder,32,5,activation=tf.nn.relu,padding="SAME")
conv1 = tf.layers.max_pooling2d(conv1, 2, 2,padding="SAME") # pooling layer 1
conv2 = tf.layers.conv2d(conv1, 64, 5, activation=tf.nn.relu,padding="SAME") # convolutional layer 2
conv2 = tf.layers.max_pooling2d(conv2, 2, 2,padding="SAME") # pooling layer 2

fc1 = tf.contrib.layers.flatten(conv2)
fc1 = tf.layers.dense(fc1,512,activation=tf.nn.relu) # anh nghi la do em cho to qua nen no lau,e  ngh=i= >do  dung it lan convulotion dung rui, cho tam 4,5 lop conv vao,oki.,nhung ma thay loss cũng da ukm, giảm, nhung minh co the cho no nhanh len cx dc ma em nao
out = tf.layers.dense(fc1, num_classes)

batch_size = 128
def random_batch(x_train,y_train,batch_size):
  rnd_indices = np.random.randint(0,len(x_train),batch_size) 
  x_batch = x_train[rnd_indices]
  y_batch = y_train[rnd_indices]
  return x_batch,y_batch

pred = out
print(tf.shape(pred))
print(tf.shape(y_placeholder))
xentropy = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=pred, labels=y_placeholder)
cost = tf.reduce_mean(xentropy)
optimizer = tf.train.AdamOptimizer()
training_op=optimizer.minimize(cost)

correct = tf.nn.in_top_k(pred, y_placeholder, 1)
accuracy = tf.reduce_mean(tf.cast(correct, tf.float32))
# Initializing the variables
init = tf.global_variables_initializer()

num_steps = 500
sess= tf.Session()
best_accuracy = 0
consecutive_accuracy = []
n_epochs = 50

sess.run(init)
for step in range(1, num_steps+1):
    x_batch, y_batch = random_batch(X_test, y_test, batch_size)
    sess.run(training_op, feed_dict={C})
    if step % 10 == 0:
        acc = sess.run( accuracy, feed_dict={x_placeholder: x_batch,y_placeholder: y_batch})
        print('Step:',step, ', Accuracy:',acc)
print("Optimization Finished!")

