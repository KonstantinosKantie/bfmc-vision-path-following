"""
Graph-based path following using a Stanley Controller.
Developed in collaboration with NLattas and Vaios Kakae.
"""
import math
import numpy as np
from sympy import Point, Line
from xy_to_node import load_graph_positions, node_id_to_xy


def odometry_following(graph_path, now_node, now_coords, next_node):
    """
    Computes the required steering angle to follow the path segment
    between `now_node` and `next_node` using a Stanley-based controller.
    """
    ids, coords = load_graph_positions(graph_path)

    now_node_coords = node_id_to_xy(now_node, ids, coords)
    next_node_coords = node_id_to_xy(next_node, ids, coords)

    p1 = Point(float(now_node_coords[0]), float(now_node_coords[1]))
    p2 = Point(float(next_node_coords[0]), float(next_node_coords[1]))

    if p1 == p2:
        print("Current node and next node are the same. No movement needed.")
        return 0.0

    direction = Point(math.cos(now_coords[2]), math.sin(now_coords[2]))
    p3 = Point(float(now_coords[0]), float(now_coords[1]))
    p4 = p3 + direction

    s1 = Line(p1, p2)  # Reference path segment
    s2 = Line(p3, p4)  # Vehicle heading vector

    heading_error = float(s1.angle_between(s2))
    crosstrack_error = float(s1.distance(p3))

    return stanley_correction(crosstrack_error, heading_error, K=0.14, velocity=100)


def stanley_correction(crosstrack_error, heading_error, K, velocity):
    """
    Stanley controller steering correction (crosstrack error in pixels).
    """
    max_steer = 250
    desired_steering_angle = 3 * (-1.3 * heading_error - 57 * K * crosstrack_error / float(velocity))
    limited_steering_angle = np.clip(desired_steering_angle, -max_steer, max_steer)
    return round(float(limited_steering_angle), 1)
    