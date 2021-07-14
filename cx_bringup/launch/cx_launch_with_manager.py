import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    bringup_dir = get_package_share_directory('cx_bringup')

    namespace = LaunchConfiguration('namespace')
    cx_params_file = LaunchConfiguration('cx_params_file')
    clips_executive_params_file = LaunchConfiguration(
        'clips_executive_params_file')

    lc_nodes = ["clips_manager",
                "clips_features_manager", "clips_executive"]

    stdout_linebuf_envvar = SetEnvironmentVariable(
        'RCUTILS_LOGGING_BUFFERED_STREAM', '1')

    declare_namespace_ = DeclareLaunchArgument(
        'namespace', default_value='',
        description='Default namespace')

    declare_cx_params_file = DeclareLaunchArgument(
        'cx_params_file',
        default_value=os.path.join(bringup_dir, 'params', 'cx_params.yaml'),
        description='Path to the ROS2 cx_params.yaml file')

    declare_clips_executive_params_file = DeclareLaunchArgument(
        'clips_executive_params_file',
        default_value=os.path.join(
            bringup_dir, 'params', 'clips-executive.yaml'),
        description='Path to Clips Executive params file')

    cx_clips_node_ = Node(
        package='cx_clips',
        executable='clips_node',
        name='clips_manager',
        output='screen',
        namespace=namespace,
        parameters=[cx_params_file],
    )

    cx_features_node_ = Node(
        package='cx_features',
        executable='features_node',
        name='clips_features_manager',
        output='screen',
        namespace=namespace,
        parameters=[cx_params_file],
    )

    cx_clips_executive_node_ = Node(
        package='cx_clips_executive',
        executable='clips_executive_node',
        name='clips_executive',
        output='screen',
        namespace=namespace,
        parameters=[clips_executive_params_file],
    )

    cx_lifecycle_manager = Node(
        package='cx_lifecycle_nodes_manager',
        executable='lifecycle_manager_node',
        name='cx_lifecycle_manager',
        output='screen',
        namespace=namespace,
        parameters=[{"node_names_to_manage": lc_nodes}],
    )

    # The lauchdescription to populate with defined CMDS
    ld = LaunchDescription()

    ld.add_action(stdout_linebuf_envvar)

    ld.add_action(declare_namespace_)
    ld.add_action(declare_cx_params_file)
    ld.add_action(declare_clips_executive_params_file)

    ld.add_action(cx_clips_node_)
    ld.add_action(cx_features_node_)
    ld.add_action(cx_clips_executive_node_)
    ld.add_action(cx_lifecycle_manager)

    return ld
