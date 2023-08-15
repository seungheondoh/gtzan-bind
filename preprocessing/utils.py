import os
from collections import Counter
import json
import pandas as pd
import numpy as np
import multiprocessing
from functools import partial
from audio_utils import load_audio
from constants import STR_CH_FIRST, MUSIC_SAMPLE_RATE, KEY_DICT

def gtzan_resampler(genre, path):
    src, _ = load_audio(
        path=os.path.join(DATASET,'gtzan','audio', genre, path),
        ch_format= STR_CH_FIRST,
        sample_rate= MUSIC_SAMPLE_RATE,
        downmix_to_mono= True)
    return src

def load_rhythms(dataset_path, fname):
    samples = json.load(open(os.path.join(dataset_path, f"rhythm/marchand2015swing/jams/{fname}.jams"), 'r'))
    sequences = {'beat':[], 'downbeat':[], '8th-note':[]}
    for ann in samples['annotations']:
        if "annotation_type" in ann['sandbox']:
            _type = ann['sandbox']['annotation_type']
            data = [i['time'] for i in ann['data']]
            sequences[_type] = data
        else:
            sequences.update(ann['sandbox'])
    return {"_".join(i.split()):j for i,j in sequences.items()}

def load_strum_metadata(dataset_path):
    strum_fingerprint = {}
    for i in pd.read_csv(os.path.join(dataset_path, "rhythm/marchand2015swing/stats.csv")).to_dict(orient = "records"):
        _id = i["filename"].replace(".wav", "")
        if type(i['artist']) == str:
            artist = i['artist']
        else:
            artist = ""
        strum_fingerprint[_id] = {
            "id": _id,
            "artist": artist,
            "title": i['title']
        }
    return strum_fingerprint

def load_metrical_annotation(dataset_path):
    metrical_annotation = json.load(open(os.path.join(dataset_path, "rhythm/quinton2015extraction/annotations_MetricalStructure_GTZAN.json"), 'r'))
    metrical_levels_pulse_rates = {instance['trackName']: [i['metrical_levels_pulse_rates'] for i in instance['data']] for instance in metrical_annotation}
    annotator = {instance['trackName']: [i['annotator'] for i in instance['data']] for instance in metrical_annotation}
    return metrical_levels_pulse_rates, annotator

def load_caption(dataset_path):
    df_cap = pd.read_csv(os.path.join(dataset_path, "caption/denk2023brain2music/brain2music-captions.csv")).to_dict(orient="records")
    id2caps = {i["ID"].replace("_15s", ""):i["DescEN"] for i in df_cap}
    id2caps['disco.00011'] = id2caps['disco.000011'] # update wrong annotation
    return id2caps

def get_metainfo(dataset_path, track_id):
    meta_path = os.path.join(dataset_path,"metadata/doh2023fingerprint/results")
    return json.load(open(f"{meta_path}/{track_id}.json", "r"))

def _parsing_meta(temp):
    metadata, lyrics, youtube_url = {}, "", ""
    for section in temp['track']['sections']:
        if section['type'] == "SONG":
            metadata = {i["title"].lower() :i["text"] for i in section['metadata']}
        elif section['type'] == "LYRICS":
            lyrics = section['text']
        elif section['type'] == "VIDEO":
            youtube_url = section['youtubeurl']
            r = requests.get(youtube_url)
            yt_url = r.json()['actions'][0]['uri'].replace("?autoplay=1","")
    return metadata, lyrics, yt_url

def load_strum_split(dataset_path):
    sturm_path = os.path.join(dataset_path, "split/sturm2013faults")
    tr_names = os.path.join(sturm_path, "train_filtered.txt")
    va_names = os.path.join(sturm_path, "valid_filtered.txt")
    te_names = os.path.join(sturm_path, "test_filtered.txt")
        
    train_track = set(open(tr_names,'r').read().splitlines())
    valid_track = set(open(va_names,'r').read().splitlines())
    test_track = set(open(te_names,'r').read().splitlines())
    return train_track, valid_track, test_track

    