==================================================================================
Metrical structure annotations for the GTZAN dataset
Elio Quinton, 
Centre for Digital Music, Queen Mary University of London 2015
==================================================================================


1 - Brief Description
——————————————————————
We present a dataset consisting of metrical structure annotations for the GTZAN dataset.

- Each track of the dataset have been annotated at least twice.
- The annotations have been made by Professional drummers
- The metrical structure is represented by the pulse rates (in BPM) of all the metrical levels present in the music


2 - Citation
—————————————

If you make use of this dataset, please cite:
[1] E. Quinton, C. Harte, and M. Sandler, “Extraction of Metrical Structure from Music Recordings,” in Proc. of the 18th Int. Conference on Digital Audio Effects (DAFx). Trondheim, Norway, Nov 30 - Dec 3, 2015.


3 - Data Structure
———————————————————

3-1 JSON

The annotations dataset is presented in JSON format in order to be easily parsed while being human readable. 
For each track, a JSON object containing two fields is provided: 
	- “trackName”: contains the name of the track with the .wav extension
	- “data”: contains a list of JSON objects, one per unique annotation. Each annotation objects contains two fields: 
		- “annotator”: the annotator identifier. Numerous annotator have contributed to this dataset, each of them has a unique identifier. They are not labelled in any particular order.
		- “metrical_levels_pulse_rates”: is a list of all the metrical levels pulse rates annotated by the corresponding annotator, in BPM.  

Example data for the track ‘metal.00062.wav’:

{
  "data": [
    {
      "metrical_levels_pulse_rates": [
        29.2,
        58.9,
        119.5,
        240.0,
        480.0
      ],
      "annotator": "annotator1"
    },
    {
      "metrical_levels_pulse_rates": [
        30.0,
        60.0,
        119.4,
        240.0,
        480.0
      ],
      "annotator": "annotator3"
    },
    {
      "metrical_levels_pulse_rates": [
        29.4,
        58.7,
        117.5,
        241.7
      ],
      "annotator": "annotator2"
    }
  ],
  "trackName": "metal.00062.wav"
}


3-2 CSV

The annotation data is also provided in csv format, one file per audio track, as found in the ‘csv’ folder. 
Each file contains one annotation per raw. The left column contains the annotator label while the following columns contain the metrical levels pulse rates (in BPM). 

