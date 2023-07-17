import numpy as np

from moisesdb.signal import (
    frame_signal,
    hwr,
    pad_along_axis,
    triangular_window,
    unframe_signal,
)


def track_energy(x, frame_length, hop_length, win):
    x = pad_along_axis(x, frame_length - hop_length, axis=-1)
    xmat = frame_signal(x, frame_length=frame_length, hop_length=hop_length)
    xmat = hwr(xmat) ** 0.5
    return np.mean((xmat.transpose(0, 1, 3, 2) * win), axis=-1)


def compute_activity_signal(
    x,
    frame_length=4096,
    hop_length=2048,
    win=triangular_window,
    var_lambda=20.0,
    theta=0.15,
):
    """
    x: nd.array with shape [stem, channels, samples]
    return: nd.array with the same shape as x containing the activity signal
    """
    e = track_energy(x, frame_length, hop_length, win(frame_length))
    e = e / e.max(axis=-1, keepdims=True)[0]
    c = 1.0 - (1.0 / (1.0 + np.exp(np.inner(var_lambda, (e - theta)))))
    c = to_original_size(
        c, size=x.shape[-1], frame_length=frame_length, hop_length=hop_length
    )
    return c


def to_original_size(act_signal, size, frame_length=4096, hop_length=2048):
    *shape, nwin = act_signal.shape
    hop_mat = np.ones((*shape, nwin, frame_length)) * act_signal[..., None]
    hop_mat = unframe_signal(hop_mat.transpose(-2, 0, 1, 3), hop_length)
    return hop_mat[..., :size]


def filter_from_mask(x, mask):
    """
    x: nd.array with the activity signal
    mask: nd.array of type bool
    ex.
        mask = activity > 0.25
        audio_non_silent = filter_from_mask(audio, mask)
    """
    for d in range(mask.ndim - 1):
        mask = mask.prod(0).astype(bool)
    return x[..., mask]
