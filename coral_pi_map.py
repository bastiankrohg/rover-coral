import grpc
from rover_protos import mars_rover_pb2, mars_rover_pb2_grpc


class Coral:
    def __init__(self, mapping_server_address="localhost:50051", pi_address="192.168.0.169:50052"):
        # Mapping server connection
        self.mapping_channel = grpc.insecure_channel(mapping_server_address)
        self.mapping_stub = mars_rover_pb2_grpc.RoverServiceStub(self.mapping_channel)

        # Pi server connection
        self.pi_channel = grpc.insecure_channel(pi_address)
        self.pi_stub = mars_rover_pb2_grpc.RoverServiceStub(self.pi_channel)

        print("[DEBUG] Connected to both Mapping and Pi servers.")

    # === Locomotion ===
    def drive_forward(self, speed):
        request = mars_rover_pb2.DriveRequest(speed=speed)
        # Call mapping and pi stubs
        self.mapping_stub.DriveForward(request)
        response = self.pi_stub.DriveForward(request)
        print(response.message)

    def reverse(self, speed):
        request = mars_rover_pb2.DriveRequest(speed=speed)
        # Call mapping and pi stubs
        self.mapping_stub.Reverse(request)
        response = self.pi_stub.Reverse(request)
        print(response.message)

    def move_distance(self, distance_cm, speed):
        """Move the rover forward/backward by a specified distance."""
        request = mars_rover_pb2.MoveDistanceRequest(distance=distance_cm, speed=speed)
        response = self.pi_stub.MoveDistance(request)
        print(response.message)

    def brake(self):
        """Send a command to activate the rover's braking."""
        request = mars_rover_pb2.StopRequest()  # No arguments required
        response = self.pi_stub.Brake(request)  # Call the Pi gRPC stub
        print(response.message)

    def turn_left(self, speed):
        request = mars_rover_pb2.TurnRequest(speed=speed)
        # Call mapping and pi stubs
        self.mapping_stub.TurnLeft(request)
        response = self.pi_stub.TurnLeft(request)
        print(response.message)

    def turn_right(self, speed):
        request = mars_rover_pb2.TurnRequest(speed=speed)
        # Call mapping and pi stubs
        self.mapping_stub.TurnRight(request)
        response = self.pi_stub.TurnRight(request)
        print(response.message)

    def turn_on_spot(self, speed):
        request = mars_rover_pb2.TurnRequest(speed=speed)
        # Call mapping and pi stubs
        self.mapping_stub.TurnOnSpot(request)
        response = self.pi_stub.TurnOnSpot(request)
        print(response.message)

    def spin_angle(self, angle):
        """Spinning in place by an angle"""
        request = mars_rover_pb2.SpinRequest(angle=angle)
        response = self.pi_stub.SpinAngle(request)
        print(response.message)
    
    def turn_angle_forward(self, angle, speed=50):
        """Turning forward while adjusting the angle"""
        request = mars_rover_pb2.TurnRequest(angle=angle, speed=speed)
        response = self.pi_stub.TurnAngleForward(request)
        print(response.message)

    def turn_angle_backward(self, angle, speed=50):
        """Turning backward while adjusting the angle"""
        request = mars_rover_pb2.TurnRequest(angle=angle, speed=speed)
        response = self.pi_stub.TurnAngleBackward(request)
        print(response.message)

    def stop_movement(self):
        request = mars_rover_pb2.StopRequest()
        # Call mapping and pi stubs
        self.mapping_stub.StopMovement(request)
        response = self.pi_stub.StopMovement(request)
        print(response.message)

    # === Sensors ===
    def get_ultrasound_measurement(self):
        request = mars_rover_pb2.UltrasoundRequest()
        response = self.pi_stub.GetUltrasoundMeasurement(request)
        print(f"Ultrasound Measurement: {response.distance} cm")
        return response.distance

    def get_light_intensity(self):
        request = mars_rover_pb2.LightIntensityRequest()
        response = self.pi_stub.GetLightIntensity(request)
        print(f"Light Intensity: {response.intensity}")
        return response.intensity

    # === LED Control ===
    def control_headlights(self, on):
        request = mars_rover_pb2.LEDRequest(on=on)
        response = self.pi_stub.ControlHeadlights(request)
        print(response.message)

    def control_wheel_leds(self, wheel_number, on):
        request = mars_rover_pb2.WheelLEDRequest(wheel_number=wheel_number, on=on)
        response = self.pi_stub.ControlWheelLEDs(request)
        print(response.message)

    # === Servo Control ===
    def rotate_periscope(self, angle):
        request = mars_rover_pb2.RotateRequest(angle=angle)
        response = self.pi_stub.RotatePeriscope(request)
        print(response.message)

    def calibrate_servo(self, servo_number, angle):
        request = mars_rover_pb2.RotateRequest(angle=angle)
        response = self.pi_stub.CalibrateServo(request)
        print(response.message)

    # === Mapping ===
    def map_resource(self, distance=None, size=1.0, object_label="Undefined"):
        if not distance:
            distance = self.get_ultrasound_measurement()
        request = mars_rover_pb2.ResourceObstacleRequest(
            distance=distance, size=size, object=object_label
        )
        response = self.mapping_stub.MapResource(request)
        print(response.message)

    def map_obstacle(self, distance=None, size=1.0, object_label="Undefined"):
        if not distance:
            distance = self.get_ultrasound_measurement()
        request = mars_rover_pb2.ResourceObstacleRequest(
            distance=distance, size=size, object=object_label
        )
        response = self.mapping_stub.MapObstacle(request)
        print(response.message)

    def toggle_resource_list(self):
        request = mars_rover_pb2.CommandResponse()
        response = self.mapping_stub.ToggleResourceList(request)
        print(response.message)

    def toggle_obstacle_list(self):
        request = mars_rover_pb2.CommandResponse()
        response = self.mapping_stub.ToggleObstacleList(request)
        print(response.message)

    def toggle_scan(self):
        request = mars_rover_pb2.CommandResponse()
        response = self.mapping_stub.ToggleScan(request)
        print(response.message)

    def save_map(self, file_name):
        request = mars_rover_pb2.SaveMapRequest(file_name=file_name)
        response = self.mapping_stub.SaveMap(request)
        print(response.message)