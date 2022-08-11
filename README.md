# Torch Serve Deployment

TorchServe is a performant, flexible and easy to use tool for serving PyTorch eager mode and torschripted models. <br>*https://pytorch.org/serve/*

Listed below are the steps to deploy a sentence transformer model either from hugging face model hub or a custom trained model on any domain data using TorchServe.
It caters to all the requirements of deploying a model in production while providing scalability and flexibility.

# Prerequisites

1. Install Java JDK 11 <br>
    `sudo apt update` <br>
        `sudo apt install default-jre`

2. Install torchserve with its python dependencies <br>
    `pip install torchserve`

3. Install torch-model-archiver <br>
    `pip install torch-model-archiver`

# Below are the set of commands to run after installing the Prerequisites

*NOTE: Your custom model directory containing the files like pytorch_model.bin, voacb.txt and config.json should be present inside your working directory in a seperate folder*

1. Create a seperate testing environment using conda for TorchServe.

2. Then activate the environment

3. Install the pytorch dependicies using conda. You refer the command and change the version according to your system requirements.

4. Below is the link to the command from the pytorch official website <br>
    *(https://pytorch.org/)*

5. Install sentence transformers <br>
    `pip install sentence-transformers`

6. Defining a TorchServe handler for our model. Handler file is present in the repo itself you can directly use it.

7. Converting the trained checkpoint to TorchServe MAR file. <br>
    `torch-model-archiver --model-name <NAME_OF_THE_MODEL> --version 1.0 --serialized-file ./model/pytorch_model.bin --extra-files "./model/config.json,./model/vocab.txt" --handler "handler.py"`

    *Above command attaches the serialized checkpoint of your model*

8. Now, we can start a TorchServe server (by default it uses ports 8080 and 8081) for our model with a model store that contains our MAR file <br>
    `mkdir model_store && mv NAME_OF_THE_MODEL.mar model_store && torchserve --start --model-store model_store --models NAME_OF_THE_MODEL=NAME_OF_THE_MODEL.mar`

9. Now comes the moment of truth wheather our TorchServe API is working or not. To check it I have provided a file in the repo itself to test the API.