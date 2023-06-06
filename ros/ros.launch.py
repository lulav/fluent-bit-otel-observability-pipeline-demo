from launch import LaunchDescription, launch_description_sources
import subprocess
import time
from launch_ros.actions import Node
from launch.actions import ExecuteProcess, EmitEvent, IncludeLaunchDescription, DeclareLaunchArgument, OpaqueFunction, RegisterEventHandler, LogInfo, TimerAction
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import FrontendLaunchDescriptionSource
from launch.event_handlers import OnExecutionComplete, OnProcessExit, OnProcessIO, OnProcessStart, OnShutdown
from launch.events import Shutdown, process
import os

class bcolors:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def generate_launch_description():

    node_talker = Node(
                    package='demo_nodes_cpp',
                    executable='talker',
                    name='talker',
                    output='screen',
                    emulate_tty=True
                   )

    node_listener = Node(
                    package='demo_nodes_cpp',
                    executable='listener',
                    name='listener',
                    output='screen',
                    emulate_tty=True
                   )

    # proc_fluentbit = ExecuteProcess(
    #                 cmd=[['docker-compose up --build']],
    #                 shell=True,
    #                 name='fluent-bit',
    #                 output='screen',
    #                 emulate_tty=True
    #     )
    
    sys_shut_down = RegisterEventHandler(OnProcessExit(
		target_action=node_talker,
        on_exit=[
                    LogInfo(msg=(f'{bcolors.OKGREEN}The Scenario has ended!{bcolors.ENDC}')),
                    EmitEvent(event=Shutdown(
                        reason='Finished'))
		        ]		
	    ))

    bridge_dir = get_package_share_directory('rosbridge_server')
    node_rosbridge =  IncludeLaunchDescription(launch_description_sources.FrontendLaunchDescriptionSource(bridge_dir + '/launch/rosbridge_websocket_launch.xml')) 
    
    ld = LaunchDescription([node_talker, node_listener, node_rosbridge, sys_shut_down])
    return ld