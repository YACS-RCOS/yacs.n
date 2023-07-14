import tensorflow_hub as hub
from ..io.output import Output

class Sentence_Embedder():

    def __init__(self):

        self.module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
        self.model = hub.load(self.module_url)
        self.debug = Output(Output.OUT.DEBUG, auto_clear=True)
        self.debug.print(f"module {self.module_url} loaded", Output.OUT.INFO)

    def embed(self, input):
        return self.model(input)
