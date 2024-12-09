# Rover-Coral Interface

This repository provides the control interface for integrating a Google Coral Dev Board with mapping and sensor modules for the rover system. It supports testing the mapping module over gRPC and demonstrates multi-channel communication for rover controls and sensor integration. 

### Key Features:
- **`control.py`**: Acts as the main control interface over gRPC, working with the dummy ultrasound measurement script (`dummy_ultrasound.py`) to test mapping module functionalities. 
- **`coral_control.py`**: Defines the Coral class, slightly modified from `coral.py` and `coral_v2.py`, to include map-specific functionalities for extended control.
- **`coral.py`**: Contains a `main()` function and can be run independently for simple control testing.
- **`coral_v2.py`**: Designed to work alongside `manualcontrol.py` for advanced manual testing scenarios.

This repository will eventually be updated to interface with the physical hardware, sensors, and the mapping module running on the Coral Dev Board.

## Setting Up the Environment

To get started, ensure your system is prepared with the necessary dependencies and configurations.

### 1. Clone the Repository

```bash
git clone https://github.com/bastiankrohg/rover-coral.git
cd rover-coral
```

---

### 2. Install Dependencies

Ensure Python is installed (version 3.8 or later recommended). Install the required Python packages by running:

```bash
pip install grpcio grpcio-tools pynput
```

---

### 3. Starting the Modules

#### 3.1. Starting `control.py`

To start the `control.py` script, which acts as the gRPC control interface, run:

```bash
python control.py
```

This script demonstrates key control functions for testing the mapping module. It works with the dummy ultrasound script (dummy_ultrasound.py) and can be extended for integration with physical sensors and devices.

#### 3.2. Running the Dummy Ultrasound Sensor
From the rover-pi repository, start the dummy ultrasound sensor script to simulate distance measurements:
```bash
python dummy_ultrasound.py
```

This script simulates sensor data, allowing you to test the mapping functionality without needing actual hardware.

#### 3.3. Running the Mapping Module with gRPC

To test the mapping module alongside `control.py` and the dummy ultrasound script, start the mapping module:

```bash
python game_map_grpc.py
```

This script launches the mapping interface with gRPC integration. Ensure that both control.py and the dummy ultrasound sensor are running for a complete test environment.

#### 3.4. Running coral.py

To test the Coral Dev Board’s gRPC functionalities, run coral.py or manualcontrol.py:

```bash
python coral.py
```

or 

```bash
python manualcontrol.py
```

These scripts initiates the basic gRPC client, which connects to the mapping module or other gRPC servers as configured. Not integrated with the mapping module.

The manualcontrol.py script also has some basic functionality to steer the rover using the keyboard

---

### 4. Using the Controls
- W: Drive forward.
- S: Reverse.
- A: Turn on the spot (left).
- D: Turn on the spot (right).
- Q: Rotate mast left.
- E: Rotate mast right.
- O: Place a resource using the ultrasound measurement.
- P: Place an obstacle using the ultrasound measurement.
- T: Toggle scanning.
- TAB: Toggle the resource list display.
- SPACE: Toggle the obstacle list display.
- M: Save the current map to latest.json.
- ESC: Exit the control script.

Make sure to test the controls alongside the mapping module to observe how inputs affect the simulated environment.

---

### 5. Modifying and Extending the Protos

If you need to modify or extend the gRPC communication capabilities, follow these steps:

#### 5.1. Updating the Protobuf Definitions

1. Navigate to the `rover_protos` directory:
   ```bash
   cd rover_protos
   ```

2.	Modify the mars_rover.proto file to include your new message types or RPC methods.

#### 5.2. Compiling the Protobuf Files

After updating the .proto file, compile it into Python files using grpcio-tools:
    ```bash
    python -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. mars_rover.proto
    ```
This generates the mars_rover_pb2.py and mars_rover_pb2_grpc.py files.

#### 5.3. Adjusting the Imports
Once the files are compiled, adjust the imports in mars_rover_pb2_grpc.py:
- Replace the import statement that causes issues (at least when testing locally on my mac):
   ```python
   import mars_rover_pb2 as mars__rover__pb2
   ```
- Add a relative path to the mars_rover_pb2 import:
   ```python
   from . import mars_rover_pb2 as mars__rover__pb2
   ```

This ensures compatibility when using the rover_protos directory as a module.

#### 5.4. Updating Submodules

If the rover_protos directory is a git submodule, recursively update it after making changes:
    ```bash
    git submodule update --remote --recursive
    ```

---

### 6. Future Improvements: 
The rover-coral module has the potential to evolve into a highly capable system for autonomous or semi-autonomous rover operations. Most of these are optimistic, and only documented as potential improvements should the project be picked up again at a later time. Here are the key areas of focus for future improvements:

#### 6.1. Real-Time Path Planning
- Dynamic Pathfinding:
    - Implement algorithms like A* or Dijkstra to dynamically compute the most efficient routes while avoiding obstacles in real time.
    - Factor in terrain data from the mapping module to adjust for potential hazards or impassable zones.
- Reactive Adjustments:
    - Enable the rover to adjust its planned path based on unexpected changes in the environment detected by sensors.

6.2. Range Constraints in Path Planning
- Optimized Coverage:
    - Develop logic to ensure the rover operates within a predefined range, conserving battery and resources.
- Return-to-Base:
    - Introduce mechanisms to calculate the shortest route back to the starting position or charging station when the range limit is reached.
- Prioritized Navigation:
    - Allow configuration of priority zones or resources, enabling path planning to focus on high-value targets within constraints.

#### 6.3. Pattern Search and Route Generation
- Search Patterns:
    - Implement predefined search patterns such as lawnmower (SAR), spiral, or grid-based coverage for systematic area exploration.
- Autopilot:
    - Create a module to generate and execute sequences of commands for autonomous pattern-based movement.
    - Combine with real-time adjustments to adapt patterns based on obstacles or environment feedback.

#### 6.4. Autonomy
- Command Sequencing:
    - Automate the generation of complex sequences for tasks like resource collection, area scanning, and obstacle avoidance.
- Multi-Objective Optimization:
    - Enable autonomous decision-making to balance objectives such as coverage, resource efficiency, and return-to-base safety.
- Self-Correction

#### 6.5. Telemetry Dashboard
- Real-Time Data Visualization:
    - Develop a telemetry dashboard showing rover position, heading, detected obstacles/resources, and operational status (e.g., battery, connection).
- Control Feedback:
    - Allow operators to monitor the progress of autonomous tasks and intervene manually if necessary.

#### 6.6. Integration with Mapping and Hardware
- Mapping Synchronization:
    - Ensure tight integration with the mapping module for real-time updates of the rover’s environment and traced path.
- Hardware Calibration:
    - Align the software control logic with the physical hardware’s movement characteristics (e.g., turn radius, speed).
- Odometry Feedback:
    - Incorporate data from motor encoders or sensors to improve accuracy in mapping and navigation.