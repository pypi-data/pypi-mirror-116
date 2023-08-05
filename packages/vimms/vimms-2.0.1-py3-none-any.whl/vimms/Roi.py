import bisect
import sys
from collections import OrderedDict

import pandas as pd
import pylab as plt
import pymzml
import statsmodels.api as sm
from loguru import logger
from mass_spec_utils.data_processing.alignment import Peak, PeakSet
from scipy.stats import pearsonr

from vimms.Box import GenericBox
# from vimms.Chemicals import ChemicalCreator, UnknownChemical
from vimms.Chromatograms import EmpiricalChromatogram
from vimms.Common import PROTON_MASS
from vimms.Evaluation import *

POS_TRANSFORMATIONS = OrderedDict()
POS_TRANSFORMATIONS['M+H'] = lambda mz: (mz + PROTON_MASS)
POS_TRANSFORMATIONS['[M+ACN]+H'] = lambda mz: (mz + 42.033823)
POS_TRANSFORMATIONS['[M+CH3OH]+H'] = lambda mz: (mz + 33.033489)
POS_TRANSFORMATIONS['[M+NH3]+H'] = lambda mz: (mz + 18.033823)
POS_TRANSFORMATIONS['M+Na'] = lambda mz: (mz + 22.989218)
POS_TRANSFORMATIONS['M+K'] = lambda mz: (mz + 38.963158)
POS_TRANSFORMATIONS['M+2Na-H'] = lambda mz: (mz + 44.971160)
POS_TRANSFORMATIONS['M+ACN+Na'] = lambda mz: (mz + 64.015765)
POS_TRANSFORMATIONS['M+2Na-H'] = lambda mz: (mz + 44.971160)
POS_TRANSFORMATIONS['M+2K+H'] = lambda mz: (mz + 76.919040)
POS_TRANSFORMATIONS['[M+DMSO]+H'] = lambda mz: (mz + 79.02122)
POS_TRANSFORMATIONS['[M+2ACN]+H'] = lambda mz: (mz + 83.060370)
POS_TRANSFORMATIONS['2M+H'] = lambda mz: (mz * 2) + 1.007276
POS_TRANSFORMATIONS['M+ACN+Na'] = lambda mz: (mz + 64.015765)
POS_TRANSFORMATIONS['2M+NH4'] = lambda mz: (mz * 2) + 18.033823


# Object to store a RoI
# Maintains 3 lists -- mz, rt and intensity
# When a new point (mz,rt,intensity) is added, it updates the 
# list and the mean mz which is required.
class Roi(object):
    def __init__(self, mz, rt, intensity, id=None):
        self.id = id
        self.fragmentation_events = []
        self.fragmentation_intensities = []
        self.max_fragmentation_intensity = 0.0
        if type(mz) == list:
            self.mz_list = mz
        else:
            self.mz_list = [mz]
        if type(rt) == list:
            self.rt_list = rt
        else:
            self.rt_list = [rt]
        if type(intensity) == list:
            self.intensity_list = intensity
        else:
            self.intensity_list = [intensity]
        self.n = len(self.mz_list)
        self.mz_sum = sum(self.mz_list)
        self.length_in_seconds = self.rt_list[-1] - self.rt_list[0]
        self.is_fragmented = False
        self.can_fragment = True

    def fragmented(self):
        self.is_fragmented = True
        self.can_fragment = True

    def get_mean_mz(self):
        return self.mz_sum / self.n

    def get_max_intensity(self):
        return max(self.intensity_list)

    def get_min_intensity(self):
        return min(self.intensity_list)

    def get_autocorrelation(self, lag=1):
        return pd.Series(self.intensity_list).autocorr(lag=lag)

    def get_nth_point(self, n):
        if (n >= len(self.rt_list)): return None
        return self.rt_list[n], self.mz_list[n], self.intensity_list[n]

    def estimate_apex(self):
        return self.rt_list[np.argmax(self.intensity_list)]

    def add(self, mz, rt, intensity):
        self.mz_list.append(mz)
        self.rt_list.append(rt)
        self.intensity_list.append(intensity)
        self.mz_sum += mz
        self.n += 1
        self.length_in_seconds = self.rt_list[-1] - self.rt_list[0]

    def add_fragmentation_event(self, scan, precursor_intensity):
        self.fragmentation_events.append(scan)
        self.fragmentation_intensities.append(precursor_intensity)
        self.max_fragmentation_intensity = max(self.fragmentation_intensities)

    def __lt__(self, other):
        return self.get_mean_mz() <= other.get_mean_mz()

    def to_chromatogram(self):
        if self.n == 0:
            return None
        chrom = EmpiricalChromatogram(np.array(self.rt_list), np.array(self.mz_list), np.array(self.intensity_list))
        return chrom

    def __repr__(self):
        return 'ROI with data points=%d fragmentations=%d mz (%.4f-%.4f) rt (%.4f-%.4f)' % (
            self.n,
            len(self.fragmentation_events),
            self.mz_list[0], self.mz_list[-1],
            self.rt_list[0], self.rt_list[-1])

    def to_box(self, min_rt_width, min_mz_width, rt_shift=0, mz_shift=0):
        return GenericBox(min(self.rt_list) + rt_shift, max(self.rt_list) + rt_shift, min(self.mz_list) + mz_shift,
                          max(self.mz_list) + mz_shift,
                          min_xwidth=min_rt_width, min_ywidth=min_mz_width, intensity=self.max_fragmentation_intensity)

    def get_boxes_overlap(self, boxes, min_rt_width, min_mz_width, rt_shift=0, mz_shift=0):
        roi_box = self.to_box(min_rt_width, min_mz_width, rt_shift, mz_shift)
        # print(roi_box)
        overlaps = [roi_box.overlap_2(box) for box in boxes]
        return overlaps

    def get_roi_overlap(self, boxes, min_rt_width, min_mz_width, rt_shift=0, mz_shift=0):
        roi_box = self.to_box(min_rt_width, min_mz_width, rt_shift, mz_shift)
        overlaps = [roi_box.overlap_3(box) for box in boxes]
        return overlaps

    def get_last_datum(self):
        return (self.mz_list[-1], self.rt_list[-1], self.intensity_list[-1])


class SmartRoi(Roi):
    INITIAL_WAITING = 0
    CAN_FRAGMENT = 1
    AFTER_FRAGMENT = 2
    POST_PEAK = 3

    def __init__(self, mz, rt, intensity, initial_length_seconds=5, reset_length_seconds=100,
                 intensity_increase_factor=2, dew=15, drop_perc=0.01, id=None):
        super().__init__(mz, rt, intensity, id=id)

        if initial_length_seconds > 0:
            self.status = SmartRoi.INITIAL_WAITING
            self.set_can_fragment(False)
        else:
            self.status = SmartRoi.CAN_FRAGMENT
            self.set_can_fragment(True)

        self.min_frag_intensity = None

        self.initial_length_seconds = initial_length_seconds
        self.reset_length_seconds = reset_length_seconds
        self.intensity_increase_factor = intensity_increase_factor
        self.drop_perc = drop_perc
        self.dew = dew

    def fragmented(self):
        self.is_fragmented = True
        self.set_can_fragment(False)
        self.fragmented_index = len(self.mz_list) - 1
        self.status = SmartRoi.AFTER_FRAGMENT

    def get_status(self):
        if self.status == 0:
            return "INITIAL_WAITING"
        elif self.status == 1:
            return "CAN_FRAGMENT"
        elif self.status == 2:
            return "AFTER_FRAGMENT"
        elif self.status == 3:
            return "POST_PEAK"

    def add(self, mz, rt, intensity):
        super().add(mz, rt, intensity)
        if self.status == SmartRoi.INITIAL_WAITING:
            if self.length_in_seconds >= self.initial_length_seconds:
                self.status = SmartRoi.CAN_FRAGMENT
                self.set_can_fragment(True)
        elif self.status == SmartRoi.AFTER_FRAGMENT:
            # in a period after a fragmentation has happened
            # if enough time has elapsed, reset everything
            if self.rt_list[-1] - self.rt_list[self.fragmented_index] > self.reset_length_seconds:
                self.status = SmartRoi.CAN_FRAGMENT
                self.set_can_fragment(True)
            elif self.rt_list[-1] - self.rt_list[self.fragmented_index] > self.dew:
                # standard DEW has expired
                # find the min intensity since the frag
                # check current intensity -- if it is 5* when we fragmented, we can go again
                min_since_frag = min(self.intensity_list[self.fragmented_index:])
                if self.intensity_list[-1] > min_since_frag * self.intensity_increase_factor:
                    self.status = SmartRoi.CAN_FRAGMENT
                    self.set_can_fragment(True)
                elif self.intensity_list[-1] < self.drop_perc * self.intensity_list[self.fragmented_index]:
                    # signal has dropped, but ROI still exists.
                    self.status = SmartRoi.CAN_FRAGMENT
                    self.set_can_fragment(True)
                    # self.min_frag_intensity = self.intensity_list[-1]*self.intensity_increase_factor

        # code below never happens
        elif self.status == SmartRoi.POST_PEAK:
            if self.rt_list[-1] - self.rt_list[self.fragmented_index] > self.dew:
                if self.intensity_list[-1] > self.min_frag_intensity:
                    self.status = SmartRoi.CAN_FRAGMENT
                    self.set_can_fragment(True)

    def get_can_fragment(self):
        return self.can_fragment

    def set_can_fragment(self, status):
        self.can_fragment = status


# Find the RoI that a particular mz falls into
# If it falls into nothing, return None
# mz_tol is the window above and below the 
# mean_mz of the RoI. E.g. if mz_tol = 1 Da, then it looks
# plus and minus 1Da
def match(mz, roi_list, mz_tol, mz_units='Da'):
    if len(roi_list) == 0:
        return None
    pos = bisect.bisect_right(roi_list, mz)

    if pos == len(roi_list):
        if mz_units == 'Da':
            dist_left = mz.get_mean_mz() - roi_list[pos - 1].get_mean_mz()
        else:  # ppm
            dist_left = 1e6 * (mz.get_mean_mz() - roi_list[pos - 1].get_mean_mz()) / mz.get_mean_mz()

        if dist_left < mz_tol:
            return roi_list[pos - 1]
        else:
            return None
    elif pos == 0:
        if mz_units == 'Da':
            dist_right = roi_list[pos].get_mean_mz() - mz.get_mean_mz()
        else:  # ppm
            dist_right = 1e6 * (roi_list[pos].get_mean_mz() - mz.get_mean_mz()) / mz.get_mean_mz()

        if dist_right < mz_tol:
            return roi_list[pos]
        else:
            return None
    else:
        if mz_units == 'Da':
            dist_left = mz.get_mean_mz() - roi_list[pos - 1].get_mean_mz()
            dist_right = roi_list[pos].get_mean_mz() - mz.get_mean_mz()
        else:  # ppm
            dist_left = 1e6 * (mz.get_mean_mz() - roi_list[pos - 1].get_mean_mz()) / mz.get_mean_mz()
            dist_right = 1e6 * (roi_list[pos].get_mean_mz() - mz.get_mean_mz()) / mz.get_mean_mz()

        if dist_left < mz_tol and dist_right > mz_tol:
            return roi_list[pos - 1]
        elif dist_left > mz_tol and dist_right < mz_tol:
            return roi_list[pos]
        elif dist_left < mz_tol and dist_right < mz_tol:
            if dist_left <= dist_right:
                return roi_list[pos - 1]
            else:
                return roi_list[pos]
        else:
            return None


def roi_correlation(roi1, roi2, min_rt_point_overlap=5, method='pearson'):
    # flip around so that roi1 starts earlier (or equal)
    if roi2.rt_list[0] < roi1.rt_list[0]:
        temp = roi2
        roi2 = roi1
        roi1 = temp

    # check that they meet the min_rt_point overlap
    if roi1.rt_list[-1] < roi2.rt_list[0]:
        # no overlap at all
        return 0.0

    # find the position of the first element in roi2 in roi1
    pos = roi1.rt_list.index(roi2.rt_list[0])

    # print roi1.rt_list
    # print roi2.rt_list
    # print pos

    total_length = max([len(roi1.rt_list), len(roi2.rt_list) + pos])
    # print total_length

    r1 = np.zeros((total_length), np.double)
    r2 = np.zeros_like(r1)

    r1[:len(roi1.rt_list)] = roi1.intensity_list
    r2[pos:pos + len(roi2.rt_list)] = roi2.intensity_list

    # print 
    # for i,a in enumerate(r1):
    #     print "{:10.4f}\t{:10.4f}".format(a,r2[i])
    if method == 'pearson':
        r, _ = pearsonr(r1, r2)
    else:
        r = cosine_score(r1, r2)

    return r


def cosine_score(u, v):
    numerator = (u * v).sum()
    denominator = np.sqrt((u * u).sum()) * np.sqrt((v * v).sum())
    return numerator / denominator


class RoiParams(object):
    def __init__(self, mz_tol=0.001, mz_units='Da', min_length=10, min_intensity=50000, start_rt=0, stop_rt=10000000,
                 length_units="scans", ms_level=1, skip=None):
        self.mz_tol = mz_tol
        self.mz_units = mz_units
        self.min_length = min_length
        self.min_intensity = min_intensity
        self.start_rt = start_rt
        self.stop_rt = stop_rt
        self.length_units = length_units
        self.ms_level = ms_level
        self.skip = skip


# Make the RoI from an input file
# mz_units = Da for Daltons
# mz_units = ppm for ppm
def make_roi(input_file, mz_tol=0.001, mz_units='Da', min_length=10, min_intensity=50000, start_rt=0, stop_rt=10000000,
             length_units="scans", ms_level=1, skip=None):
    # input_file = 'Beer_multibeers_1_fullscan1.mzML'

    if not mz_units == 'Da' and not mz_units == 'ppm':
        logger.warning("Unknown mz units, use Da or ppm")
        return None, None

    run = pymzml.run.Reader(input_file, MS1_Precision=5e-6,
                            extraAccessions=[('MS:1000016', ['value', 'unitName'])],
                            obo_version='4.0.1')

    live_roi = []
    dead_roi = []
    junk_roi = []

    for i, spectrum in enumerate(run):
        # print spectrum['centroid_peaks']
        if skip == 'even' and i % 2 == 0:
            continue
        if skip == 'odd' and i % 2 == 1:
            continue
        if spectrum['ms level'] == ms_level:
            live_roi.sort()
            # current_ms1_scan_rt, units = spectrum['scan start time'] # this no longer works
            current_ms1_scan_rt, units = spectrum.scan_time
            if units == 'minute':
                current_ms1_scan_rt *= 60.0

            if current_ms1_scan_rt < start_rt:
                continue
            if current_ms1_scan_rt > stop_rt:
                break

            # print current_ms1_scan_rt
            # print spectrum.peaks
            not_grew = set(live_roi)
            for mz, intensity in spectrum.peaks('raw'):
                if intensity >= min_intensity:
                    match_roi = match(Roi(mz, 0, 0), live_roi, mz_tol, mz_units=mz_units)
                    if match_roi:
                        match_roi.add(mz, current_ms1_scan_rt, intensity)
                        if match_roi in not_grew:
                            not_grew.remove(match_roi)
                    else:
                        bisect.insort_right(live_roi, Roi(mz, current_ms1_scan_rt, intensity))

            for roi in not_grew:
                if length_units == "scans":
                    if roi.n >= min_length:
                        dead_roi.append(roi)
                    else:
                        junk_roi.append(roi)
                else:
                    if roi.length_in_seconds >= min_length:
                        dead_roi.append(roi)
                    else:
                        junk_roi.append(roi)
                pos = live_roi.index(roi)
                del live_roi[pos]

            # logger.debug("Scan @ {}, {} live ROIs".format(current_ms1_scan_rt, len(live_roi)))

    # process all the live ones - keeping only those that 
    # are longer than the minimum length
    good_roi = dead_roi
    for roi in live_roi:
        if roi.n >= min_length:
            good_roi.append(roi)
        else:
            junk_roi.append(roi)
    return good_roi, junk_roi


def greedy_roi_cluster(roi_list, corr_thresh=0.75, corr_type='cosine'):
    # sort in descending intensity
    roi_list_copy = [r for r in roi_list]
    roi_list_copy.sort(key=lambda x: max(x.intensity_list), reverse=True)
    roi_clusters = []
    while len(roi_list_copy) > 0:
        roi_clusters.append([roi_list_copy[0]])
        remove_idx = [0]
        if len(roi_list_copy) > 1:
            for i, r in enumerate(roi_list_copy[1:]):
                corr = roi_correlation(roi_list_copy[0], r)
                if corr > corr_thresh:
                    roi_clusters[-1].append(r)
                    remove_idx.append(i + 1)
        remove_idx.sort(reverse=True)
        for r in remove_idx:
            del roi_list_copy[r]

    return roi_clusters


def plot_roi(roi, statuses=None, log=False):
    if log:
        intensities = np.log(roi.intensity_list)
        plt.ylabel('Log Intensity')
    else:
        intensities = roi.intensity_list
        plt.ylabel('Intensity')
    if statuses is not None:
        colours = []
        for s in statuses:
            if s == 'Noise':
                colours.append('red')
            elif s == 'Increase':
                colours.append('blue')
            elif s == 'Decrease':
                colours.append('yellow')
            else:
                colours.append('green')
        plt.scatter(roi.rt_list, intensities, color=colours)
    else:
        plt.scatter(roi.rt_list, intensities)
    plt.xlabel('RT')
    plt.show()


class RoiAligner(object):
    def __init__(self, mz_tolerance_absolute=0.01,
                 mz_tolerance_ppm=10,
                 rt_tolerance=0.5,
                 mz_column_pos=1,
                 rt_column_pos=2,
                 intensity_column_pos=3,
                 min_rt_width=0.01,
                 min_mz_width=0.01,
                 n_categories=1):
        self.peaksets = []
        self.mz_tolerance_absolute = mz_tolerance_absolute
        self.mz_tolerance_ppm = mz_tolerance_ppm
        self.rt_tolerance = rt_tolerance
        self.mz_weight = 75
        self.rt_weight = 25
        self.files_loaded = []
        self.mz_column_pos = mz_column_pos
        self.rt_column_pos = rt_column_pos
        self.intensity_column_pos = intensity_column_pos
        self.sample_names = []
        self.sample_types = []
        self.min_rt_width = min_rt_width
        self.min_mz_width = min_mz_width
        self.peaksets2boxes = {}
        self.peaksets2fragintensities = {}
        self.addition_method = None
        self.n_categories = n_categories

    def add_sample(self, rois, sample_name, sample_type=None, rt_shifts=None, mz_shifts=None):
        self.sample_names.append(sample_name)
        self.sample_types.append(sample_type)
        these_peaks = []
        frag_intensities = []
        temp_boxes = []
        for i, roi in enumerate(rois):
            source_id = sample_name + '_' + str(i)
            peak_mz = roi.get_mean_mz()
            peak_rt = roi.estimate_apex()
            peak_intensity = roi.get_max_intensity()
            these_peaks.append(Peak(peak_mz, peak_rt, peak_intensity, sample_name, source_id))
            frag_intensities.append(roi.max_fragmentation_intensity)
            rt_shift = 0 if rt_shifts is None else rt_shifts[i]
            mz_shift = 0 if mz_shifts is None else mz_shifts[i]
            temp_boxes.append(roi.to_box(self.min_rt_width, self.min_mz_width, rt_shift, mz_shift))

        # do alignment, adding the peaks and boxes, and recalculating max frag intensity
        self._align(these_peaks, temp_boxes, frag_intensities, sample_name)

    def add_picked_peaks(self, mzml_file, peak_file, sample_name, picking_method='mzmine', sample_type=None,
                         half_isolation_window=1, allow_last_overlap=False, rt_shifts=None, mz_shifts=None):
        self.sample_names.append(sample_name)
        self.sample_types.append(sample_type)
        these_peaks = []
        frag_intensities = []
        # load boxes
        if picking_method == 'mzmine':
            temp_boxes = load_picked_boxes(peak_file)
        elif picking_method == 'peakonly':
            temp_boxes = load_peakonly_boxes(peak_file)  # not tested
        elif picking_method == 'xcms':
            temp_boxes = load_xcms_boxes(peak_file)  # not tested
        else:
            sys.exit('Method not supported')
        temp_boxes = update_picked_boxes(temp_boxes, rt_shifts, mz_shifts)
        # Searching in boxes
        mzml = MZMLFile(mzml_file)
        scans2boxes, boxes2scans = map_boxes_to_scans(mzml, temp_boxes, half_isolation_window=half_isolation_window,
                                                      allow_last_overlap=allow_last_overlap)
        precursor_intensities, scores = get_precursor_intensities(boxes2scans, temp_boxes, 'max')
        for i, box in enumerate(temp_boxes):
            source_id = sample_name + '_' + str(i)
            peak_mz = box.mz
            peak_rt = box.rt_in_seconds
            these_peaks.append(Peak(peak_mz, peak_rt, box.height, sample_name, source_id))
            frag_intensities.append(precursor_intensities[i])

        # do alignment, adding the peaks and boxes, and recalculating max frag intensity
        self._align(these_peaks, temp_boxes, frag_intensities, sample_name)

    def _align(self, these_peaks, temp_boxes, frag_intensities, short_name):
        if len(self.peaksets) == 0:
            # first file
            for i, peak in enumerate(these_peaks):
                self.peaksets.append(PeakSet(peak))
                self.peaksets2boxes[self.peaksets[-1]] = [temp_boxes[i]]
                self.peaksets2fragintensities[self.peaksets[-1]] = [frag_intensities[i]]
        else:
            for peakset in self.peaksets:
                candidates = list(
                    filter(lambda x: peakset.is_in_box(x[0], self.mz_tolerance_absolute, self.mz_tolerance_ppm,
                                                       self.rt_tolerance),
                           zip(these_peaks, temp_boxes, frag_intensities)))

                if len(candidates) == 0:
                    continue
                else:
                    candidates_peaks, candidates_boxes, candidates_intensities = zip(*candidates)

                    best_peak = None
                    best_box = None
                    best_frag_intensity = None
                    best_score = 0
                    for i, peak in enumerate(candidates_peaks):
                        score = peakset.compute_weight(peak, self.mz_tolerance_absolute, self.mz_tolerance_ppm,
                                                       self.rt_tolerance, self.mz_weight, self.rt_weight)
                        if score > best_score:
                            best_score = score
                            best_peak = peak
                            best_box = candidates_boxes[i]
                            best_frag_intensity = candidates_intensities[i]
                    peakset.add_peak(best_peak)
                    self.peaksets2boxes[peakset].append(best_box)
                    self.peaksets2fragintensities[peakset].append(best_frag_intensity)
                    pos = these_peaks.index(best_peak)
                    del these_peaks[pos]
                    del temp_boxes[pos]
                    del frag_intensities[pos]
            for i, peak in enumerate(these_peaks):  # remaining ones
                self.peaksets.append(PeakSet(peak))
                self.peaksets2boxes[self.peaksets[-1]] = [temp_boxes[i]]
                self.peaksets2fragintensities[self.peaksets[-1]] = [frag_intensities[i]]
        self.files_loaded.append(short_name)

    def to_matrix(self):
        n_peaksets = len(self.peaksets)
        n_files = len(self.files_loaded)
        intensity_matrix = np.zeros((n_peaksets, n_files), np.double)
        for i, peakset in enumerate(self.peaksets):
            for j, filename in enumerate(self.files_loaded):
                intensity_matrix[i, j] = peakset.get_intensity(filename)
        return intensity_matrix

    def get_boxes(self, method='mean'):
        boxes = []
        for ps in self.peaksets:
            box_list = self.peaksets2boxes[ps]
            pt1x = np.array([box.pt1.x for box in box_list])
            pt2x = np.array([box.pt2.x for box in box_list])
            pt1y = np.array([box.pt1.y for box in box_list])
            pt2y = np.array([box.pt2.y for box in box_list])
            intensity = max(self.peaksets2fragintensities[ps])
            if method == 'max':
                x1 = min(pt1x)
                x2 = max(pt2x)
                y1 = min(pt1y)
                y2 = max(pt2y)
            else:
                x1 = np.mean(pt1x)
                x2 = np.mean(pt2x)
                y1 = np.mean(pt1y)
                y2 = np.mean(pt2y)
            boxes.append(GenericBox(x1, x2, y1, y2, intensity=intensity, min_xwidth=self.min_rt_width,
                                    min_ywidth=self.min_mz_width))
        return boxes

    def get_max_frag_intensities(self):
        return [max(self.peaksets2fragintensities[ps]) for ps in self.peaksets]


class FrequentistRoiAligner(RoiAligner):
    def get_boxes(self, method='mean'):
        boxes = super().get_boxes(method)
        categories = np.unique(np.array(self.sample_types))
        enough_categories = min(Counter(self.sample_types).values()) > 1 and len(categories) == self.n_categories
        pvalues = self.get_p_values(enough_categories)
        for i, box in enumerate(boxes):
            box.pvalue = pvalues[i]
        return boxes

    def get_p_values(self, enough_catergories):
        # need to match boxes, not base chemicals
        if enough_catergories:
            p_values = []
            # sort X
            X = np.array(self.to_matrix())
            # sort y
            categories = np.unique(np.array(self.sample_types))
            if self.n_categories == 2:  # logistic regression
                x = np.array([1 for i in self.sample_types])
                if 'control' in categories:
                    control_type = 'control'
                else:
                    control_type = categories[0]
                x[np.where(np.array(self.sample_types) == control_type)] = 0
                x = sm.add_constant(x)
                for i in range(X.shape[0]):
                    y = np.log(X[i, :] + 1)
                    model = sm.OLS(y, x)
                    p_values.append(model.fit(disp=0).pvalues[1])
            else:  # classification
                pass
        else:
            p_values = [None for ps in self.peaksets]
        return p_values


def get_precursor_intensities(boxes2scans, boxes, method):
    assert method in ['max', 'first']
    precursor_intensities = []
    scores = []
    for i, box in enumerate(boxes):
        if box in boxes2scans:
            scans = boxes2scans[box]
            scans = sorted(scans, key=lambda s: s.rt_in_seconds)

            # A box can be linked to multiple ms2 scans.
            # Here we get all the ms2 scans that overlap a box.
            # For each ms2 scan, we then find its precursor intensity using the last ms1 scan
            box_intensities = []
            for ms2_scan in scans:
                precursor = ms2_scan.previous_ms1.get_precursor(ms2_scan.precursor_mz)
                if precursor is not None:
                    box_intensities.append(precursor[1])  # precursor is (mz, intensity)

            if method == 'max':
                # for each box, get the max precursor intensity
                if len(box_intensities) > 0:
                    intensity = max(box_intensities)
                    score = intensity / box.height
                    precursor_intensities.append(intensity)
                    scores.append(score)
                else:
                    precursor_intensities.append(0.0)
                    scores.append(0.0)

            elif method == 'first':
                # for each box, get the first precursor intensity (smallest RT)
                intensity = box_intensities[0]
                score = intensity / box.height
                precursor_intensities.append(intensity)
                scores.append(score)
        else:
            precursor_intensities.append(0.0)
            scores.append(0.0)

    precursor_intensities = np.array(precursor_intensities)
    scores = np.array(scores)
    return precursor_intensities, scores


def update_picked_boxes(picked_boxes, rt_shifts, mz_shifts):
    if rt_shifts is None and mz_shifts is None:
        return picked_boxes
    new_boxes = picked_boxes
    if rt_shifts is not None:
        for i, box in enumerate(new_boxes):
            box.rt += float(rt_shifts[i]) / 60.0
            box.rt_in_minutes += float(rt_shifts[i]) / 60.0
            box.rt_in_seconds += float(rt_shifts[i])
            box.rt_range = [box.rt_range[0] + rt_shifts[i] / 60.0, box.rt_range[1] + rt_shifts[i] / 60.0]
            box.rt_range_in_seconds = [box.rt_range_in_seconds[0] + rt_shifts[i],
                                       box.rt_range_in_seconds[1] + rt_shifts[i]]
    if mz_shifts is not None:
        for i, box in enumerate(new_boxes):
            box.mz += mz_shifts[i]
            box.mz_range = [box.mz_range[0] + mz_shifts[i], box.mz_range[1] + mz_shifts[i]]
    return new_boxes
