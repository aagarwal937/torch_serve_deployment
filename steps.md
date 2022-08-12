# Sequence of steps


### pre-requisites
MODEL_DIR (path/to/model/files)
MAR_MODEL_STORE (path/to/mode/store)



### create mar file
`torch-model-archiver --model-name <some_name> --version <some_version> --serialized-file ./MODEL_DIR/pytorch_model.bin --extra-files "./MODEL_DIR/config.json,./MODEL_DIR/vocab.txt" --handler <model_handler_file>
`

example some_name -> bert
example some_version -> 1.0
example model_handler_file -> transformers_classifier_torchserve_handler.py


### store/copy/move the resulting .mar file into a well know directory 'MAR_MODEL_STORE'


### start the torchserve server
`torchserve --start --model-store MAR_MODEL_STORE --models <some_env_var>=<some_name>.mar
`