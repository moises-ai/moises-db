import numpy as np


def pad_along_axis(array, target_length, axis=0):
    pad_size = target_length - array.shape[axis]
    if pad_size <= 0:
        return array
    npad = [(0, 0)] * array.ndim
    npad[axis] = (0, pad_size)
    return np.pad(array, pad_width=npad, mode="constant", constant_values=0)


def hwr(x, floor=1e-7):
    return (x + np.abs(x)) / 2


def compute_nbwin(size, frame_length, hop_length):
    nbwin = np.ceil((size - (frame_length - hop_length)) / hop_length).astype(int)
    return nbwin


def compute_length(nbwin, frame_length, hop_length):
    length = hop_length * nbwin + (frame_length - hop_length)
    return length


def triangular_window(length, power=1.0):
    window = np.concatenate(
        [np.arange(1, length // 2 + 1), np.arange(length - length // 2, 0, -1)]
    )
    return (window / window.max()) ** power


def frame_signal(x, frame_length, hop_length):
    n_frames = compute_nbwin(x.shape[-1], frame_length, hop_length)
    x = pad_along_axis(x, n_frames * hop_length, axis=-1)
    strides = np.array(x.strides)
    new_stride = np.prod(strides[strides > 0])
    shape = list(x.shape)[:-1] + [frame_length, n_frames]
    strides = list(x.strides) + [hop_length * strides[-1]]
    return np.lib.stride_tricks.as_strided(x, shape, strides)


def unframe_signal(framed, hop_length, window_fn=triangular_window):
    nbwin, nbsamples = framed.shape[0], framed.shape[-1]
    signal_length = compute_length(nbwin, nbsamples, hop_length)
    win = window_fn(nbsamples)
    framed = framed * win
    offsets = range(0, signal_length - hop_length, hop_length)
    reconstructed = np.zeros((*framed.shape[1:-1], signal_length))
    weights = np.zeros((*framed.shape[1:-1], signal_length))
    for ofidx, offset in enumerate(offsets):
        reconstructed[..., offset : offset + nbsamples] += framed[ofidx]
        weights[..., offset : offset + nbsamples] += win
    return reconstructed / weights
