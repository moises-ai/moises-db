# moises-db
Moises Source Separation Public Dataset

# Download and Configure Environment Variable

Please download the dataset at `research.moises.ai`, extract it and configure the environment variable `MOISESDB_PATH` accordingly.

```
export MOISESDB_PATH=./moises-db-data
```

# Install

You can install this package with 

```
pip install git@github.com:moises-ai/moises-db.git
```

# Usage

## `MoisesDB`

After downloading and configuring the path for the dataset, you can create an instance of `MoisesDB` to access the tracks. You can also provide the dataset path with the `data_path` argument.

```
from moisesdb.dataset import MoisesDB

db = MoisesDB(
    data_path='./moises-db-data',
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

The stems and audio are computed on-the-fly. You can create a stems version only of the dataset using the `save_stems` method of the `MoisesDBTrack`.

```
track = db[0]
path =  './moises-db-stems/0'
track.save_stems(path)
```

# Contribute

People interested in uploading tracks to the MoisesDB can access https://datasets.moises.ai/stems and follow the instructions on the website.

