import grpc
from rover_protos import mars_rover_pb2, mars_rover_pb2_grpc


class Coral:
    def __init__(self, mapping_server_address="localhost:50051", ultra_server_address="localhost:50052"): # pi_server_address="localhost:50052"):
        # Mapping server connection
        self.mapping_channel = grpc.insecure_channel(mapping_server_address)
        self.mapping_stub = mars_rover_pb2_grpc.RoverServiceStub(self.mapping_channel)

        # Ultrasound server connection
        self.ultrasound_channel = grpc.insecure_channel(ultra_server_address)
        self.ultrasound_stub = mars_rover_pb2_grpc.RoverServiceStub(self.ultrasound_channel)

        print("[DEBUG] Connected to both Mapping and Ultrasound servers.")

    # === Mapping Commands ===
    def drive_forward(self, speed):
        request = mars_rover_pb2.DriveRequest(speed=speed)
        response = self.mapping_stub.DriveForward(request)
        print(response.message)

    def reverse(self, speed):
        request = mars_rover_pb2.DriveRequest(speed=speed)
        response = self.mapping_stub.Reverse(request)
        print(response.message)

    def turn_left(self, angle):
        request = mars_rover_pb2.TurnRequest(angle=angle)
        response = self.mapping_stub.TurnLeft(request)
        print(response.message)

    def turn_right(self, angle):
        request = mars_rover_pb2.TurnRequest(angle=angle)
        response = self.mapping_stub.TurnRight(request)
        print(response.message)

    def rotate_on_spot(self, angle):
        request = mars_rover_pb2.TurnRequest(angle=angle)
        response = self.mapping_stub.RotateOnSpot(request)
        print(response.message)

    def stop_movement(self):
        request = mars_rover_pb2.StopRequest()
        response = self.mapping_stub.StopMovement(request)
        print(response.message)

    def place_resource(self, distance):
        request = mars_rover_pb2.PlaceResourceRequest(distance=distance)
        response = self.mapping_stub.PlaceResource(request)
        print(response.message)

    def place_obstacle(self, distance):
        request = mars_rover_pb2.PlaceObstacleRequest(distance=distance)
        response = self.mapping_stub.PlaceObstacle(request)
        print(response.message)

    # === Ultrasound Measurements ===
    def get_ultrasound_measurement(self):
        request = mars_rover_pb2.UltrasoundRequest()
        response = self.ultrasound_stub.GetUltrasoundMeasurement(request)
        print(f"[DEBUG] Ultrasound Measurement: {response.distance} cm")
        return response.distance