import os

import yaml
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, OpaqueFunction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def get_teleop_controller(_context, *_, **kwargs) -> Node:
    return [Node(
        package="simple_drone_control",
        executable="teleop",
        namespace=kwargs["model_ns"],
        output="screen",
        prefix="xterm -e",
        arguments=['--ros-args', '--log-level', 'DEBUG'],
    )]

def generate_launch_description():
    simple_drone_bringup_path = get_package_share_directory('simple_drone_bringup')

    rviz_path = os.path.join(
        simple_drone_bringup_path, "rviz", "rviz.rviz"
    )
    
    yaml_file_path = os.path.join(
        get_package_share_directory('simple_drone_bringup'),
        'config', 'drone.yaml'
    )

    model_ns = "drone"

    with open(yaml_file_path, 'r') as f:
        yaml_dict = yaml.load(f, Loader=yaml.FullLoader)
        model_ns = yaml_dict["namespace"]

    return LaunchDescription([
        Node(
            package="rviz2",
            executable="rviz2",
            name="rviz2",
            arguments=[
                "-d", rviz_path
            ],
            output="screen",
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(simple_drone_bringup_path, 'launch', 'simple_drone_gazebo.launch.py')
            )
        ),

        Node(
            package='joy',
            executable='joy_node',
            name='joy',
            namespace=model_ns,
            output='screen',
        ),

        OpaqueFunction(
            function=get_teleop_controller,
            kwargs={'model_ns': model_ns},
        ),
    ])
