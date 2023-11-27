---
language: 
- en
pretty_name: MoisesDB
tags:
- audio
- music
- source separation
license: NC-RCL
---

# MoisesDB
Moises Dataset for Source Separation

### Dataset Description

- **Homepage:** [MoisesDB homepage](https://developer.moises.ai/research/)
- **Repository:** [MoisesDB repository](https://github.com/moises-ai/moises-db)
- **Paper:** [Moisesdb: A dataset for source separation beyond 4-stems](https://arxiv.org/abs/2307.15913)
- **Point of Contact:** [Igor Pereira](mailto:igor@moises.ai)

### Dataset Summary

MoisesDB is a dataset for source separation. It provides a collection of tracks and their separated stems (vocals, bass, drums, etc.). The dataset is used to evaluate the performance of source separation algorithms.

# Download the data

Please download the dataset at our research [website](https://developer.moises.ai/research), extract it and configure the environment variable `MOISESDB_PATH` accordingly.

```
export MOISESDB_PATH=./moises-db-data
```

The directory structure should be

```
moisesdb:
    moisesdb_v0.1
        track uuid 0
        track uuid 1
        .
        .
        .
```

# Install

You can install this package with

```
pip install git+https://github.com/moises-ai/moises-db.git
```

# Usage

## `MoisesDB`

After downloading and configuring the path for the dataset, you can create an instance of `MoisesDB` to access the tracks. You can also provide the dataset path with the `data_path` argument.

```
from moisesdb.dataset import MoisesDB

db = MoisesDB(
    data_path='./moisesdb',
    sample_rate=44100
)
```

The `MoisesDB` object has iterator properties that you can use to access all files within the dataset.

```
n_songs = len(db)
track = db[0]  # Returns a MoisesDBTrack object
```

## `MoisesDBTrack`

The `MoisesDBTrack` object holds information about a track in the dataset, perform on-the-fly mixing for stems and multiple sources within a stem.

You can access all the stems and mixture from the `stem` and `audio` properties. The `stem` property returns a dictionary whith available stems as keys and `nd.array` on values. The `audio` property results in a `nd.array` with the mixture.

```
track = db[0]
stems = track.stems  # stems = {'vocals': ..., 'bass': ..., ...}
mixture track.audio # mixture = nd.array
```

The `MoisesDBTrack` object also contains other non-audio information from the track such as:
- `track.id`
- `track.provider`
- `track.artist`
- `track.name`
- `track.genre`
- `track.sources`
- `track.bleedings`
- `track.activity`

The stems and mixture are computed on-the-fly. You can create a stems-only version of the dataset using the `save_stems` method of the `MoisesDBTrack`.

```
track = db[0]
path =  './moises-db-stems/0'
track.save_stems(path)
```

# Performance Evaluation

We run a few source separation algorithms as well as oracle methods to evaluate the performance of each track of the `MoisesDB`. These results are located in `csv` files at the `benchmark` folder.

# Citing

If you used the `MoisesDB` dataset on your research, please cite the following paper.

```
@misc{pereira2023moisesdb,
      title={Moisesdb: A dataset for source separation beyond 4-stems}, 
      author={Igor Pereira and Felipe Araújo and Filip Korzeniowski and Richard Vogl},
      year={2023},
      eprint={2307.15913},
      archivePrefix={arXiv},
      primaryClass={cs.SD}
}
```

# Licensing

`MoisesDB` is distributed with the NC-RCL license.

```
"Non-Commercial Research Community license (NC-RCL)

Limited Redistribution: You are permitted to copy and utilize the provided audio material in any medium or format, as long as it is done only for non-commercial purposes within the research community, and the redistribution is conducted solely through the platform moises.ai or other platforms explicitly authorized by the licensor. Redistribution outside the authorized platforms is not allowed without the licensor's written consent.

Attribution: You must give appropriate credit (including the artist's name and the song's title), and provide a link to this license or a notice indicating the terms of this license.

Non-Commercial Use: You cannot use the material for any commercial purposes or financial gain. This includes, but is not limited to, the sale, licensing, or rental of the material, as well as any use where the primary aim is to generate revenue or profits.

No Derivative Works: You cannot create, remix, adapt, or build upon the material, unless explicitly permitted by the artist.

Preservation of Legal Notices: You cannot remove any copyright or other proprietary notices which are included in or attached to the material.

Termination: If you fail to comply with this license, your rights to use the material will be terminated automatically.

Voice Cloning Restriction: You are prohibited from using the vocal stems or any part of the audio material to create a public digital imitation of the artist's voice (e.g: a vocal clone or replica). This includes, but is not limited to, the utilization of voice synthesis technology, deep learning algorithms, and other artificial intelligence-based tools."
```


