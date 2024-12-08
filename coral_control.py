import grpc
from rover_protos import mars_rover_pb2, mars_rover_pb2_grpc


class Coral:
    def __init__(self, mapping_server_address="localhost:50051", ultra_server_address="localhost:50052"):
        # Mapping server connection
        self.mapping_channel = grpc.insecure_channel(mapping_server_address)
        self.mapping_stub = mars_rover_pb2_grpc.RoverServiceStub(self.mapping_channel)

        # Ultrasound server connection
        self.ultrasound_channel = grpc.insecure_channel(ultra_server_address)
        self.ultrasound_stub = mars_rover_pb2_grpc.RoverServiceStub(self.ultrasound_channel)

        print("[DEBUG] Connected to both Mapping and Ultrasound servers.")

    # === Locomotion ===
    def drive_forward(self, speed):
        request = mars_rover_pb2.DriveRequest(speed=speed)
        response = self.mapping_stub.DriveForward(request)  # Use mapping_stub
        print(response.message)

    def reverse(self, speed):
        request = mars_rover_pb2.DriveRequest(speed=speed)
        response = self.mapping_stub.Reverse(request)  # Use mapping_stub
        print(response.message)

    def turn_left(self, angle):
        request = mars_rover_pb2.TurnRequest(angle=angle)
        response = self.mapping_stub.TurnLeft(request)  # Use mapping_stub
        print(response.message)

    def turn_right(self, angle):
        request = mars_rover_pb2.TurnRequest(angle=angle)
        response = self.mapping_stub.TurnRight(request)  # Use mapping_stub
        print(response.message)

    def turn_on_spot(self, angle):
        request = mars_rover_pb2.TurnRequest(angle=angle)
        response = self.mapping_stub.TurnOnSpot(request)  # Use mapping_stub
        print(response.message)

    def stop_movement(self):
        request = mars_rover_pb2.StopRequest()
        response = self.mapping_stub.StopMovement(request)  # Use mapping_stub
        print(response.message)

    # === Sensors ===
    def get_ultrasound_measurement(self):
        request = mars_rover_pb2.UltrasoundRequest()
        response = self.ultrasound_stub.GetUltrasoundMeasurement(request)  # Use ultrasound_stub
        print(f"Ultrasound Measurement: {response.distance} cm")
        return response.distance

    def get_light_intensity(self):
        request = mars_rover_pb2.LightIntensityRequest()
        response = self.ultrasound_stub.GetLightIntensity(request)  # Use ultrasound_stub
        print(f"Light Intensity: {response.intensity}")

    # === LED Control ===
    def control_headlights(self, on):
        request = mars_rover_pb2.LEDRequest(on=on)
        response = self.mapping_stub.ControlHeadlights(request)  # Use mapping_stub
        print(response.message)

    def control_wheel_leds(self, wheel_number, on):
        request = mars_rover_pb2.WheelLEDRequest(wheel_number=wheel_number, on=on)
        response = self.mapping_stub.ControlWheelLEDs(request)  # Use mapping_stub
        print(response.message)

    # === Servo Control ===
    def rotate_periscope(self, angle):
        request = mars_rover_pb2.RotateRequest(angle=angle)
        response = self.mapping_stub.RotatePeriscope(request)  # Use mapping_stub
        print(response.message)

    def calibrate_servo(self, servo_number, angle):
        request = mars_rover_pb2.RotateRequest(angle=angle)
        response = self.mapping_stub.CalibrateServo(request)  # Use mapping_stub
        print(response.message)

    # === Mapping ===
    def map_resource(self, distance=None, size=1.0, object_label="Undefined"):
        """Map a resource with optional object and distance."""
        if not distance:
            distance = self.get_ultrasound_measurement()
        request = mars_rover_pb2.ResourceObstacleRequest(
            distance=distance, size=size, object=object_label
        )
        response = self.mapping_stub.MapResource(request)
        print(response.message)

    def map_obstacle(self, distance=None, size=1.0, object_label="Undefined"):
        """Map an obstacle with optional object and distance."""
        if not distance:
            distance = self.get_ultrasound_measurement()
        request = mars_rover_pb2.ResourceObstacleRequest(
            distance=distance, size=size, object=object_label
        )
        response = self.mapping_stub.MapObstacle(request)
        print(response.message)

    def toggle_resource_list(self):
        request = mars_rover_pb2.CommandResponse()  # No specific data needed for toggling
        response = self.mapping_stub.ToggleResourceList(request)
        print(response.message)

    def toggle_obstacle_list(self):
        request = mars_rover_pb2.CommandResponse()  # No specific data needed for toggling
        response = self.mapping_stub.ToggleObstacleList(request)
        print(response.message)