import os
import pandas as pd
from typing import List

from Artist import Artist
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.cluster import KMeans
from sklearn.neighbors import LocalOutlierFactor
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
from Constants import PLT_COLORMAPS, STOPWORDS_PATH
import random
from wordcloud import WordCloud, STOPWORDS


"""
CLASS: NLPArtistProcessor
This class holds some methods for processing data about artists' lyrics.
"""
class NLPArtistProcessor:

    """
    METHOD: getTFIDFTable.
    Creates a data-table from the lyrics, using tf-idf.
    INPUT: artist (Artist): the Artist instance to be referenced.
           albums (List[str]): a list of albums to be referenced.
    OUTPUT: the tf-idf table (pd.DataFrame).
    """
    @staticmethod
    def __getTFIDFTable(artist: Artist, albums: List[str]) -> pd.DataFrame:
        artist_path = artist.artist_path
        songs_lyrics_list = []
        # gets the lyrics.
        for album in albums:
            current_path = artist_path + f"\\{album}"
            for song in os.listdir(current_path):
                file = open(f"{current_path}\\{song}", "r+")
                current_song_lyrics = file.read()
                songs_lyrics_list.append(current_song_lyrics)
                file.close()
        # creates the tf-idf table.
        my_stop_words = ENGLISH_STOP_WORDS
        my_stop_words = my_stop_words.union(open(STOPWORDS_PATH, "r+").read().split("\n"))
        tv = TfidfVectorizer(stop_words=my_stop_words)
        tv_results = tv.fit_transform(songs_lyrics_list)
        songs_table = pd.DataFrame(tv_results.todense())

        # adds indexes for albums and songs' names.
        table = pd.DataFrame()
        for album in albums:
            current_path = artist_path + f"\\{album}"
            for song in os.listdir(current_path):
                song_dict = {'SONG': song.replace(".txt", ""), 'ALBUM': album}
                table = table.append(song_dict, ignore_index=True)
        for i in range(0, songs_table.shape[1]):
            table = pd.concat([table, songs_table.loc[:, i]], axis=1)
        return table


    """
    METHOD: KMEANS.
    Implements K-Means algorithm for 2 class (inliers and outliers).
    INPUT: artist (Artist): the Artist instance to be referenced.
           albums (List[str]): a list of albums to be referenced.
    OUTPUT: none.
    """
    @staticmethod
    def KMEANS(artist: Artist, albums: List[str]) -> None:
        artist_data = NLPArtistProcessor.__getTFIDFTable(artist, albums) # gets the tf-idf table.
        # clustering.
        songs_data = artist_data.iloc[:, 2:]
        model = KMeans(2)
        result = model.fit_predict(songs_data)
        # prints outliers.
        for i in range(0, result.shape[0]):
            if (result[i] == 2):
                print(artist_data.iloc[i, 1])

    """
    METHOD: LOF.
    Implements Local Outliers Factory algorithm.
    INPUT: artist (Artist): the Artist instance to be referenced.
           albums (List[str]): a list of albums to be referenced.
    OUTPUT: none.
    """
    @staticmethod
    def LOF(artist: Artist, albums = List[str]) -> None:
        artist_data = NLPArtistProcessor.__getTFIDFTable(artist, albums) # gets the tf-idf table.
        songs_data = artist_data.iloc[:, 2:]
        # predicting outliers.
        lof = LocalOutlierFactor(n_neighbors=int(0.1*songs_data.shape[0]))
        result = lof.fit_predict(songs_data)
        # prints outliers.
        for i in range(0, result.shape[0]):
            if(result[i]==-1):
                print(artist_data.iloc[i, 1])

    """
    METHOD: ISO_FOREST.
    Implements Isolation Forest algorithm.
    INPUT: artist (Artist): the Artist instance to be referenced.
           albums (List[str]): a list of albums to be referenced.
    OUTPUT: none.
    """
    @staticmethod
    def ISO_FOREST(artist: Artist, albums: List[str]) -> None:
        artist_data = NLPArtistProcessor.__getTFIDFTable(artist, albums) # gets the tf-idf table.
        songs_data = artist_data.iloc[:, 2:]
        # predicting outliers.
        result = IsolationForest(random_state=0).fit_predict(songs_data)
        # prints outliers.
        for i in range(0, result.shape[0]):
            if(result[i]==-1):
                print(artist_data.iloc[i, 1])

    """
    METHOD: createWordCloud.
    Analyzes and creates a word-cloud object for an artist.
    INPUT: artist (Artist): the Artist instance to be referenced.
           albums (List[str]): a list of albums to be referenced.
    OUTPUT: none.
    """
    @staticmethod
    def createWordCloud(artist: Artist, albums: List[str]) -> None:
        # gets the songs' lyrics.
        text = ""
        for album_name in albums:
            album_path = artist.artist_path + f"\\{album_name}"
            for song in os.listdir(album_path):
                file = open(f"{album_path}\\{song}", "r+")
                current_song_lyrics = file.read()
                text += current_song_lyrics
                file.close()
        NLPArtistProcessor.visualWordCloud(text) # creates a visual word-cloud.

    """
    METHOD: visualWordCloud.
    Creates a visual word-cloud out of a given text.
    INPUT: text (str): the given text.
    OUTPUT: none.
    """
    @staticmethod
    def visualWordCloud(text: str) -> None:
        stop_words = set(STOPWORDS)
        stop_words.update(open(STOPWORDS_PATH, "r+").read().split("\n"))
        colormap = random.choice(PLT_COLORMAPS)
        word_cloud = WordCloud(stopwords=stop_words,
                               background_color="white",
                               colormap=colormap,
                               max_font_size=65,
                               include_numbers=True,
                               min_word_length=3)
        word_cloud.generate(text)
        plt.imshow(word_cloud, interpolation="bilinear")
        plt.axis("off")
        plt.show()

