import subprocess

proto_file_path = '../proto/embedding.proto' # proto folder in project root, not python root
subprocess.run([
    'python', '-m', 'grpc_tools.protoc',
    '-I../proto', '--python_out=.', '--grpc_python_out=.',
    proto_file_path
])
# the above compilation step must precede the import of the generated proto modules.

# imports will complain until the proto files are generated
import embedding_pb2
import embedding_pb2_grpc

__all__ = ("embedding_pb2", "embedding_pb2_grpc")
