# Deep Learning Setup

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

Number of slots denotes the number of GPU in your VMs.


```
# Oracle 7.7 GPU support
#https://blogs.oracle.com/wim/using-a-baremetal-gpu-shape-in-oracle-cloud-infrastructure-with-oracle-linux-7-and-tensorflow
nvidia-smi # show info on NVIDIA Tesla GPU (i.e are we on correct image?)
sudo yum -y install python-pip python-devel atlas atlas-devel gcc-gfortran openssl-devel libffi-devel
pip install --upgrade pip
pip install --upgrade virtualenv
virtualenv --system-site-packages ~/venvs/tensorflow
source ~/venvs/tensorflow/bin/activate
pip install --upgrade tensorflow-gpu
yum install -y cuda-10-1
pip install keras
```


```
# Verify that TF is using gpu
from tensorflow.python.client import device_lib
print(device_lib.list_local_devices())
```


```
# Fix keras loadlib issue
cd /usr/local/cuda-10.1/lib64
for lib in $(ls *10.1* | sed -e 's/.10.1.*//g' | uniq); do ln -s "$lib" "$lib.10.0" ; done
 ln -s /usr/lib64/libcublas.so.10 /usr/lib64/libcublas.so.10.0
export LD_LIBRARY_PATH=/usr/local/cuda-10.1/lib64:$LD_LIBRARY_PATH
```

```
# Verify that you see GPU in Keras:
#
from keras import backend as K
K.tensorflow_backend._get_available_gpus()
```
