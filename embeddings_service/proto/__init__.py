import subprocess

# This compilation step must precede the import of the generated proto modules.
print("Generating proto files...") 
# this is the proto file in main project root, not python root
proto_file_path = '../proto/embedding.proto'
subprocess.run([
    'python', '-m', 'grpc_tools.protoc',
    '-I../proto', '--python_out=.', '--grpc_python_out=.',
    proto_file_path
])
print("Proto files generated.")

# this will complain until the proto files are generated
import embedding_pb2
import embedding_pb2_grpc

__all__ = ("embedding_pb2", "embedding_pb2_grpc")
