import rclpy
from rclpy.node import Node

from std_msgs.msg import String


class MavlinkInterface(Node):

    def __init__(self):
        super().__init__('mavlink_interface')


def main(args=None):
    rclpy.init(args=args)

    mavlink_interface = MavlinkInterface()

    rclpy.spin(mavlink_interface)

    mavlink_interface.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
