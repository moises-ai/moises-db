import os
import librosa
import json
import yaml
import fsspec


def load_json(path):
    with fsspec.open(path, 'r') as f:
        return json.loads(f.read(-1))
    

def load_audio(path, fsspec_kwargs={}, **kwargs):
    with fsspec.open(path, 'rb', **fsspec_kwargs) as f:
        samples = list(librosa.load(f, sr=None, mono=False, **kwargs))
    if samples[0].ndim < 2:
        samples[0] = samples[0][None, ...].repeat(2, axis=0)
    return samples


def get_fs(path):
    fs, _ = fsspec.core.url_to_fs(str(path))
    return fs
