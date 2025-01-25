import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument, LogInfo
from launch_ros.actions import Node

import xacro


def generate_launch_description():
    # Declare use_sim_time argument
    use_sim_time = LaunchConfiguration('use_sim_time')

    # Get the package directory and Xacro file path
    try:
        pkg_path = get_package_share_directory('differential_drive_robot')
        xacro_file = os.path.join(pkg_path, 'description', 'robot_core.xacro')
    except Exception as e:
        raise RuntimeError(f"Error finding package or Xacro file: {e}")

    # Process the Xacro file
    try:
        robot_description_config = xacro.process_file(xacro_file).toxml()
    except Exception as e:
        raise RuntimeError(f"Error processing Xacro file: {e}")

    # Create a robot_state_publisher node
    params = {'robot_description': robot_description_config, 'use_sim_time': use_sim_time}
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params]
    )

    # Log messages for better debugging
    log_info_node = LogInfo(msg="Launching robot_state_publisher with the provided URDF...")

    # Return the LaunchDescription
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation time if true'
        ),
        log_info_node,
        node_robot_state_publisher
    ])
