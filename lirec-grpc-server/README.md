# Ramanujan Machine Web Portal - LIReC gRPC Server

You will need to have Python gRPC tools installed:

`pip install grpcio grpcio-tools`

And you will need to generate the code from the proto, running this command from the `lire-grpc-server` directory:

`python3 -m grpc_tools.protoc --proto_path=../protos --python_out=. --grpc_python_out=. ../protos/lirec.proto`

You should then be able to run the gRPC server (after activating your virtual environment and installing dependencies from requirements.txt):

`python server.py &`

You can then interact with the gRPC server however you choose. grpcurl is a great command line tool or you can use a tool with a user interface such as Postman.
