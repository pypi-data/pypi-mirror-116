import numpy as np


def mape(real, predict, threshold=0):
    """
    Mean Absolute Percentage Error
    :param real: np.array
    :param predict: np.array
    :param threshold: float
    :return: float
    """
    # if threshold is None:
    #     return np.mean(np.abs(real - predict) / real) * 100
    keep = np.argwhere(np.abs(real) > threshold)
    r = real[keep]
    p = predict[keep]
    if len(r) == 0:
        return 0
    return np.mean(np.abs(r - p) / np.abs(r)) * 100


def pape(real, predict):
    """
    Peak Absolute Percentage Error
    :param real:
    :param predict:
    :return:
    """
    keep = np.argmax(real)
    r = real[keep]
    p = predict[keep]
    if r == 0:
        return 0
    return np.abs(r - p) / r * 100


def mae(real, predict, threshold=None):
    """
    Mean Absolute Error
    """
    if threshold is not None:
        keep = np.argwhere(np.abs(real) > threshold)
        real = real[keep]
        predict = predict[keep]
    return np.mean(np.abs(real - predict))


def smape(real, predict, threshold=0):
    """
    Symmetric Mean Absolute Percentage Error
    :param real: np.array
    :param predict: np.array
    :return: float
    """
    real_abs = np.abs(real)
    keep = np.argwhere(real_abs > threshold)

    r = real[keep]
    p = predict[keep]
    return np.mean(2 * np.abs(r - p) / (real_abs + np.abs(p))) * 100


def rmse(real, predict):
    """
    Root Mean Square Error
    rmse > mae
    """
    return np.mean(np.square(real - predict)) ** 0.5
