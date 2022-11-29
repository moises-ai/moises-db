import os
import fsspec
from moisesdb.utils import get_fs
from moisesdb.defaults import default_data_path, default_sample_rate
from moisesdb.track import MoisesDBTrack


class MoisesDB:
    def __init__(self, data_path=default_data_path, sample_rate=default_sample_rate):
        self.data_path = os.environ.get('MOISESDB_PATH', data_path)
        self.sample_rate = sample_rate
        self.providers_list = self.get_providers(data_path)
        self.providers_tracks = self.get_tracks_list(self.providers_list)
        self.tracks = self.build_tracks(self.providers_tracks)
        self.flatten_map = self.build_flatten_map(self.tracks)

    def get_providers(self, data_path):
        fs = get_fs(self.data_path)
        return [os.path.basename(p) for p in fs.ls(self.data_path)]

    def get_providers_tracks(self, provider):
        fs = get_fs(self.data_path)
        providers_tracks = [
            os.path.basename(p) for p in fs.ls(os.path.join(self.data_path, provider))
        ]
        return [
            t
            for t in providers_tracks
            if fs.exists(os.path.join(self.data_path, provider, t, "data.json"))
        ]

    def get_tracks_list(self, providers_list):
        return {p: self.get_providers_tracks(provider=p) for p in providers_list}

    def build_tracks(self, providers_tracks):
        tracks = {}
        for provider, tracks_list in providers_tracks.items():
            tracks[provider] = [
                MoisesDBTrack(
                    provider=provider,
                    track_id=t,
                    data_path=self.data_path,
                    sample_rate=self.sample_rate,
                )
                for t in tracks_list
            ]
        return tracks

    def build_flatten_map(self, tracks):
        flatten_map = []
        for provider, tracks_list in tracks.items():
            for track in tracks_list:
                flatten_map.append(track)
        return flatten_map

    def __len__(self):
        return len(self.flatten_map)

    def __getitem__(self, idx):
        return self.flatten_map[idx]
