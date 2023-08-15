import os
import numpy as np
import json
import argparse
from time import sleep
from tqdm import tqdm
import pandas as pd
import asyncio
from shazamio import Shazam

shazam = Shazam()
async def _recognize_song(t_id, input_path):
    out = await shazam.recognize_song(input_path)
    if out['matches'] == []:
        print("error!", t_id)
    else:
        with open(os.path.join('../dataset/metadata/doh2023fingerprint/results', f"{t_id}.json"), mode="w") as io:
            json.dump(out, io, indent=4)
        print("Save", t_id)

async def _search_track(t_id, title, artist):
    if type(artist) == str:
        query = title + " by " + artist
    else:
        query = title
    tracks = await shazam.search_track(query=query, limit=20)
    if 'tracks' in tracks:
        for i in tracks['tracks']['hits']:
            if title.lower() in i['heading']['title'].lower():
                print(title, artist)
                print("="*30)
                break
    else:
        print(tracks)
    

def detect_shazam(help_fn, t_id, input_path):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(help_fn(t_id, input_path))

def detect_shazam_track(help_fn, fname, title, artist):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(help_fn(fname, title, artist))

def audio_finger_printing(dataset_dir):
    alread_downloads = set([i.replace(".json", "")for i in os.listdir("../dataset/metadata/doh2023fingerprint/results")])
    audio_dict = {fname.replace(".wav", ""): f"{dataset_dir}/{genre}/{fname}" for genre in os.listdir(dataset_dir) for fname in os.listdir(f"{dataset_dir}/{genre}")}
    audio_fnames = [fname.replace(".wav","") for genre in os.listdir(dataset_dir) for fname in os.listdir(f"{dataset_dir}/{genre}") if fname.replace(".wav", "") not in alread_downloads]
    audio_files = [audio_dict[i] for i in audio_fnames]
    errors = []
    for file, fname in zip(tqdm(audio_files), audio_fnames):
        try:
            detect_shazam(_recognize_song, fname, file)
        except:
            errors.append(fname)
    return errors

def title_finger_printing(errors): 
    df_meta = pd.read_csv("../dataset/rhythm/marchand2015swing/stats.csv")
    df_meta["filename"] = [i.replace(".wav", "") for i in df_meta['filename']]
    df_meta = df_meta.set_index("filename").loc[errors]
    df_meta = df_meta.loc[[name for i, name in zip(df_meta['title'], df_meta.index) if type(i) == str]]
    for idx in range(len(df_meta)):
        instance = df_meta.iloc[idx]
        fname, title, artist = instance.name, instance['title'], instance['artist']
        detect_shazam_track(_search_track, fname, title, artist)

if __name__ == '__main__':
    dataset_dir = "../dataset/audio"
    errors = audio_finger_printing(dataset_dir)
    