import os
import argparse
from time import sleep

from ShazamAPI.ShazamAPI.api import Shazam

def detect_shazam(p_id, input_path, chunk_time_sec=5, max_duration_min=90):
    # Setting
    with open(input_path, 'rb') as f:
        input = f.read()
    shazam = Shazam(input)
    shazam.MAX_TIME_SECONDS = chunk_time_sec
    recognizer = shazam.recognizeSong()
    
    # Detection
    results = {}
    detected_times = {}
    keyerrors = []
    while True:
        try:
            response = next(recognizer)
            if len(response) != 2: raise ValueError(len(response))
            
            # max time cutting
            if max_duration_min != None and response[0] > max_duration_min*60: 
                print(f'[{p_id}] Exceeded Maximum Time', response[0], flush=True)
                break
            
            shazam_key = response[1]['track']['key']

            if shazam_key in results:
                detected_times[shazam_key]['all'].append(response[0])
                continue
            else:
                track = response[1]['track']
                images = response[1]['track']['images']
                text = response[1]['track']['sections'][1]
                results[shazam_key] = {
                    'shazam_id': shazam_key,
                    'title': track.get('title', None),
                    'artist': track.get('subtitle', None),
                    'album_cover_url': images.get('coverart', None),
                    'isrc': track.get('isrc', None),
                    'lyrics': text.get('text', None)
                }
                detected_times[shazam_key] = {'all': [response[0]]}
                
            sleep(1)
            
        except ValueError as v:
            print(f'[{p_id}] LengthError', v, flush=True)
            continue
        
        except KeyError as k:
            keyerrors.append(response[0])
            
        except StopIteration:
            break
    
    misdetected_cnt = 0
    for k, v in results.items():
        if len(detected_times[k]['all']) < 3:
            del detected_times[k]
            misdetected_cnt += 1
            continue
        
        detected_times[k]['start_time'] = detected_times[k]['all'][0]
        detected_times[k]['end_time'] = detected_times[k]['all'][-1]
    
    # Search and Add Unknown Tracks
    detected_times = search_unknown(detected_times, keyerrors)
    return results, detected_times, misdetected_cnt

def search_unknown(d_times, errors):
    
    if len(errors) < 3: return d_times
    
    cnt = 0
    box = [errors[0]]
    
    for idx in range(len(errors)-1):
        if errors[idx+1] - errors[idx] < 15:
            box.append(errors[idx+1])
            continue
        
        if len(box) > 5 and (box[-1] - box[0]) > 30:
            d_times[f'UNK_{cnt}'] = {
                'all': box,
                'start_time': box[0],
                'end_time': box[-1]
            }
            cnt += 1
        box = [errors[idx+1]]
    return d_times