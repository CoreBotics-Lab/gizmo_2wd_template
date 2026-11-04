import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    gizmo_gazebo_dir = get_package_share_directory('gizmo_gazebo')
    
    line_world_path = os.path.join(
        gizmo_gazebo_dir,
        'worlds',
        'line_world.sdf'
    )
    
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gizmo_gazebo_dir, 'launch', 'gazebo.launch.py')
        ),
        launch_arguments={
            'world_file': line_world_path,
            'use_camera': 'true',
            'use_lidar': 'false',
            'run_rviz2': 'false',
            'spawn_x': '2.0',
            'spawn_y': '0.0',
            'spawn_z': '0.1',
            'spawn_yaw': '1.5708'
        }.items()
    )
    
    return LaunchDescription([
        gazebo_launch
    ])
