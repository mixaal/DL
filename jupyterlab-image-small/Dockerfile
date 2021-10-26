FROM oraclelinux:8
#RUN yum install -y gcc gcc-c++ python3 vim tree python3-pip-wheel net-tools python3-devel atlas atlas-devel gcc-gfortran openssl-devel libffi-devel zip unzip cmake pkg-config automake openblas make lapack libtool
RUN yum install -y python3 vim tree python3-pip-wheel net-tools python3-devel zip unzip

RUN curl -kv https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3 ./get-pip.py
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
RUN pip install pillow
RUN pip install sklearn
RUN pip install line_profiler
RUN pip install snakeviz
RUN pip install jupyterthemes
RUN pip install ipywidgets
RUN pip install xgboost
RUN jupyter nbextension enable --py widgetsnbextension
RUN jt -t chesterish -T -N -kl # Dark theme, kernel log, name and toolbar on
RUN mkdir -p /root/.ipython/profile_default/startup
ADD startup.ipy  /root/.ipython/profile_default/startup

RUN mkdir /jupyter_root
RUN mkdir /jupyter_root/images
RUN mkdir /jupyter_root/examples
RUN mkdir /jupyter_root/datasets
RUN mkdir /jupyter_root/weights
RUN mkdir /jupyter_root/models

RUN pip install line_profiler
RUN pip install py-heat-magic

RUN rm -rf /root/opencv* /root/.cache/pip/http/* /root/eigen* /root/glog-master/

RUN mkdir -p /root/.oci/
ADD execute-notebook.sh /root
RUN curl -kv -L "https://github.com/mixaal/trollbox/blob/main/build/trollbox-linux-amd64?raw=true" -o /root/.oci/trollbox-linux-amd64 
RUN chmod +x /root/.oci/trollbox-linux-amd64
RUN chmod +x /root/execute-notebook.sh

RUN pip install nbconvert

ENTRYPOINT /root/execute-notebook.sh

EXPOSE 8888
