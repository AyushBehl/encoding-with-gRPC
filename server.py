import base64
from concurrent import futures
import grpc
from proto import numbers_pb2_grpc
from proto import numbers_pb2

class GrpcTestServiceServicer (numbers_pb2_grpc.GrpcTestServiceServicer):

    def GrpcTestFunction(self, request, context):

        print ('Request received for unary communication')
        print(request.unaryToUnary)
        responseToSend = numbers_pb2.ResponseString()
        responseToSend.encoded = base64.b64encode(request.unaryToUnary.encode("utf-8"))
        return responseToSend

    def UnaryToStreamFunction(self, request, context):
        print ('Request received for unary to stream communication')
        print(request.unaryToStream)

        for i in range (2):
            response = numbers_pb2.EncodedUnaryToStreamResponse()
            streamData = []
            for i in request.unaryToStream:
                streamData.append(base64.b64encode(i.encode("utf-8")).decode("utf-8"))
            response.encodedUnaryToStream.extend(streamData)
            yield response
    
    def StreamToUnaryFunction(self, request_iterator, context):

        print('Request received for stream to unary reply')
        responseToSend = numbers_pb2.UnaryReply()
        for i in request_iterator:
            encodedData = base64.b64encode(i.unaryToUnary.encode("utf-8")).decode("utf-8")
            responseToSend.request.append(numbers_pb2.UnaryDataRequest(unaryToUnary = encodedData))

        return responseToSend
    
    def StreamToStreamFunction(self, request_iterator, context):

        print('Request received for stream to stream reply')
        for request in request_iterator:
            encoded = numbers_pb2.ResponseString()
            encoded.encoded = base64.b64encode(request.unaryToUnary.encode("utf-8"))
            yield encoded

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    numbers_pb2_grpc.add_GrpcTestServiceServicer_to_server(GrpcTestServiceServicer(), server)
    server.add_insecure_port('localhost:52000')
    server.start()
    server.wait_for_termination()
    print('Server started')

if __name__ == '__main__':
    serve()