from Artist import Artist
from NLPArtistProcessor import NLPArtistProcessor
from Constants import AD_METHOD, AD_METHODS_DICT
import os

"""
FILE: main.py.
the main file of the project.
"""
def main():
    # greets the user and asks for an artist's name.
    print("[*] HELLO!")
    artist_name = input("[?] Please enter an artist's name: ")
    artist_name = artist_name.strip().replace(" ","").lower()
    # gets the artist's lyrics.
    artist = Artist(artist_name)

    # prepares the relevant albums.
    print("[?] Which albums would you like to consider?")
    for album in os.listdir(artist.artist_path):
        print(f"\t{album}")
    albums_list = input("[?] Write their numbers separated by a comma, or 0 if you'd like them all.\n").split(",")
    if(albums_list[0].strip()!='0'):
        albums_list = [x.strip() for x in albums_list]
        albums_list = [album for album in os.listdir(artist.artist_path) if str(os.listdir(artist.artist_path).index(album) + 1) in albums_list]
    else:
        albums_list = os.listdir(artist.artist_path)

    # gets the preferred AD-METHOD and implements it.
    print("[?] Which anomaly-detection method would you like to use?")
    for key in AD_METHODS_DICT.keys():
        print(f"\t{key}")
    chosen_method = int(input("[?] Write its number.\n"))
    if(chosen_method==AD_METHOD.LOF.value):
        NLPArtistProcessor.LOF(artist, albums_list)
    if(chosen_method==AD_METHOD.ISO_FOREST.value):
        NLPArtistProcessor.ISO_FOREST(artist, albums_list)
    if(chosen_method==AD_METHOD.KMEANS.value):
        NLPArtistProcessor.KMEANS(artist, albums_list)
    if(chosen_method==AD_METHOD.WCLOUD.value):
        NLPArtistProcessor.createWordCloud(artist, albums_list)
    #NLPArtistProcessor.hierarchicalClusteringArtist(artist, 3)
    #NLPArtistProcessor.KMeansClusteringArtist(artist, 3)
    #NLPArtistProcessor.visual2D(artist)

#TODO ASK FOR A METHOD: LOF, ISO_FOREST, KMEANS.

if __name__ == "__main__":
  main()