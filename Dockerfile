FROM pytorch/torchserve
USER root
RUN chmod 777 -R .

RUN python -m pip install --upgrade pip

COPY ./mini.mar model_store/
COPY ./config.properties /config.properties

# CMD ["torchserve", "--start" ,"--model-store", "model_store" ,"--models" ,"mini=mini.mar"]