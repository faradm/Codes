import os
import pickle as pkl
import numpy as np
def bytescaling(data, cmin=None, cmax=None, high=255, low=0):
    """
    Converting the input image to uint8 dtype and scaling
    the range to ``(low, high)`` (default 0-255). If the input image already has 
    dtype uint8, no scaling is done.
    :param data: 16-bit image data array
    :param cmin: bias scaling of small values (def: data.min())
    :param cmax: bias scaling of large values (def: data.max())
    :param high: scale max value to high. (def: 255)
    :param low: scale min value to low. (def: 0)
    :return: 8-bit image data array
    """
    if data.dtype == np.uint8:
        return data

    if high > 255:
        high = 255
    if low < 0:
        low = 0
    if high < low:
        raise ValueError("`high` should be greater than or equal to `low`.")

    if cmin is None:
        cmin = data.min()
    if cmax is None:
        cmax = data.max()

    cscale = cmax - cmin
    if cscale == 0:
        cscale = 1

    scale = float(high - low) / cscale
    bytedata = (data - cmin) * scale + low
    return (bytedata.clip(low, high) + 0.5).astype(np.uint8)


if __name__ == "__name__":
    dir = "../pkl_files"
    files = os.listdir(dir)
    for file in files:
        file_adr = os.path.join(dir, file)
        img = None
        X = None
        with open(file_adr, "rb") as f:
            X = pkl.load(f)
        img = X['fullmammo_img']
        img = bytescaling(img)
        X['fullmammo_img'] = img
        pkl.dump(os.path.join("../pkl_files_edited", file))