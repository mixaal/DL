# Deep Learning Setup


## Basic Setup

The following combination is supported:
 * tensorflow-gpu 2.0.0
 * cuda-10.1.168
 * libcudnn 7.6.4

Create you instances in cloud, the name will be the one which must reside in `/etc/hosts` file. Add public IP address to your /etc/hosts file:

```
<first ip>     mixaal-gpu-1
<second ip>     mixaal-gpu-2
...
```

Make sure you have all your gpu instances listed in `hosts` file:
```
mixaal-gpu-1 slots=1
mixaal-gpu-2 slots=1
...
```

Number of slots denotes the number of GPU in your VMs. Make sure to distribute the ssh keys on root between all nodes.

Now download libcudnn from nvidia, make sure you obey the license:
https://docs.nvidia.com/deeplearning/sdk/cudnn-sla/index.html

Here is the download link (you must be in nvidia free developer program):
https://developer.nvidia.com/compute/machine-learning/cudnn/secure/7.6.4.38/Production/10.1_20190923/cudnn-10.1-linux-x64-v7.6.4.38.tgz

Upload the library on all nodes and install it:
```
sudo su -
tar xzvf cudnn-10.1-linux-x64-v7.6.4.38.tgz 
cp cuda/lib64/libcudnn* /usr/local/cuda-10.1/lib64/
cp cuda/include/cudnn.h /usr/local/cuda-10.1/include/
```

From now on, the GPU is fully utiized:

```
sudo su -
./runenv.sh keras_mnist_cnn.py
```

## Running with Horovod

Now copy the `keras_mnist_horovod.py` to all nodes. Create the following file on each node (wrapper):
```
cat /root/run_horovod.sh
PWD=$(pwd)

set -x
sudo su - <<EOC
source ~/venvs/tensorflow/bin/activate
export LD_LIBRARY_PATH=/usr/local/cuda-10.1/lib64:$LD_LIBRARY_PATHA
python keras_mnist_horovod.py
EOC
```

Run horovod:
```
time horovodrun -np 2 -H mixaal-gpu-2:1,mixaal-gpu-1:1 bash -c /root/run_horovod.sh
```

## Jupiter Notebook Service

Run jupyter:
```
nohup jupyter notebook --allow-root --ip 127.0.0.1 &
```

From your desktop:
```
ssh -o ServerAliveInterval=240 -L 8888:localhost:8888 root@mixaal-gpu-1
```

Now you can access the notebook via the URL you see in the jupyter console.

## Jupyter Notebooks

The following notebooks are pre-installed:

* Africa Crisis: The one from kaggle.com shows `seaborn` and `matplotlib.pyplot` in action
* Keras ML Demo: MNIST dataset running on GPU and libcudnn-7.6.4
* ImageNet: Pre-trained VGG16 architecture running on GPU, activation layers shown
* Mandelbrot: using `IPython.parallel` to execute Mandelbrot's fractal computation in parallel
