import rclpy
from rclpy.node import Node


class MavlinkInterface(Node):

    def __init__(self):
        super().__init__('mavlink_interface')


def main(args=None):
    rclpy.init(args=args)

    mavlink_interface = MavlinkInterface()

    rclpy.logging.initialize()
    rclpy.logging.get_logger('test').info("Node running")

    rclpy.spin(mavlink_interface)

    mavlink_interface.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
