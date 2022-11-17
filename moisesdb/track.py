import os
import json
import yaml
import numpy as np
import librosa
from moisesdb.defaults import default_data_path, all_stems
from moisesdb.utils import load_json, load_audio


class MoisesDBTrack:
    def __init__(self,
                 provider,
                 track_id,
                 data_path=default_data_path,
                 sample_rate=44100):
        self.data_path = os.environ.get('MOISESDB_PATH', data_path)
        self.path = os.path.join(self.data_path, provider, track_id)
        json_data = load_json(os.path.join(self.path, 'data.json'))
        
        self.sr = sample_rate
        self.provider = provider
        self.track_id = track_id
        self.artist = json_data.get('artist', '')
        self.name = json_data.get('song', 'untitled')
        self.genre = json_data.get('genre', 'undefined')
        self.sources = self.parse_sources(json_data.get('stems', {}))
        
    def parse_sources(self, stems):
        parsed_stems = {s.get('stemName'): {} for s in stems}
        for stem in stems:
            unique_tracks = list(set([t['trackType'] for t in stem.get('tracks')]))
            parsed_tracks = {t: [] for t in unique_tracks}
            for track in stem.get('tracks', []):
                file_path = os.path.join(
                    self.data_path,
                    self.provider,
                    self.track_id,
                    stem.get('stemName'), 
                    track.get('id')
                ) + '.' + track.get('extension')
                parsed_tracks[track['trackType']].append(file_path)

            parsed_stems[stem.get('stemName')].update(parsed_tracks)
        return parsed_stems

    def stem_sources(self, stem):
        sources = self.sources.get(stem, {}) 
        sources_audio = {}
        for source, paths in sources.items():
            source_audios = [load_audio(p) for p in paths]
            sample_rates = [s[1] for s in source_audios]
            min_length = min([s[0].shape[-1] for s in source_audios])
            sources_audio[source] = [{
                'audio': s[0][..., :min_length],
                'sr': sr
            } for s, sr in zip(source_audios, sample_rates)]
        return sources_audio
    
    def stem_sources_mixture(self, stem):
        stem_sources = self.stem_sources(stem=stem)
        sources_mixture = {}
        for source, sources_data in stem_sources.items():
            # Resample
            for source_data in sources_data:
                source_data['audio'] = librosa.resample(
                    source_data['audio'],
                    orig_sr=source_data['sr'],
                    target_sr=self.sr
                )
            # Mix Individual Source
            sources_mixture[source] = np.stack([s['audio'] for s in sources_data]).sum(0)
        return sources_mixture
    
    def stem_mixture(self, stem):
        sources_mixture = self.stem_sources_mixture(stem=stem)
        all_sources = [s for s in sources_mixture.values()]
        if all_sources:
            return np.stack([s for s in sources_mixture.values()]).sum(0)
        else:
            return None
    
    @property
    def stems(self):
        stems = {}
        for stem in all_stems:
            stems[stem] = self.stem_mixture(stem=stem)
        return stems
    
    @property
    def audio(self):
        stems = self.stems
        stems = {k: v for k, v in stems.items() if v is not None}
        max_length = max([s.shape[-1] for s in stems.values()])
        pad_length = [max_length - s.shape[-1] for s in stems.values()]
        padded_mixtures = []
        for s, p in zip(stems.values(), pad_length):
            padded_mixtures.append(np.pad(s, ((0, 0), (0, p))) if p else s)
        return np.stack(padded_mixtures).sum(0)
