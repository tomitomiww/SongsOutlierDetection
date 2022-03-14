# SongsOutlierDetection
## Research and practicing NLP and Anomaly Detection
### Languages: Python

"SongsOutlierDetection" is a program for finding unique songs out of artists discography. The program asks from the user an artist's name, downloads their discography and proferms an anomaly detecion process, hopefully finding songs which stands out. The program only references the songs' lyrics (and leaves out notes and composition), and allows the user to exmine only part of the artist's discography.

The program uses TF-IDF statistic in orfer to analyze the songs, and offers the user three types of algorithms for anomaly detection:
- Local Outlier Factory (LOF).
- Isolation Forset.
- K-Means.
Moreover, the program offers the user to create a word-cloud out of the songs' lyrics.

Unfortunaly, the algorithms performed poorly on various popular artists (i.e Taylor Swift, Lorde, Adele, Rihanna, Billie Holiday and more), and they didn't detected any anomalies in the artists' discography. This means that some other methods need to be taken, or that most aritsts' songs' lyrics are consisted. Either way, the program performs great when it comes to extracing an artist's entire discography and saving it[^1].

[^1]: The program only considers songs which were included in a studio-album, and doesn't consider EPs, remixes, demos, audiobooks and singles.

