import os
from constants import DATASET
from tqdm import tqdm
from utils import load_rhythms, load_strum_metadata, load_metrical_annotation, load_caption, get_metainfo, _parsing_meta, load_strum_split
from constants import KEY_DICT

def bind_process(dataset_path, strum_fingerprint, id2caps, metrical_levels_pulse_rates, annotator, train_track, valid_track, test_track):
    audio_path = os.path.join(dataset_path, "audio")
    key_path = os.path.join(dataset_path, "key/kraft_lerch2013tonalness/gtzan_key/genres")
    meta_path = os.path.join(dataset_path, "metadata/doh2023fingerprint/results")
    meta_tracks = set([i.replace(".json", "") for i in os.listdir(meta_path)])

    all_dataset = []
    for tag in os.listdir(audio_path):
        for fname in tqdm(os.listdir(f"{audio_path}/{tag}")):
            path = f"{tag}/{fname}"
            track_id = fname.replace(".wav", "")
            if path in train_track:
                split = "train"
            elif path in valid_track:
                split = "valid"
            elif path in test_track:
                split = "test"
            else:
                split = ""
            
            if track_id in meta_tracks:
                meta_json = get_metainfo(dataset_path, track_id)
                shazam_id = meta_json['track']['key']
                title = meta_json['track']['title']
                artist_name = meta_json['track']['subtitle']
            elif (track_id not in meta_tracks) and (track_id in strum_fingerprint):
                title = strum_fingerprint[track_id]["title"]
                artist_name = strum_fingerprint[track_id]["artist"]
                shazam_id = ""
                meta_json = {}
            elif (track_id not in meta_tracks) and (track_id not in strum_fingerprint):
                shazam_id = ""
                title = ""
                artist_name = ""
                meta_json = {}
            try:
                album_art_img_url = meta_json['track']['images']['coverarthq']
                artist_img_url = meta_json['track']['images']['background']
            except:
                album_art_img_url = ""
                artist_img_url = ""
            try:
                metadata, lyrics, yt_url = _parsing_meta(meta_json)
            except:
                metadata = {}
                lyrics= ""
                yt_url= ""
            if track_id in id2caps:
                caption = id2caps[track_id]
            else:
                caption = ""
            # key
            key_value = open(f"{key_path}/{path}".replace(".wav",".lerch.txt"),'r').read()
            key_info = KEY_DICT[key_value.strip()]
            rhythms_dict = load_rhythms(dataset_path, fname)
            results = {
                "track_id":track_id,
                "shazam_id":shazam_id,
                "title":title,
                "artist_name":artist_name,
                "album": metadata.get("album", ""),
                "label": metadata.get("label", ""),
                "released": metadata.get("released", ""),
                "tag":tag,
                "caption_15s": caption,
                "key":key_info,
                "youtube_url": yt_url,
                "album_img_url": album_art_img_url,
                "artist_img_url": artist_img_url,
                "path":path,
                "fault_filtered_split" : split
            }
            results.update(rhythms_dict)
            results["metrical_levels_pulse_rates"] = metrical_levels_pulse_rates[fname],
            results["metrical_annotators"] = annotator[fname]
            all_dataset.append(results)
    return all_dataset


def main(dataset_path):
    metrical_levels_pulse_rates, annotator = load_metrical_annotation(dataset_path)
    id2caps = load_caption(dataset_path)
    strum_fingerprint = load_strum_metadata(dataset_path)
    train_track, valid_track, test_track = load_strum_split(dataset_path)
    all_dataset = bind_process(
        dataset_path, 
        strum_fingerprint, 
        id2caps, 
        metrical_levels_pulse_rates,
        annotator, 
        train_track, 
        valid_track, 
        test_track
    )
    print(all_dataset[0])

if __name__ == '__main__':
    main(dataset_path="../dataset")