import os


default_sample_rate = 44100
default_data_path = 'gs://service-dataset-collection-new'


taxonomy = {
    'vocals': [
        'lead male singer',
        'lead female singer',
        'human choir',
        'background vocals',
        'other (vocoder, beatboxing etc)'
    ],
    'bass': [
        'bass guitar',
        'bass synthesizer (moog etc)',
        'contrabass/double bass (bass of instrings)',
        'tuba (bass of brass)',
        'bassoon (bass of woodwind)',
    ],
    'drums': [
        'snare drum',
        'toms',
        'kick drum',
        'cymbals',
        'overheads',
        'full acoustic drumkit',
        'drum machine',
    ],
    'other': [
        'fx/processed sound, scratches, gun shots, explosions etc',
        'click track',
    ],
    'guitar': [
        'clean electric guitar',
        'distorted electric guitar',
        'lap steel guitar or slide guitar',
        'acoustic guitar',
    ],
    'other plucked': [
        'banjo, mandolin, ukulele, harp etc'
    ],
    'percussion': [
        'a-tonal percussion (claps, shakers, congas, cowbell etc)',
        'pitched percussion (mallets, glockenspiel, ...)',
    ],
    'piano': [
        'grand piano',
        'electric piano (rhodes, wurlitzer, piano sound alike)',
    ],
    'other keys': [
        'organ, electric organ',
        'synth pad',
        'synth lead',
        'other sounds (hapischord, melotron etc)',
    ],
    'bowed strings': [
        'violin (solo)',
        'viola (solo)',
        'cello (solo)',
        'violin section',
        'viola section',
        'cello section',
        'string section',
        'other strings',
    ],
    'wind': [
        'brass (trumpet, trombone, french horn, brass etc)',
        'flutes (piccolo, bamboo flute, panpipes, flutes etc)',
        'reeds (saxophone, clarinets, oboe, english horn, bagpipe)',
        'other wind',
    ]
}

all_stems = [t.replace(' ', '_') for t in taxonomy.keys()]

mix_4_stems = {
    'vocals': ['vocals'],
    'bass': ['bass'],
    'drums': ['drums'],
    'other': [s for s in all_stems if s not in ['vocals', 'bass', 'drums']]
}

mix_5_stems = {
    'vocals': ['vocals'],
    'bass': ['bass'],
    'guitar': ['guitar'],
    'drums': ['drums'],
    'other': [s for s in all_stems if s not in ['vocals', 'bass', 'drums', 'guitar']]
}

mix_6_stems = {
    'vocals': ['vocals'],
    'bass': ['bass'],
    'guitar': ['guitar'],
    'piano': ['piano'],
    'drums': ['drums'],
    'other': [s for s in all_stems if s not in ['vocals', 'bass', 'drums', 'guitar', 'piano']]
}
