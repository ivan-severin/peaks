from __future__ import print_function

import numpy as np
import peakutils
import pylab

from scipy.signal import savgol_filter



class Spetrumn(object):
    x = np.array
    y = np.array

    # Additional data
    smooth_y = np.array
    baseline = np.array
    indexes = np.array
    peaks = np.array
    fwhm = np.array

    def __init__(sel):
        pass

    def calc_run(self, x_data, y_data, dd=50):
        try:
            if len(x_data) != len(y_data):
                raise ValueError("len %d != %d" % (x_data, y_data))

        except Exception as e:
            print(e)

        self.x = x_data[dd:]
        self.y = y_data[dd:]

        self.calc_baseline()
        self.calc_peak_indexes(limit_peaks=True)
        self.calc_fwhm()

    def get_peaks(self, interpolate=False):
        return peakutils.interpolate(self.x, self.y, ind=self.indexes)

    def get_smoothed_peaks(self, interpolate=False):
        return peakutils.interpolate(self.x, self.y_smooth, ind=self.indexes)

    def calc_fwhm(self):
        self.fwhm = np.zeros(self.indexes.shape)
        for i, ind in enumerate(self.indexes):
            self.fwhm[i] = (self.fwhm3(peakpos=ind, baseline=self.baseline[ind]))

    def calc_baseline(self, order=0):
        """
        Get Baseline
        :param order: polynomial order
        :return: baseline array np.ndarray()
        """
        self.baseline = np.zeros(self.y.shape)
        self.baseline = peakutils.baseline(self.y, deg=order)

    def calc_peak_indexes(self, thres=0.3, min_dist=50, window=15, order=5, limit_peaks=False):
        """

        :param thres:
        :param min_dist:
        :param window: window_length for Savitsky-Golay filter
        :param order: polynom order for Savitsky-Golay filter
        :param limit_peaks: do i need malke less then 4 peak ?
        :return: Nothing
        """
        self.y_smooth = savgol_filter(self.y, window_length=window, polyorder=order)

        # Detect Peaks
        self.indexes = peakutils.indexes(self.y_smooth, thres=thres + 0.01, min_dist=min_dist)

        if limit_peaks and len(self.indexes) > 4:
            self.indexes = peakutils.indexes(self.y_smooth, thres=thres + 0.3, min_dist=min_dist + 20)

    def fwhm3(self, peakpos=-1, baseline=0.):
        """
        calculates the full width at half maximum (fwhm) of some curve.
        the function will return the fwhm with sub-pixel interpolation.
         It will start at the maximum position and 'walk' left and right until it approaches the half values.
        INPUT:
        - valuelist: e.g. the list containing the temporal shape of a pulse
        OPTIONAL INPUT:
        -peakpos: position of the peak to examine (list index)
        the global maximum will be used if omitted.
        OUTPUT:
        -fwhm (value)
        """
        if peakpos == -1:  # no peakpos given -> take maximum
            peak = np.max(self.y)
            peakpos = np.min(np.nonzero(self.y == peak))

        peakvalue = self.y[peakpos]
        phalf = (peakvalue + baseline) / 2.0

        # go left and right, starting from peakpos
        ind1 = peakpos
        ind2 = peakpos

        while ind1 > 2 and self.y[ind1] > phalf:
            ind1 = ind1 - 1
        while ind2 < len(self.y) - 1 and self.y[ind2] > phalf:
            ind2 = ind2 + 1

        grad1 = self.y[ind1 + 1] - self.y[ind1]
        grad2 = self.y[ind2] - self.y[ind2 - 1]

        # calculate the linear interpolations
        p1interp = ind1 + (phalf - self.y[ind1]) / grad1
        p2interp = ind2 + (phalf - self.y[ind2]) / grad2

        # calculate the width
        try:
            width = self.x[int(p2interp)] - self.x[int(p1interp)]
        except IndexError as err:
            print('Problem with Indexes. Probably here is no max.')
            print(err)
            width = 0

        return width

    def plot_all(self, nm=False):
        """
        Plots graphics:
        :param: xd, yd: main spectrum data
        """
        # pylab.title=t_name
        # pylab.figure(figsize=(4.5, 8))

        if max(self.x) > 1000.:
            units = '1/cm'
        #     x = 18796.99 - self.x / 1e7
        else:
            #     x = 1e7 / (18796.99-self.x)
            units = 'nm'
        #     # xd = xd +532
        # try:

        # pylab.plot(self.x, self.y, lw=0.5, color='b')

        pylab.plot(self.x, self.y_smooth, lw=0.5, color='r')

        # pylab.plot(self.x, self.baseline, color='g')

        peaks_x = self.x[self.indexes]

        n = 0
        for i in range(len(peaks_x)):
            pylab.annotate("%0.1f" % (peaks_x[n]), (peaks_x[n], self.y[i]))
            pylab.axvline(peaks_x[n], color='g')
            n += 1
        pylab.xlabel(units)
        pylab.ylabel('Intensity, arb. u.')
