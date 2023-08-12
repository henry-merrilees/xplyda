import subprocess

# todo: presently the file must be run from package root, make absolute

def compile_proto():
    """ This compilation step must precede the import of the generated proto modules. """
    print("Generating proto files...") 
    # this is the proto file in project root, not package root
    proto_file_path = '../proto/embedding.proto'
    subprocess.run([
        'python', '-m', 'grpc_tools.protoc',
        '-I../proto', '--python_out=.', '--grpc_python_out=.',
        proto_file_path
    ])
    print("Proto files generated.")

compile_proto()
# this will complain until the proto files are generated
import embedding_pb2
import embedding_pb2_grpc

__all__ = ("embedding_pb2", "embedding_pb2_grpc")
