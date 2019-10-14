PWD=$(pwd)
sudo su - <<EOC
source ~/venvs/tensorflow/bin/activate
export LD_LIBRARY_PATH=/usr/local/cuda-10.1/lib64:$LD_LIBRARY_PATH
python $PWD/check_keras.py
EOC

