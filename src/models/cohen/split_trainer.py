import numpy as np
from scipy.signal import convolve2d

from data import density_map, scale_annotation
from Trainer import Trainer

from .model import build_model, shape

_image_split = 16
_image_size = shape[0]
_receptive_field_size = 32


def _get_validation_data(data, testing_indices):
    X, _, _, Locations = data
    Y = np.array([_get_output(locations)
                  for locations in Locations[testing_indices]])
    X_test = X[testing_indices]
    return X_test.reshape((*X_test.shape, 1)), Y


def _build_model():
    return build_model()


def _get_x(data):
    return data[0]


def _get_y(data):
    return _get_output(data[3])


filter = np.full((_receptive_field_size, _receptive_field_size), 1)


def _get_output(locations):
    output = np.pad(convolve2d(locations, filter), (1, 0), mode="constant")
    return output.reshape((*output.shape, 1))


def get_trainer(persistence_directory):
    return Trainer(persistence_directory, _image_split, _image_size, _get_validation_data, _build_model, _get_x, _get_y)
