from typing import List, Tuple
import matplotlib.pyplot as plt
import numpy as np
from catmull_rom_things import sample_catmull_rom_spline


def read_alpha_carbon_positions(filename: str) -> List[Tuple[float, float, float]]:
    with open(filename, 'rt') as file:
        lines = file.read().split('\n')

    atom_lines = [x for x in lines if x[:4] == 'ATOM']
    ca_lines = [x for x in atom_lines if x[12:16].strip() == 'CA']

    ca_positions: List[Tuple[float, float, float]] = []

    for ca_line in ca_lines:
        x_string = ca_line[30:38].strip()
        y_string = ca_line[38:45].strip()
        z_string = ca_line[46:54].strip()

        x_float = float(x_string)
        y_float = float(y_string)
        z_float = float(z_string)

        position = (x_float, y_float, z_float)

        ca_positions.append(position)

    return ca_positions


if __name__ == '__main__':
    ca_positions = read_alpha_carbon_positions('8e28.pdb')

    points = sample_catmull_rom_spline(ca_positions, 10)

    ax = plt.subplot(projection='3d')

    xs = [pos[0] for pos in points]
    ys = [pos[1] for pos in points]
    zs = [pos[2] for pos in points]

    ax.plot(xs, ys, zs, label='CA trace - linear')
    plt.show()

    ax_2 = plt.subplot(projection='3d')
