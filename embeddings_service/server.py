import logging
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

logger = logging.getLogger("rich")

import typer
import grpc
from concurrent import futures
from sentence_transformers import SentenceTransformer
from proto import embedding_pb2, embedding_pb2_grpc

import embedding_pb2_grpc
import numpy as np
from time import time

import sys
MAX_MESSAGE_LENGTH = -1 # -1 means unlimited
OPTIONS=(
        ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
        ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH),
)

class EmbeddingService(embedding_pb2_grpc.EmbeddingServiceServicer):
    def __init__(self, device):
        logger.info('Initializing EmbeddingService.')
        self.embedding_model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2', device=device)
        self.device = device

    def GenerateEmbeddings(self, request, context):
        start = time()

        logger.info(f'GenerateEmbeddings called with {len(request.texts)} texts. Handling on device ({self.device}).')
        texts = request.texts
        embeddings = self.embedding_model.encode(texts, device=self.device)
        embedding_list = [embedding_pb2.Embedding(values=e.tolist()) for e in embeddings]
        response = embedding_pb2.EmbeddingResponse(embeddings=embedding_list)

        end = time()
        duration = end-start
        per = duration/len(texts)
        logger.info(f'GenerateEmbeddings finished in {duration:.4f}s ({per:.6f}s per text).')
        return response



def _client(port):
    """ An example client calling the EmbeddingService. """
    with grpc.insecure_channel(f'localhost:{port}') as channel:
        stub = embedding_pb2_grpc.EmbeddingServiceStub(channel)
        texts = ["This is a sample text.", "Another example text."]
        response = stub.GenerateEmbeddings(embedding_pb2.EmbeddingRequest(texts=texts))
        
        embeddings = [np.array(e.values) for e in response.embeddings]
        for text, embedding in zip(texts, embeddings):
            print(f"Text: {text}")
            print(f"Embedding: {embedding}")

def serve(port: int = 50052, device: str = 'cpu'):
    logger.info(f"Server started on port {port}...")
    logger.warn("GRPC often by default has an incoming message size limit of 4MB. If you need to encode more than about 5000 embeddings, you need to increase this limit.")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), options=OPTIONS)
    embedding_pb2_grpc.add_EmbeddingServiceServicer_to_server(EmbeddingService(device=device), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    typer.run(serve)
