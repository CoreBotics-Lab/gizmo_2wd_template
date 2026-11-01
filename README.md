# Gizmo 2WD Autonomous Mobile Robot Template

A reproducible, fully isolated ROS 2 and Gazebo Harmonic simulation template for the Gizmo 2-Wheel Differential Drive Autonomous Mobile Robot (AMR). Powered by Pixi and RoboStack.

---

## Architectural Overview

This template provides the canonical kinematic, sensor, and simulation baseline for the Gizmo AMR. It is designed to be cloned or instantiated as a GitHub template for research and development across autonomous navigation, computer vision, spatial perception, and fleet robotics.

```
                                [ROS 2 User Nodes / Teleop]
                                             |
                                             v
                                         (/cmd_vel)
                                             |
                                             v
                                     [ros_gz_bridge]
                                       |          ^
                            (gz.msgs.Twist)       | (Sensor Messages)
                                       v          |
     +-------------------------------------------------------------------------+
     |                            Gazebo Harmonic                              |
     |                                                                         |
     |   +-----------------------------------------------------------------+   |
     |   |                       Gizmo 2WD Robot Model                     |   |
     |   |                                                                 |   |
     |   |  - Diff Drive: 70mm Drive Wheels (gz-sim-diff-drive-system)     |   |
     |   |  - 2D LiDAR: 360 deg Planar Scanner (gz-sim-sensors-system)     |   |
     |   |  - RGB/Depth Camera: Intel RealSense D435 Model                 |   |
     |   |  - IMU: 6-DOF Inertial Measurement Unit                         |   |
     |   +-----------------------------------------------------------------+   |
     |                                                                         |
     +-------------------------------------------------------------------------+
```

---

## Hardware and Kinematic Specifications

| Parameter | Specification | URDF Definition |
| :--- | :--- | :--- |
| **Drive Architecture** | 2-Wheel Differential Drive with Dual Passive Casters | `gizmo_description/urdf/include/robot_components/` |
| **Wheel Diameter** | $70\,\text{mm}$ ($r = 0.035\,\text{m}$) | `wheel_left.xacro`, `wheel_right.xacro` |
| **Wheel Track Separation** | $0.160\,\text{m}$ | `gizmo_mobile_base.xacro` |
| **Primary Vision Sensor** | Intel RealSense D435 RGB/Depth Camera | `camera.xacro`, `camera.gazebo.xacro` |
| **Planar Rangefinder** | 2D Laser Scanner ($360^\circ$ FOV) | `lidar.xacro`, `lidar.gazebo.xacro` |
| **Inertial Unit** | Bosch BNO055 9-DOF IMU (filtered to 6-DOF) | `imu.xacro`, `imu.gazebo.xacro` |
| **Middleware** | Eclipse CycloneDDS (`rmw_cyclonedds_cpp`) | `dds_config/cyclonedds.xml` |

---

## Package Architecture

| Package | Type | Description |
| :--- | :--- | :--- |
| **`gizmo_description`** | `ament_cmake` | Kinematic URDF/Xacro macros, STL visual and collision meshes, mass inertia matrices, and Gazebo sensor attachments. |
| **`gizmo_gazebo`** | `ament_cmake` | Gazebo Harmonic simulation worlds (`simpleWorld.sdf`, `simpleBiggerWorld.sdf`), ROS-GZ bidirectional topic bridge configs, and robot spawn orchestrators. |
| **`gizmo_teleop`** | `ament_cmake` | Keyboard velocity teleoperation interface with hardware limit clamping publishing directly to `/cmd_vel`. |

---

## ROS 2 Topics and Sensor Interface

| ROS 2 Topic | Type | Direction | Gazebo Source |
| :--- | :--- | :--- | :--- |
| `/cmd_vel` | `geometry_msgs/msg/Twist` | ROS $\to$ GZ | Differential drive controller plugin |
| `/wheel_odom` | `nav_msgs/msg/Odometry` | GZ $\to$ ROS | Wheel encoder odometry plugin |
| `/joint_states` | `sensor_msgs/msg/JointState` | GZ $\to$ ROS | Drive wheel joint state publisher |
| `/scan` | `sensor_msgs/msg/LaserScan` | GZ $\to$ ROS | Planar LiDAR sensor plugin |
| `/camera/image_raw` | `sensor_msgs/msg/Image` | GZ $\to$ ROS | RealSense D435 RGB sensor |
| `/camera/camera_info` | `sensor_msgs/msg/CameraInfo` | GZ $\to$ ROS | RealSense D435 intrinsic matrix |
| `/camera/depth/image_raw`| `sensor_msgs/msg/Image` | GZ $\to$ ROS | RealSense depth sensor |
| `/imu/data` | `sensor_msgs/msg/Imu` | GZ $\to$ ROS | IMU sensor plugin |

---

## Quickstart Guide

### 1. Prerequisites
Install Pixi on Linux or WSL2 (Ubuntu 24.04 or 26.04 recommended):
```bash
curl -fsSL https://pixi.sh/install.sh | bash
```

### 2. Workspace Initialization
Clone this repository and install the isolated RoboStack environment:
```bash
git clone https://github.com/CoreBotics-Lab/gizmo_2wd_template.git
cd gizmo_2wd_template
pixi install
```

### 3. Entering the Shell and Building
Enter the isolated shell where ROS 2 variables, CycloneDDS, and custom build aliases are automatically sourced:
```bash
pixi shell
build
```

Custom build helper commands available inside `pixi shell`:
* `build` - Incremental build across all workspace packages with symlink-install.
* `build <package_name>` - Build a single package with auto-completion.
* `debug <package_name>` - Build with `RelWithDebInfo` for GDB debugging.
* `clean all` - Remove `build/`, `install/`, and `log/` directories cleanly.

---

## Running the Simulation

### Launch Robot Simulation in Gazebo Harmonic
```bash
pixi run ros2 launch gizmo_gazebo gazebo_simpleWorld.launch.py
```

### Launch RViz2 Model Visualizer
In a second terminal:
```bash
pixi shell
rviz2 -d install/gizmo_gazebo/share/gizmo_gazebo/rviz/gazebo.rviz
```

### Keyboard Teleoperation
In a third terminal:
```bash
pixi shell
ros2 run gizmo_teleop teleop_node
```

---

## Using as a Base for New Projects

To create a new AMR project from this template:
1. Click **Use this template** on GitHub to create a new project repository (e.g., `gizmo_vision_docking`).
2. Clone your new repository and add project-specific dependencies directly to `pixi.toml` (e.g. `ros-lyrical-cv-bridge`, `opencv`).
3. Add your project packages into `src/` alongside `gizmo_description`, `gizmo_gazebo`, and `gizmo_teleop`.

