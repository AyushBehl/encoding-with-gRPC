import grpc
from proto import numbers_pb2_grpc
from proto import numbers_pb2

def streamingEncoding():

    while True:
        inputString = input('Enter input string for encoding or just exit to exit: ')
        if inputString == 'exit':
            break

        encodeRequest = numbers_pb2.UnaryDataRequest(unaryToUnary = inputString)
        yield encodeRequest


def run():
    with grpc.insecure_channel('localhost:52000') as channel:
        stub = numbers_pb2_grpc.GrpcTestServiceStub(channel)

        print("enter type of encoding to be done with grpc: ")
        userInput = input(" 1. Binary to Binary call encoding in grpc \n 2. Binary to Stream call encoding in grpc \n 3. Stream to Binary call encoding in grpc \n 4. Stream to Stream call encoding : \n")
        
        if userInput == '1':
            encodeStringRequest = numbers_pb2.UnaryDataRequest(unaryToUnary = 'test string')
            callAndResponse = stub.GrpcTestFunction(encodeStringRequest)
            print(callAndResponse.encoded)
        
        elif userInput == '2':
            encodingListRequest = numbers_pb2.UnaryToStreamDataRequest(unaryToStream = ['first string', 'second string'])
            getResponse = stub.UnaryToStreamFunction(encodingListRequest)
            for response in getResponse:
                print(response)
        
        elif userInput == '3':
            encodeStreamRequest = stub.StreamToUnaryFunction(streamingEncoding())
            print(encodeStreamRequest)
        
        elif userInput == '4':
            responseChat = stub.StreamToStreamFunction(streamingEncoding())
            for responseReceived in responseChat:
                print('Response received: ')
                print(responseReceived.encoded)

if __name__ == "__main__":
    run()