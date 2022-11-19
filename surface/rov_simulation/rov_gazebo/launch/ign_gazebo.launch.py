# Copyright 2022 CWRUbotix
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from ament_index_python.packages import get_package_share_directory

from launch_ros.actions import Node
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch.substitutions import Command
from launch_ros.descriptions import ParameterValue


def generate_launch_description():

    rov_gazebo_path: str = get_package_share_directory('rov_gazebo')
    ros_ign_gazebo_path: str = get_package_share_directory('ros_ign_gazebo')
    rov_description_path: str = get_package_share_directory('rov_description')
    world_path: str = os.path.join(
        rov_gazebo_path, 'worlds', 'underwater.world'
    )

    # Launches Gazebo
    gazeboLaunch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(
                ros_ign_gazebo_path, 'launch', 'ign_gazebo.launch.py'
            )
        ]),
        launch_arguments={world_path}
    )

    filenameURDF: str = "rov.xacro"
    filenameYaml: str = "rov_description_params.yaml"
    # filenameSDF = "rov.sdf"
    # filenameTest ="bluerov.sdf"

    # Path to Xacro file of robot
    path_to_urdf: str = os.path.join(rov_description_path, 'urdf', filenameURDF)

    # path_to_param = os.path.join(rov_description_path,'config',filenameYaml)
    # path_to_sdf = os.path.join(rov_description_path,'urdf',filenameSDF)
    # path_to_test_sdf = os.path.join(rov_description_path,'urdf',filenameTest)

    robot_desc: ParameterValue = ParameterValue(
        Command(['xacro ', path_to_urdf, ' params_path:=', filenameYaml]), value_type=str
        # Command("xacro rov.xacro params_path:=rov_description_params.yaml")
    )

    params = {
            'robot_description': robot_desc
    }

    # Publishes the state of the robot
    robot_state_publisher_node: Node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[params],
        # arguments=[path_to_urdf]
    )

    # joint_state_publisher_node: Node = Node(
    #     package='joint_state_publisher',
    #     executable='joint_state_publisher',
    #     arguments=[path_to_urdf]
    # )

    topicName: str = "robot_description"

    create_robot_node: Node = Node(
        package='ros_ign_gazebo',
        executable='create',
        arguments=[
            '-topic', topicName,
            # 'output', 'screen',
        ]
    )

    # spawn_entity_node: Node = Node(
    #     package='gazebo_ros',
    #     executable='spawn_entity.py',
    #     arguments=[
    #         '-entity','rov',
    #         '-topic','/robot_description',
    #         '-x', '0',
    #         '-y', '2',
    #         '-z', '0',
    #        # 'output', 'screen',
    #     ]
    # )

    # rviz = Node(
    #     package="rviz2",
    #     executable="rviz2",
    #     arguments=['-d' + os.path.join(rov_gazebo_path, 'config', 'rov.rviz')],

    # )

    return LaunchDescription([
        gazeboLaunch,
        robot_state_publisher_node,
        create_robot_node,
        # joint_state_publisher_node,
        # spawn_entity_node,
        # rviz,
    ])