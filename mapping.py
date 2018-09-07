import numpy as np
# import seaborn as sns
import matplotlib.pyplot as plt

from spectrum import Spetrumn
from configparser import ConfigParser


class Mapping(object):
    """docstring for Mapping"""
    # self.filename
    source_name = 'None'
    graph_name = 'None'
    size_x = 0
    size_y = 0
    size_graph = 0
    data_unit = ''
    x_axis = np.empty(0)
    y_axis = np.empty(0)

    def __init__(self, filename):
        basename = ' '.join(filename.split(' ')[:-1])
        tile_header = ' (Header).txt'
        tile_x_axis = ' (X-Axis).txt'
        tile_y_axis = ' (Y-Axis).txt'

        self.read_header(file_name=basename + tile_header)
        self.read_x_axis(file_name=basename + tile_x_axis)
        self.read_y_axis(file_name=basename + tile_y_axis)
        self.plot_heatmap()
        # self.gen_heatmap(300,400)
        self.plot()

    def __find_nearest(self, value):
        idx = (np.abs(self.x_axis - value)).argmin()
        print("nearest x_array[", idx, "] = ", self.x_axis[idx], "==", value)
        if idx == 0 or idx == self.size_x:
            raise ValueError("nearest not found! val: " + str(value)
                             + "x_axis[" + str(idx) + "]: " + str(self.x_axis[idx]))
        return idx

    def read_header(self, file_name):
        config = ConfigParser(comment_prefixes=('//', '#', ';'))
        config.read(file_name)

        self.source_name = config.get('Header', 'FileName')
        self.graph_name = config.get('Header', 'GraphName')
        self.size_x = config.getint('Header', 'SizeX')
        self.size_y = config.getint('Header', 'Sizey')
        self.size_graph = config.getint('Header', 'SizeGraph')
        self.data_unit = config.get('Header', 'DataUnit')

        print("source_name=", self.source_name)
        print("graph_name =", self.graph_name)
        print("size_x     =", self.size_x)
        print("size_y     =", self.size_y)
        print("size_graph =", self.size_graph)
        print("data_unit  =", self.data_unit)

    def read_x_axis(self, file_name):
        self.x_axis = np.loadtxt(file_name)
        print("x-axis: ", type(self.x_axis))
        print("x-axis.size: ", self.x_axis.size)
        print("x-axis[:5]: ", self.x_axis[:5])

    def read_y_axis(self, file_name):
        self.y_axis = np.loadtxt(file_name).reshape((self.size_x,
                                                     self.size_y,
                                                     self.size_graph))

        print("y-axis: ", type(self.y_axis))
        print("y-axis.shape: ", self.y_axis.shape)

    def gen_heatmap(self, ind_begin, ind_end, method=None):
        try:
            ind_beg = int(ind_begin)
            ind_end = int(ind_end)
            if ind_beg > ind_end:
                raise ValueError("index" + str(ind_begin) + " bigger then " + str(ind_end))

            # TODO: Add handling method

        except Exception as e:
            print(e)
            return np.zeros()

        heatmap = np.zeros((self.size_x, self.size_y))

        heatmap = self.y_axis[:, :, ind_beg:ind_end]

        print("Heatmap shape:", heatmap.shape)
        heatmap = np.average(heatmap, axis=2)
        print("Avereged Heatmap shape:", heatmap.shape)
        return heatmap

    def plot(self):
        pass

        # spec = Spetrumn(self.x_axis, self.y_axis[16, 5])
        # plt.plot(spec.x, spec.y)
        # print("baseline shape:", spec.baseline.shape)
        # print("baseline:", spec.baseline[:5])
        #
        # print("indexes shape:", spec.indexes.shape)
        # print("indexes:", spec.indexes[:5])
        #
        # print("fwhm shape:", spec.fwhm.shape)
        # print("fwhm:", spec.fwhm[:5])

        # spec.plot_all()


        # plt.show()
        # for i, ival in enumerate(spec.y[])


    def plot_heatmap(self):
        pass
        # ax = sns.heatmap(self.gen_heatmap(500, 600), cmap="YlGnBu")

        # plt.show()


