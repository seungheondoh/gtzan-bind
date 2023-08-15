DATASET="../dataset"
INT_RANDOM_SEED = 42
MUSIC_SAMPLE_RATE = 22050
STR_CH_FIRST = 'channels_first'
STR_CH_LAST = 'channels_last'
DATA_LENGTH = MUSIC_SAMPLE_RATE * 30
INPUT_LENGTH = MUSIC_SAMPLE_RATE * 10
CHUNK_SIZE = 16

KEY_DICT = {
    '0': 'major a',
    '1': 'major a#',
    '2': 'major b',
    '3': 'major c',
    '4': 'major c#',
    '5': 'major d',
    '6': 'major d#',
    '7': 'major e',
    '8': 'major f',
    '9': 'major f#',
    '10': 'major g',
    '11': 'major g#',
    '12': 'minor a',
    '13': 'minor a#',
    '14': 'minor b',
    '15': 'minor c',
    '16': 'minor c#',
    '17': 'minor d',
    '18': 'minor d#',
    '19': 'minor e',
    '20': 'minor f',
    '21': 'minor f#',
    '22': 'minor g',
    '23': 'minor g#',
    '-1': ""
}