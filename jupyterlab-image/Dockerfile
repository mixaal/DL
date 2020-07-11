FROM oraclelinux:8
RUN yum install -y gcc gcc-c++ python3 vim tree python3-pip-wheel net-tools python3-devel atlas atlas-devel gcc-gfortran openssl-devel libffi-devel zip unzip cmake pkg-config automake openblas make lapack libtool

RUN curl -kv https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3 ./get-pip.py
RUN pip install --upgrade tensorflow-gpu
RUN pip install keras
RUN pip install keras_datasets
RUN pip install jupyterlab
RUN pip install jupyter
RUN pip install matplotlib
RUN pip install pandas
RUN pip install geopandas
RUN pip install descartes
RUN pip install mplleaflet
RUN pip install seaborn
RUN pip install oci
RUN pip install oci-cli
RUN pip install ipyparallel
RUN pip install pillow
RUN pip install sklearn
RUN pip install line_profiler
RUN pip install snakeviz
RUN pip install jupyterthemes
RUN pip install ipywidgets
RUN pip install pymysql
RUN jupyter nbextension enable --py widgetsnbextension
RUN jt -t chesterish -T -N -kl # Dark theme, kernel log, name and toolbar on
#ipcluster nbextension enable
RUN pip install tensorflow_datasets
RUN mkdir -p /root/.ipython/profile_default/startup
ADD startup.ipy  /root/.ipython/profile_default/startup

ADD install-eigen /root
ADD install-opencv4 /root
ADD get-opencv4 /root
ADD install-glog /root
RUN /root/install-eigen
RUN /root/install-glog
RUN /root/get-opencv4
RUN /root/install-opencv4

RUN mkdir /jupyter_root
RUN mkdir /jupyter_root/images
RUN mkdir /jupyter_root/examples
RUN mkdir /jupyter_root/datasets
RUN mkdir /jupyter_root/weights
RUN mkdir /jupyter_root/models
ADD run-notebook.sh /root

ADD images/*jpg /jupyter_root/images/
ADD examples/*ipynb /jupyter_root/examples/
ADD datasets/*csv /jupyter_root/datasets/
ADD models/* /jupyter_root/models/
#ADD weights/*hdf5 /jupyter_root/weights/

RUN ipcluster nbextension enable

RUN pip install line_profiler
RUN pip install py-heat-magic

RUN yum remove -y gcc gcc-c++ gcc-gfortran openssl-devel libffi-devel cmake make libtool
RUN rm -rf /root/opencv* /root/.cache/pip/http/* /root/eigen* /root/glog-master/

#COPY index.css usr/local/lib/python3.6/site-packages/jupyterlab/themes/\@jupyterlab/theme-dark-extension/index.css 
#RUN yum install -y nodejs npm
#RUN jupyter lab build

ENTRYPOINT /root/run-notebook.sh

EXPOSE 8888 8889 8080
