PWD=$(pwd)

COMMAND="$@"
sudo su - <<EOC
source ~/venvs/tensorflow/bin/activate
export LD_LIBRARY_PATH=/usr/local/cuda-10.1/lib64:$LD_LIBRARY_PATHA
python "$COMMAND"
EOC

