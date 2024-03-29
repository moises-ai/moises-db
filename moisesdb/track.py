import logging
import os

import librosa
import numpy as np

from moisesdb.activity import compute_activity_signal
from moisesdb.defaults import all_stems, default_data_path
from moisesdb.utils import load_audio, load_json, save_audio

logger = logging.getLogger(__name__)


class MoisesDBTrack:
    def __init__(
        self, provider, track_id, data_path=default_data_path, sample_rate=44100
    ):
        self.data_path = data_path
        self.path = os.path.join(self.data_path, provider, track_id)
        self.json_data = load_json(os.path.join(self.path, "data.json"))

        self.sr = sample_rate
        self.provider = provider
        self.id = track_id
        self.artist = self.json_data.get("artist", "")
        self.name = self.json_data.get("song", "untitled")
        self.genre = self.json_data.get("genre", "undefined")
        self.sources = self._parse_sources(self.json_data.get("stems", {}))
        self.bleedings = self._parse_bleeding(self.json_data.get("stems", {}))
        
    def _parse_bleeding(self, stems):
        bleeds = {s.get("stemName"): {} for s in stems}
        for stem in stems:
            unique_tracks = list({t["trackType"] for t in stem.get("tracks")})
            parsed_tracks = {t: [] for t in unique_tracks}
            stem_name = stem.get("stemName")
            for track in stem.get("tracks", []):
                parsed_tracks[track["trackType"]].append(track.get("has_bleed", False))
                
            if bleeds[stem_name]:
                for track_type, tracks in bleeds.items():
                    bleeds[stem_name].setdefault(track_type, []).extend(tracks)
            else:
                bleeds[stem_name].update(parsed_tracks)
        return bleeds

    def _parse_sources(self, stems):
        parsed_stems = {s.get("stemName"): {} for s in stems}
        for stem in stems:
            unique_tracks = list({t["trackType"] for t in stem.get("tracks")})
            parsed_tracks = {t: [] for t in unique_tracks}
            stem_name = stem.get("stemName")
            for track in stem.get("tracks", []):
                file_path = (
                    os.path.join(
                        self.data_path,
                        self.provider,
                        self.id,
                        stem_name,
                        track.get("id"),
                    )
                    + "."
                    + track.get("extension")
                )
                track_type = track["trackType"]
                parsed_tracks[track_type].append(file_path)

            if parsed_stems[stem_name]:
                for track_type, tracks in parsed_tracks.items():
                    parsed_stems[stem_name].setdefault(track_type, []).extend(tracks)
            else:
                parsed_stems[stem_name].update(parsed_tracks)

        return parsed_stems

    def stem_sources(self, stem):
        sources = self.sources.get(stem, {})
        sources_audio = {}
        for source, paths in sources.items():
            source_audios = [load_audio(p) for p in paths]
            sample_rates = [s[1] for s in source_audios]
            min_len = min(s[0].shape[-1] for s in source_audios)
            sources_audio[source] = [
                {"audio": s[0][..., :min_len], "sr": sr}
                for s, sr in zip(source_audios, sample_rates)
            ]
        return sources_audio

    def stem_sources_mixture(self, stem):
        stem_sources = self.stem_sources(stem=stem)
        sources_mixture = {}
        for source, sources_data in stem_sources.items():
            # Resample
            for source_data in sources_data:
                source_data["audio"] = librosa.resample(
                    source_data["audio"], orig_sr=source_data["sr"], target_sr=self.sr
                )
            # Mix
            sources_mixture[source] = trim_and_mix([s["audio"] for s in sources_data])
        return sources_mixture

    def stem_mixture(self, stem):
        sources_mixture = self.stem_sources_mixture(stem=stem)
        if all_sources := list(sources_mixture.values()):
            return trim_and_mix(all_sources)
        else:
            return None

    def save_stems(self, path):
        for stem, audio in self.stems.items():
            if audio is not None:
                filepath = os.path.join(path, f"{stem}.wav")
                logger.info(f"Saving {filepath}")
                save_audio(filepath, audio, sr=self.sr)

    def mix_stems(self, mix_map):
        stems = {}
        for stem, stem_sources in mix_map.items():
            stems_to_mix = [self.stem_mixture(s) for s in stem_sources]
            stems_to_mix = [s for s in stems_to_mix if s is not None]
            stems[stem] = trim_and_mix(stems_to_mix)
        return stems

    @property
    def stems(self):
        stems = {}
        for stem in all_stems:
            mix = self.stem_mixture(stem=stem)
            if mix is not None:
                stems[stem] = mix
        return stems

    @property
    def audio(self):
        stems = self.stems
        stems = {k: v for k, v in stems.items() if v is not None}
        return pad_and_mix(stems.values())

    @property
    def activity(self):
        return {
            stem: compute_activity_signal(audio[None, ...])[0]
            for stem, audio in self.stems.items()
        }


def pad_to_len(source, length):
    return np.pad(source, ((0, 0), (0, length))) if length > 0 else source


def pad_and_mix(sources):
    max_len = max(s.shape[-1] for s in sources)
    pad_len = [max_len - s.shape[-1] for s in sources]
    padded_mixtures = [pad_to_len(s, p) for s, p in zip(sources, pad_len)]
    return np.stack(padded_mixtures).sum(0)


def trim_and_mix(sources):
    min_len = min(s.shape[-1] for s in sources)
    return np.stack([s[..., :min_len] for s in sources]).sum(0)
