#!/bin/bash -xe


if [ "$SET_THEME" != "" ] ; then
   jt -t "$SET_THEME" -T -N -kl 
fi

export PYTHONPATH=/usr/local/python/

#nohup ipcluster start &

cd /root
nohup /root/.oci/trollbox-linux-amd64 &

cd /jupyter_root
nohup jupyter notebook --allow-root --ip 0.0.0.0 --no-browser --port 8888 
#nohup jupyter lab --ip 0.0.0.0 --no-browser --allow-root --port 8889
