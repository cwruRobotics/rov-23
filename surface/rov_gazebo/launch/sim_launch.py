import os
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

NS = "simulation"


def generate_launch_description():
    rov_gazebo_path: str = get_package_share_directory("rov_gazebo")
    ros_ign_gazebo_path: str = get_package_share_directory("ros_ign_gazebo")
    surface_main_path: str = get_package_share_directory("surface_main")

    # Generates rov_in_world.sdf file
    exec(open(os.path.join(rov_gazebo_path, "worlds", "make_sdf.py")).read())

    world_path: str = os.path.join(rov_gazebo_path, "worlds", "rov_in_world.sdf")

    # Launches Gazebo
    gazeboLaunch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [os.path.join(ros_ign_gazebo_path, "launch", "ign_gazebo.launch.py")]
        ),
        launch_arguments={"ign_args": world_path}.items(),
    )

    # Not using keyboard launch file
    keyboard_driver = Node(
        package="keyboard_driver",
        executable="keyboard_driver_node",
        output="screen",
        name="keyboard_driver_node",
        namespace=NS,
        remappings=[(f"/{NS}/manual_control", "/manual_control")]
    )

    # Thrust Bridge
    thrust_bridge = Node(
        package="ros_ign_bridge",
        executable="parameter_bridge",
        namespace=NS,
        name="thrust_bridge",
        arguments=[
            "/model/rov/joint/thruster_top_front_left_body_blade_joint/cmd_thrust"
            "@std_msgs/msg/Float64@ignition.msgs.Double",
            "/model/rov/joint/thruster_top_front_right_body_blade_joint/cmd_thrust"
            "@std_msgs/msg/Float64@ignition.msgs.Double",
            "/model/rov/joint/thruster_top_back_left_body_blade_joint/cmd_thrust"
            "@std_msgs/msg/Float64@ignition.msgs.Double",
            "/model/rov/joint/thruster_top_back_right_body_blade_joint/cmd_thrust"
            "@std_msgs/msg/Float64@ignition.msgs.Double",
            "/model/rov/joint/thruster_bottom_front_left_body_blade_joint/cmd_thrust"
            "@std_msgs/msg/Float64@ignition.msgs.Double",
            "/model/rov/joint/thruster_bottom_front_right_body_blade_joint/cmd_thrust"
            "@std_msgs/msg/Float64@ignition.msgs.Double",
            "/model/rov/joint/thruster_bottom_back_left_body_blade_joint/cmd_thrust"
            "@std_msgs/msg/Float64@ignition.msgs.Double",
            "/model/rov/joint/thruster_bottom_back_right_body_blade_joint/cmd_thrust"
            "@std_msgs/msg/Float64@ignition.msgs.Double",
        ],
        remappings=[
            ("/model/rov/joint/thruster_top_front_left_body_blade_joint/cmd_thrust",
             f"/{NS}/model/rov/joint/thruster_top_front_left_body_blade_joint/cmd_thrust"),
            ("/model/rov/joint/thruster_top_front_right_body_blade_joint/cmd_thrust",
             f"/{NS}/model/rov/joint/thruster_top_front_right_body_blade_joint/cmd_thrust"),
            ("/model/rov/joint/thruster_top_back_left_body_blade_joint/cmd_thrust",
             f"/{NS}/model/rov/joint/thruster_top_back_left_body_blade_joint/cmd_thrust"),
            ("/model/rov/joint/thruster_top_back_right_body_blade_joint/cmd_thrust",
             f"/{NS}/model/rov/joint/thruster_top_back_right_body_blade_joint/cmd_thrust"),
            ("/model/rov/joint/thruster_bottom_front_left_body_blade_joint/cmd_thrust",
             f"/{NS}/model/rov/joint/thruster_bottom_front_left_body_blade_joint/cmd_thrust"),
            ("/model/rov/joint/thruster_bottom_front_right_body_blade_joint/cmd_thrust",
             f"/{NS}/model/rov/joint/thruster_bottom_front_right_body_blade_joint/cmd_thrust"),
            ("/model/rov/joint/thruster_bottom_back_left_body_blade_joint/cmd_thrust",
             f"/{NS}/model/rov/joint/thruster_bottom_back_left_body_blade_joint/cmd_thrust"),
            ("/model/rov/joint/thruster_bottom_back_right_body_blade_joint/cmd_thrust",
             f"/{NS}/model/rov/joint/thruster_bottom_back_right_body_blade_joint/cmd_thrust"),
        ],
        output="screen",
    )

    cam_bridge = Node(
        package="ros_ign_bridge",
        executable="parameter_bridge",
        namespace=NS,
        name="cam_bridge",
        arguments=[
            "/bottom_cam/image_raw@sensor_msgs/msg/Image@ignition.msgs.Image",
            "/front_cam/image_raw@sensor_msgs/msg/Image@ignition.msgs.Image",
            "/manip_cam/image_raw@sensor_msgs/msg/Image@ignition.msgs.Image",
            "/depth_cam@sensor_msgs/msg/Image@ignition.msgs.Image",
            "/depth_cam/points@sensor_msgs/msg/PointCloud2@ignition.msgs.PointCloudPacked",
        ],
        remappings=[
            ("/bottom_cam/image_raw", f"/{NS}/bottom_cam/image_raw"),
            ("/front_cam/image_raw", f"/{NS}/front_cam/image_raw"),
            ("/manip_cam/image_raw", f"/{NS}/manip_cam/image_raw"),
            ("/depth_cam/image_raw", f"/{NS}/depth_cam"),
            ("/depth_cam/points", f"/{NS}/depth_cam/points"),
        ],
        output="screen",
    )

        output="screen",
    )

    thruster_controller = Node(
        package="rov_gazebo",
        executable="thruster_controller_node",
        output="screen",
        namespace=NS,
        remappings=[(f"/{NS}/manual_control", '/manual_control')]
    )

    # Launches Controller
    surface_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(
                surface_main_path, 'launch', 'surface_all_nodes_launch.py'
            )
        ]),
    )

    return LaunchDescription(
        [gazeboLaunch,
         keyboard_driver,
         thrust_bridge,
         cam_bridge,
         thruster_controller,
         surface_launch]
    )
