import os
from concurrent.futures import ThreadPoolExecutor

from tqdm import tqdm

from moisesdb.defaults import default_data_path, default_sample_rate
from moisesdb.track import MoisesDBTrack
from moisesdb.utils import get_fs


class MoisesDB:
    def __init__(self, data_path=default_data_path, sample_rate=default_sample_rate):
        self.data_path = os.environ.get("MOISESDB_PATH", data_path)
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
        futures = []
        with ThreadPoolExecutor() as executor:
            for t in providers_tracks:
                futures.append(
                    executor.submit(
                        fs.exists,
                        os.path.join(self.data_path, provider, t, "data.json"),
                    )
                )
            track_exists = [f.result() for f in futures]
        return [t for t, te in zip(providers_tracks, track_exists) if te]

    def get_tracks_list(self, providers_list):
        futures = []
        with ThreadPoolExecutor() as executor:
            for p in providers_list:
                futures.append(executor.submit(self.get_providers_tracks, provider=p))
        return {p: f.result() for p, f in zip(providers_list, futures)}

    def build_tracks(self, providers_tracks):
        tracks = {}
        with ThreadPoolExecutor() as executor:
            for provider, tracks_list in providers_tracks.items():
                futures = []
                for t in tracks_list:
                    futures.append(
                        executor.submit(
                            MoisesDBTrack,
                            provider=provider,
                            track_id=t,
                            data_path=self.data_path,
                            sample_rate=self.sample_rate,
                        )
                    )

                itt = tqdm(
                    futures,
                    total=len(futures),
                    desc="Loading tracks info from provider %s" % provider,
                )
                tracks[provider] = [future.result() for future in itt]
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
