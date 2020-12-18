#!/bin/bash -xe


if [ "$SET_THEME" != "" ] ; then
   jt -t "$SET_THEME" -T -N -kl 
fi

export PYTHONPATH=/usr/local/python/

nohup ipcluster start &

#Enable this one if you need Net2Viz
#cd /backend
#nohup python3 ./server.py &

cd /jupyter_root
nohup jupyter notebook --allow-root --ip 0.0.0.0 --no-browser --port 8888 &
nohup jupyter lab --ip 0.0.0.0 --no-browser --allow-root --port 8889
