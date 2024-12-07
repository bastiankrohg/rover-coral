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

    def rotate_on_spot(self, angle):
        request = mars_rover_pb2.TurnRequest(angle=angle)
        response = self.mapping_stub.RotateOnSpot(request)  # Use mapping_stub
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