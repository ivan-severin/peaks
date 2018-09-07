from mapping import Mapping
from mapping import Spetrumn
import numpy as np

if __name__ == '__main__':
    m = Mapping('data/1 Export File (Header).txt')
    comps = np.zeros((m.size_x, m.size_y, 5))
    Ni, Nj = m.y_axis.shape[0], m.y_axis.shape[1]

    # try:
    for i in range(Ni):
        for j in range(Nj):
            print("\n\n\n i: ", i, "j: ", j)
            spec = Spetrumn()
            spec.calc_run(m.x_axis, m.y_axis[i, j])
            print("baseline shape:", spec.baseline.shape)
            print("baseline:", spec.baseline[:5])

            print("indexes shape:", spec.indexes.shape)
            print("indexes:", spec.indexes[:5])

            print("fwhm shape:", spec.fwhm.shape)
            print("fwhm:", spec.fwhm[:5])
    # except Exception as e:
    #      print(e)

    # print(Ni, Nk)