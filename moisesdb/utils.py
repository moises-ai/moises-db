import json
from io import BytesIO

import fsspec
import librosa
import soundfile as sf


def load_json(path):
    with fsspec.open(path, "r") as f:
        return json.loads(f.read(-1))


def load_audio(path, fsspec_kwargs={}, **kwargs):
    with fsspec.open(path, "rb", **fsspec_kwargs) as f:
        samples = list(librosa.load(f, sr=None, mono=False, **kwargs))
    if samples[0].ndim < 2:
        samples[0] = samples[0][None, ...].repeat(2, axis=0)
    return samples


def save_audio(path, audio, **kwargs):
    wav_io = BytesIO()
    sf.write(
        wav_io,
        audio.T,
        samplerate=kwargs.pop("sr", 44100),
        subtype=kwargs.pop("subtype", "PCM_24"),
        format=kwargs.pop("format", "wav"),
        **kwargs
    )
    with fsspec.open(path, mode="wb") as f:
        f.write(wav_io.getbuffer())


def get_fs(path):
    fs, _ = fsspec.core.url_to_fs(str(path))
    return fs
