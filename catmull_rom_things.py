from typing import List, Tuple
import numpy as np

Vector = Tuple[float, float, float]
ControlPointSet = Tuple[Vector, Vector, Vector, Vector]

def _get_next_t(
        current_t: float,
        first_control_point: Vector,
        second_control_point: Vector
) -> float:
    x, y, z = first_control_point
    next_x, next_y, next_z = second_control_point
    dx, dy, dz = next_x - x, next_y - y, next_z - z
    l = np.sqrt((dx ** 2 + dy ** 2 + dz ** 2))
    return current_t + np.sqrt(l)


def sample_catmull_rom_segment(
        control_point_set: ControlPointSet,
        point_count: int
) -> List[Vector]:

    p_0, p_1, p_2, p_3 = control_point_set

    t_0 = 0.0
    t_1 = _get_next_t(t_0, p_0, p_1)
    t_2 = _get_next_t(t_1, p_1, p_2)
    t_3 = _get_next_t(t_2, p_2, p_3)
    t = np.linspace(t_1, t_2, point_count).reshape(point_count, 1)

    a_0 = (t_1 - t) / (t_1 - t_0) * p_0 + (t - t_0) / (t_1 - t_0) * p_1
    a_1 = (t_2 - t) / (t_2 - t_1) * p_1 + (t - t_1) / (t_2 - t_1) * p_2
    a_2 = (t_3 - t) / (t_3 - t_2) * p_2 + (t - t_2) / (t_3 - t_2) * p_3

    b_0 = (t_2 - t) / (t_2 - t_0) * a_0 + (t - t_0) / (t_2 - t_0) * a_1
    b_1 = (t_3 - t) / (t_3 - t_1) * a_1 + (t - t_1) / (t_3 - t_1) * a_2

    points = (t_2 - t) / (t_2 - t_1) * b_0 + (t - t_1) / (t_2 - t_1) * b_1
    return points


def _points_to_control_point_sets(points: List[Vector]) -> List[ControlPointSet]:
    control_point_sets: List[ControlPointSet] = []

    for i in range(len(points) - 3):
        control_point_set = (
            points[i],
            points[i + 1],
            points[i + 2],
            points[i + 3]
        )
        control_point_sets.append(control_point_set)

    return control_point_sets


def sample_catmull_rom_spline(points: List[Vector], samples_per_segment: int) -> List[Vector]:
    control_point_sets = _points_to_control_point_sets(points)
    samples: List[Vector] = []

    for i in range(len(control_point_sets)):
        control_point_set = control_point_sets[i]
        segment = list(sample_catmull_rom_segment(control_point_set, samples_per_segment))

        if i != 0:
            segment.pop(0)
        if i != len(control_point_sets) - 1:
            segment.pop(-1)

        samples += segment

    return samples
