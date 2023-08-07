==========================================================

 Key annotations for the GTZAN genre dataset

   Tom Li and Antoni B. Chan
   Department of Computer Science
   City University of Hong Kong

   July 10, 2012

==========================================================

About the labeling process: 

I listened to a song while pressing the key of an electronic keyboard.  I labeled the songs according to the position of the "Do" sound in the So-Fa name. So C Major corresponds to A Minor. In other words, the labels are the relative major scales (all minor keys will be labeled 3 semitones higher).

I also tried to add a major/minor label.  This was rather difficult for some songs, basically because classical and blues music can shift scales very frequently. More over, there are more musical scales than major/minor.  Many of the songs follow the blues scale, so the labeling could be expanded to major/minor/blues.

The difficulty of annotating the key labels varies by the genre. The simplest genre is the pop genre. The most difficult genres are the classical and the hip hop genre. Some classical songs change scale after several seconds, while in most of the hip hop music I needed to use the bass to determine the key.

--------------------------------------------------------------
The attached files are the key annotation of the dataset:

groundkeys.txt -- text file of key annotations, C to 0, C# to 1, D to 2 ....... B to 11.  The songs are in alphabetical order (blues 1-100, classical 1-100, etc).

gtzankeys.xls -- Excel file containing the key labels and the incomplete major/minor labeling. (groundkeys.txt was generated from this file).

echonestkey/ -- echonest key and ID information.  I also tried automatic annotation, using the EchoNest APIs.  The confidence level of the results are also low (see in the parentheses). I uploaded the GTZAN dataset to the APIs, so you will just need to refer to the index of the media files in case you want to do further analysis of the dataset.

--------------------------------------------------------------
If you use this data, please cite the following paper:

  Genre Classification and the Invariance of MFCC Features to Key and Tempo,
  Tom LH. Li and A. B. Chan,
  in Intl. Conference on MultiMedia Modeling (MMM),
  Taipei, Jan 2011.

--------------------------------------------------------------
Problems?
Contact Info:

  Tom Li (tomli1985 atsign gmail.com)
  Antoni Chan (abchan atsign cityu.edu.hk)

