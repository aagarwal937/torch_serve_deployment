# pull the latest torchserv image built assuming GPU support
FROM pytorch/torchserve:latest-gpu as base

# change user and change permissions
USER root
RUN chmod 777 -R .

# install python dependencies
RUN pip3 install sentence-transformers

# copy the config file into WORKDIR
COPY ./config.properties /home/model-server/config.properties

# start the server
CMD ["torchserve", "--start", "--ts-config", "/home/model-server/config.properties"]