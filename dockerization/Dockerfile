# pull the latest torchserve docker image
FROM pytorch/torchserve

# setting workdir in the container
WORKDIR /torchserve_local

# change user and change permissions
USER root
RUN chmod 777 -R .

# copy the requirements file to WORKID
COPY ./requirements.txt /torchserve_local/requirements.txt

# install the requirements
RUN pip install -r requirements.txt

# copy the config file into WORKDIR
COPY ./config.properties /torchserve_local/

#copy the .mar file created in previous step
COPY ./bert.mar /torchserve_local/model_store/

# start the server
CMD ["torchserve", "--start", "--ts-config", "/torchserve_local/config.properties"]