import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import LaserScan
import math
from visualization_msgs.msg import Marker, MarkerArray
from rclpy.duration import Duration



class CylDetector(Node):
    def __init__(self):
        super().__init__('cylinderss')
        self.sub = self.create_subscription(
            LaserScan, '/scan', self.scan_cyl, qos_profile_sensor_data)
        self.r = 0.15 # Radio del cilindro
        self.pub = self.create_publisher(MarkerArray, '/landmarks', 10)

    def scan_cyl(self, msg):
        points = []
        for i, d in enumerate(msg.ranges):
            if msg.range_min < d < msg.range_max:
                theta = msg.angle_min + i * msg.angle_increment
                x = d * math.cos(theta)
                y = d * math.sin(theta)
                points.append((x, y))

        groups = self.group_points(points)
        centers = [self.estimate_center(g) for g in groups]
        txt = ', '.join(f'({cx:.2f}, {cy:.2f})' for cx, cy in centers)
        self.get_logger().info(f'{len(centers)} cilindros: {txt}')

        markers = MarkerArray()
        for k, (cx, cy) in enumerate(centers):
            m = Marker()
            m.header.frame_id = msg.header.frame_id
            m.header.stamp = msg.header.stamp
            m.ns = 'landmarks'
            m.id = k
            m.type = Marker.CYLINDER
            m.action = Marker.ADD
            m.pose.position.x = cx
            m.pose.position.y = cy
            m.pose.position.z = 0.0
            m.pose.orientation.w = 1.0
            m.scale.x = 2 * self.r
            m.scale.y = 2 * self.r
            m.scale.z = 0.5
            m.color.r = 0.0
            m.color.g = 0.8
            m.color.b = 0.2
            m.color.a = 0.6
            m.lifetime = Duration(seconds=0.5).to_msg()
            markers.markers.append(m)
        self.pub.publish(markers)






    def group_points(self, points, margin=0.2):
        if not points:
            return []

        groups = []
        current = [points[0]]
        # Idea: comparamos el punto actual con el anterior del grupo. Si no está "tan lejos",
        # lo incluimos dentro del mismo grupo
        for p in points[1:]:
            prev = current[-1]
            dist = math.hypot(p[0] - prev[0], p[1] - prev[1])

            if dist < margin:
                current.append(p)
            else:
                groups.append(current)
                current = [p]

        groups.append(current)
        return groups

    def estimate_center(self, group):
        # Obtenemos el ángulo entre el robot y el punto promedio de los puntos de un grupo
        mx = sum(p[0] for p in group) / len(group)
        my = sum(p[1] for p in group) / len(group)
        ang = math.atan2(my, mx)

        # Pto más cercano + radio
        d_min = min(math.hypot(p[0], p[1]) for p in group)
        D = d_min + self.r

        # Pasamos a coords cartesianas
        cx = D * math.cos(ang)
        cy = D * math.sin(ang)
        return (cx, cy)




def main():
    rclpy.init()
    node = CylDetector()
    rclpy.spin(node)


if __name__ == '__main__':
    main()