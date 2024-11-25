import grpc
from rover_protos.mars_rover_pb2 import StopRequest, DriveRequest
from rover_protos.mars_rover_pb2_grpc import RoverServiceStub

# Connect to the server
channel = grpc.insecure_channel("localhost:50051")
stub = RoverServiceStub(channel)

# Test the DriveForward RPC
drive_request = DriveRequest(speed=10.0)
drive_response = stub.DriveForward(drive_request)
print(f"DriveForward Response: {drive_response.message}, Success: {drive_response.success}")

# Test the StopMovement RPC
stop_request = StopRequest()
stop_response = stub.StopMovement(stop_request)
print(f"StopMovement Response: {stop_response.message}, Success: {stop_response.success}")