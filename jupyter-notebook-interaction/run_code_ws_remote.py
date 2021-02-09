'''
Entry point module to start the interactive console.
'''
import json
import requests
import datetime
import uuid
import os
from pprint import pprint
from threading import Thread
#pip3 install websocket_client !!! not webscoket!
from websocket import create_connection
import base64
from PIL import Image
import tempfile

def get_img_name():
    return tempfile.gettempdir()+"/"+uuid.uuid1().hex+".png"

def logme(message):
    print(message)
    text_file = open("/tmp/pycharm-jupyter-exec.log", "a")
    text_file.write("\n"+message)
    text_file.close()

def save_to_file(filename, data):
    file = open(filename, "wb")
    file.write(data)
    file.close()

def show_image(img_base64_data):
    global idx
    img_binary_data = base64.b64decode(img_base64_data)
    img_name = get_img_name()
    save_to_file(img_name, img_binary_data)
    s=os.popen("eog "+img_name)

def create_json(code_fragment):
    textcode=json.dumps(code_fragment.splitlines(True))

    return '''
    {
  "name": "IntelliJStatementExecution.ipynb",
  "path": "IntelliJStatementExecution.ipynb",
  "type": "notebook",
  "format": "json",
  "content": {
    "nbformat": 4,
    "nbformat_minor": 2,
    "metadata": {
      "kernelspec": {
        "display_name": "Python 3",
        "name": "python3",
        "language": "python"
      },
      "language_info": {
        "mimetype": "text/x-python",
        "nbconvert_exporter": "python",
        "version": "3.8.2",
        "name": "python",
        "file_extension": ".py",
        "pygments_lexer": "ipython2",
        "codemirror_mode": {
          "version": 2,
          "name": "ipython"
        }
      }
    },
    "cells": [
      {
        "cell_type": "code",
        "execution_count": 0,
        "source": '''+textcode+''',
        "outputs": [],
	"metadata": {
          "trusted": true
        }
      }
     ]
   }
}
'''

def send_execute_request(msg_id, code):
    msg_type = 'execute_request';
    content = { 'code' : code, 'silent':False }
    hdr = { 'msg_id' : msg_id, 
        'username': 'test', 
        'session': uuid.uuid1().hex, 
        'data': datetime.datetime.now().isoformat(),
        'msg_type': msg_type,
        'version' : '5.0' }
    msg = { 'header': hdr, 'parent_header': hdr, 
        'metadata': {},
        'content': content }
    return msg

def run_notebook(hostport, token):
    notebook_path = '/IntelliJStatementExecution.ipynb'
    base = "http://"+hostport
    headers = {'Authorization': 'Token '+token}

    url = base + '/api/kernels'
    response = requests.post(url,headers=headers)
    kernel = json.loads(response.text)

    # Load the notebook and get the code of each cell
    url = base + '/api/contents' + notebook_path
    response = requests.get(url,headers=headers)
    file = json.loads(response.text)
    code = [ c['source'] for c in file['content']['cells'] if len(c['source'])>0 ]

    # Execution request/reply is done on websockets channels
    ws = create_connection("ws://"+hostport+"/api/kernels/"+kernel["id"]+"/channels", header=headers)
    for c in code:
        logme("sending snippet:"+str(c))
        msg_id = uuid.uuid1().hex
        ws.send(json.dumps(send_execute_request(msg_id, c)))

        # We ignore all the other messages, we just get the code execution output
        # (this needs to be improved for production to take into account errors, large cell output, images, etc.)
        logme("len: "+str(len(code)))
        for i in range(0, len(code)):
            while True:
                rsp = json.loads(ws.recv())
                msg_type = rsp["msg_type"]
                logme("msg_type:"+msg_type)
                #logme(str(rsp))
                parent_msg_id = rsp["parent_header"]["msg_id"]
                if msg_type == "execute_input":
                    logme("<<< " + rsp["content"]["code"])
                if msg_type == "status" and rsp["content"]["execution_state"] == "idle":
                    break
                if msg_type == "stream" and parent_msg_id == msg_id:
                    logme(">>> " + rsp["content"]["text"])
                    #break
                if msg_type == "display_data":
                    #logme(str(rsp))
                    logme(">>> " + rsp["content"]["data"]["text/plain"])
                    try:
                        show_image(rsp["content"]["data"]["image/png"])
                    except KeyError:
                        pass
                if msg_type == "execute_result" and parent_msg_id == msg_id:
                    #logme(str(rsp))
                    logme(">>> " + rsp["content"]["data"]["text/plain"])
                    #break

        ws.close()

def send_to_notebook(hostport, token, body):
    headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
    baseuri = "http://"+hostport
    logme("baseuri:"+baseuri)
    logme("token  :"+token)
    logme("body   :"+body)
    return requests.put(baseuri+'/api/contents/IntelliJStatementExecution.ipynb?token='+token, data=create_json(body), headers=headers)

#=======================================================================================================================
# main
#=======================================================================================================================
if __name__ == '__main__':
    code = """
import keras
import matplotlib.pyplot as plt
plt.plot([1, 2, 3, 4])
plt.ylabel('some numbers')
plt.show()
"""

    code = """
from __future__ import print_function
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K

batch_size = 128
num_classes = 10
epochs = 6

# input image dimensions
img_rows, img_cols = 28, 28

# the data, split between train and test sets
(x_train, y_train), (x_test, y_test) = mnist.load_data()

if K.image_data_format() == 'channels_first':
    x_train = x_train.reshape(x_train.shape[0], 1, img_rows, img_cols)
    x_test = x_test.reshape(x_test.shape[0], 1, img_rows, img_cols)
    input_shape = (1, img_rows, img_cols)
else:
    x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
    x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
    input_shape = (img_rows, img_cols, 1)

x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255
print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

# convert class vectors to binary class matrices
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=input_shape))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax'))

model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adadelta(),
              metrics=['accuracy'])
              
history = model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_data=(x_test, y_test))
score = model.evaluate(x_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

import matplotlib.pyplot as plt

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(1, len(acc)+1)

plt.plot(epochs, acc, 'bo', label='Training accuracy')
plt.plot(epochs, val_acc, 'b', label='Validation accuracy')
plt.title("Training and Validation Accuracy")
plt.legend()
plt.figure()

plt.plot(epochs, loss, 'bo', label='Training loss')
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title("Training and Validation Loss")
plt.legend()
plt.figure()
"""
    token = os.environ["JUPYTER_TOKEN"]
    send_to_notebook("localhost:8888", token, code)
    run_notebook("localhost:8888", token)
