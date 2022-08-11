r"""TorchServe uses the concept of handlers to define how requests are processed by a served model"""

# =============================================================================
# Importing the core modules
import os
import json
from json import JSONEncoder
import zipfile


# =============================================================================
# Importing the 3rd party modules
import numpy


# =============================================================================
# Importing the deep Learning modules
from sentence_transformers import SentenceTransformer


# =============================================================================
class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


class SematicSearch(object):
    """
    SematicSearch handler class. This handler takes a corpus and query strings
    as input and returns the closest 5 sentences of the corpus for each query sentence based on cosine similarity.
    """

    def __init__(self):
        super(SematicSearch, self).__init__()
        self.initialized = False
        self.embedder = None
    
    def initialize(self, context):
        properties = context.system_properties
        model_dir = properties.get("model_dir")
        print(model_dir)
        print(os.listdir('/home/ctopatdel/model-server/temp/'))
        try:
            with zipfile.ZipFile(model_dir + '/pytorch_model.bin', 'r') as zip_ref:
                zip_ref.extractall(model_dir)
            
            with zipfile.ZipFile(model_dir + '/pool.zip', 'r') as zip_ref:
                zip_ref.extractall(model_dir)
        except:
            print('tried unzipping again')
        
        self.embedder = SentenceTransformer(model_dir)
        self.initialized = True
    
    def preprocess(self, data):
        print(data)
        inputs = data[0].get("data")
        print(inputs)
        if inputs is None:
            inputs = data[0].get("body")
        inputs = inputs.decode('utf-8')
        inputs = json.loads(inputs)
        queries = inputs['queries']

        return queries

    def inference(self, data):
        query_embeddings = self.embedder.encode(data)
        return query_embeddings

    def postprocess(self, data):
        return [json.dumps(data, cls=NumpyArrayEncoder)]


_service = SematicSearch()

def handle(data, context):
    """
    Entry point for SematicSearch handler
    """
    try:
        if not _service.initialized:
            _service.initialize(context)

        if data is None:
            return None

        data = _service.preprocess(data)
        data = _service.inference(data)
        data = _service.postprocess(data)

        return data
    except Exception as e:
        raise Exception("Unable to process input data. " + str(e))