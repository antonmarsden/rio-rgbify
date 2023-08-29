from __future__ import division
import numpy as np


def data_to_rgb(data, encoding, baseval, interval, round_digits=0):
    """
    Given an arbitrary (rows x cols) ndarray,
    encode the data into uint8 RGB from an arbitrary
    base and interval

    Parameters
    -----------
    data: ndarray
        (rows x cols) ndarray of data to encode
    baseval: float
        the base value of the RGB numbering system.
        will be treated as zero for this encoding
    interval: float
        the interval at which to encode
    round_digits: int
        erased less significant digits

    Returns
    --------
    ndarray: rgb data
        a uint8 (3 x rows x cols) ndarray with the
        data encoded
    """
    data = data.astype(np.float64)

    if(encoding == "terrarium"):
        data += 32768
    else:
        data -= baseval
        data /= interval

    data = np.around(data / 2**round_digits) * 2**round_digits

    rows, cols = data.shape

    datarange = data.max() - data.min()

    if _range_check(datarange):
        raise ValueError("Data of {} larger than 256 ** 3".format(datarange))

    rgb = np.zeros((3, rows, cols), dtype=np.uint8)

    if(encoding == "terrarium"):
        rgb[0] = data // 256
        rgb[1] = np.floor(data % 256);
        rgb[2] = np.floor((data - np.floor(data)) * 256)
    else:
        rgb[0] = ((((data // 256) // 256) / 256) - (((data // 256) // 256) // 256)) * 256
        rgb[1] = (((data // 256) / 256) - ((data // 256) // 256)) * 256
        rgb[2] = ((data / 256) - (data // 256)) * 256

    return rgb


def _decode(data, base, interval):
    """
    Utility to decode RGB encoded data
    """
    data = data.astype(np.float64)
    if(encoding == "terrarium"):
        return (data[0] * 256 + data[1] + data[2] / 256) - 32768
    else:
        return base + (((data[0] * 256 * 256) + (data[1] * 256) + data[2]) * interval)

def _range_check(datarange):
    """
    Utility to check if data range is outside of precision for 3 digit base 256
    """
    maxrange = 256 ** 3

    return datarange > maxrange
