import unittest
import gammalearn.utils as utils
import numpy as np
from ctapipe.instrument import CameraGeometry


class MockLSTDataset(object):

    def __init__(self):

        self.images = np.array([np.full(1855, 0.001),
                                np.full(1855, 1),
                                np.full(1855, 0.0001),
                                np.full(1855, 0.1)])
        self.images[3, 903:910] = 30
        self.images[2, 1799:1806] = 10  # for cleaning and leakage
        self.camera_type = 'LST_LSTCam'
        self.group_by = 'image'
        self.geom = CameraGeometry.from_name('LSTCam')
        self.simu = True
        self.dl1_params = {
            'event_id': np.array([0, 0, 1, 2]),
            'mc_type': np.array([1, 0, 0, 0]),
            'mc_energy': np.array([0.010, 2.5, 0.12, 0.8]),
            'log_mc_energy': np.log10(np.array([0.010, 2.5, 0.12, 0.8])),
            'mc_alt_tel': np.full(4, np.deg2rad(70)),
            'mc_az_tel': np.full(4, np.deg2rad(180)),
            'mc_alt': np.deg2rad([71, 75, 68, 69]),
            'mc_az': np.deg2rad([180, 180, 179.5, 175]),
            'mc_core_x': np.array([50.3, -150, -100, 100])/1000,
            'mc_core_y': np.array([48, -51, 0, 0])/1000,
            'tel_id': np.array([2, 1, 3, 1]),
            'tel_pos_x': np.array([75.28, -70.93, -70.93, -70.93])/1000,
            'tel_pos_y': np.array([50.46, -52.07, 53.1, -52.07])/1000,
        }

    def __len__(self):
        return len(self.images)


class TestUtils(unittest.TestCase):

    def setUp(self) -> None:

        self.intensity_filter_parameters = [300, np.inf]
        self.intensity_true_mask = [False, True, False, True]

        self.cleaning_filter_parameters = {'picture_thresh': 6, 'boundary_thresh': 3,
                                           'keep_isolated_pixels': False, 'min_number_picture_neighbors': 2}
        self.cleaning_true_mask = [False, False, True, True]

        self.leakage_parameters = {'leakage2_cut': 0.2, 'picture_thresh': 6, 'boundary_thresh': 3,
                                   'keep_isolated_pixels': False, 'min_number_picture_neighbors': 2}
        self.leakage_true_mask = [False, False, False, True]

        self.energy_parameters = {'energy': [0.02, 2], 'filter_only_gammas': True}
        self.energy_true_mask = [True, False, True, True]

        self.emission_cone_parameters = {'max_angle': np.deg2rad(4.)}
        self.emission_cone_true_mask = [True, False, True, True]

        self.impact_distance_parameters = {'max_distance': 0.05}
        self.impact_distance_true_mask = [True, False, False, False]

        self.multiplicity_parameters = {'multiplicity': 2}
        self.multiplicity_true_mask = [True, True, False, False]
        self.multiplicity_strict_parameters = {'multiplicity': 1, 'strict': True}
        self.multiplicity_strict_true_mask = [False, False, True, True]
        self.multiplicity_strict_true_trig_energies = np.array([0.010, 0.12, 0.8])

    def test_emission_cone(self):
        self.dataset = MockLSTDataset()
        assert np.all(utils.emission_cone_filter(self.dataset, **self.emission_cone_parameters) ==
                      self.emission_cone_true_mask)

    def test_impact_distance(self):
        self.dataset = MockLSTDataset()
        assert np.all(utils.impact_distance_filter(self.dataset, **self.impact_distance_parameters) ==
                      self.impact_distance_true_mask)

    def test_multiplicity(self):
        self.dataset = MockLSTDataset()
        assert np.all(utils.telescope_multiplicity_filter(self.dataset, **self.multiplicity_parameters) ==
                      self.multiplicity_true_mask)

    def test_multiplicity_strict(self):
        self.dataset = MockLSTDataset()
        assert np.all(utils.telescope_multiplicity_filter(self.dataset, **self.multiplicity_strict_parameters) ==
                      self.multiplicity_strict_true_mask)

    def test_energy(self):
        self.dataset_lst = MockLSTDataset()
        assert np.all(utils.energyband_filter(self.dataset_lst, **self.energy_parameters) ==
                      self.energy_true_mask)

    def test_leakage(self):
        self.dataset = MockLSTDataset()
        assert np.all(utils.leakage_filter(self.dataset, **self.leakage_parameters) ==
                      self.leakage_true_mask)

    def test_cleaning(self):
        self.dataset = MockLSTDataset()
        assert np.all(utils.cleaning_filter(self.dataset, **self.cleaning_filter_parameters) ==
                      self.cleaning_true_mask)


if __name__ == '__main__':
    unittest.main()
