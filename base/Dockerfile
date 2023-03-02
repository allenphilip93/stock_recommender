FROM apache/airflow:latest

# USER root
# RUN apt-get -y update \
#     && apt-get -y install npm \
#     && npm install -g elasticdump
USER ${AIRFLOW_UID}

RUN pip install pendulum
RUN pip install pandas
RUN pip install yfinance
RUN pip install psycopg2-binary
# https://github.com/altaurog/pgcopy/issues/18
# RUN pip install pgcopy

# RUN pip install "apache-airflow[crypto]"
# RUN pip install sklearn
# RUN pip install networkx
# RUN pip install ordered_set
# RUN pip install pyvis
# RUN pip install colormath
# RUN pip install azure-storage-blob==12.9.0
# RUN pip install pwlf==2.2.1
# RUN pip install scipy
# RUN pip install xgboost
# RUN pip install boto3==1.24.43
# RUN pip install requests_aws4auth
# RUN pip install lightgbm
# RUN pip install sagemaker

# ARG CACHEBUST
# COPY ./cmplib-2.1.0-py3-none-any.whl .
# RUN pip uninstall --yes ./cmplib-1.0-py3-none-any.whl
# RUN pip install ./cmplib-2.1.0-py3-none-any.whl --force-reinstall

# RUN pip install dask[complete]
# RUN pip install jupyter
# RUN pip install jupyter-server-proxy
# RUN jupyter nbextension enable --py widgetsnbextension
# RUN pip install jupyterlab && jupyter serverextension enable --py jupyterlab
# RUN pip install mlflow
# RUN pip install tensorflow
# RUN pip install tqdm
# RUN pip install mlxtend
# RUN pip install xgboost
# RUN pip install rrcf
# RUN pip install markupsafe==2.0.1
# RUN pip install psycopg2
# RUN pip install cython
# RUN pip install SQLAlchemy==1.3.23
# RUN pip install flask_oauthlib>=0.9
# RUN pip install wtforms
# RUN pip install lz4
# RUN pip install numpy>=1.15.1
# RUN pip install pandas>=0.25.0
# RUN pip install scipy
# RUN pip install pyarrow>=0.14.0
# RUN pip install matplotlib
# RUN pip install cloudpickle>=0.2.2
# RUN pip install blosc
# RUN pip install cytoolz
# RUN pip install ipywidgets

# RUN apt-get -y update \
#     && apt-get -y install npm \
#     && npm install -g elasticdump

