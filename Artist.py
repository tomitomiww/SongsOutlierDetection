import time
import os
import requests
from datetime import date
from bs4 import BeautifulSoup
from Constants import DATA_STATUS, DATA_PATH, EXISTING_DATA_PATH, DATA_SEPERATION_CHAR, SKIP_LIST
from typing import List

"""
CLASS: Artist.
Represents an artist by its name, data_status, data-path and the albums which were already read.
"""
class Artist:
    """
    METHOD: __init__
    Initialize an Artist's instance by creating its path and reading the artist's songs.
    INPUT: artist_name (str): the artist's name.
    OUTPUT: none.
    """
    def __init__(self, artist_name: str):
        self.__artist_name: str = None # the artist's name.
        self.__artist_path: str = None # the artist's data's path.
        self.__existing_albums: List[str] = None # the albums which were read.

        self.__artist_name = artist_name
        self.__artist_path = DATA_PATH + f"\\{self.__artist_name}"
        # checks which part of the artist's discography already exists.
        data_status = self.checkExistingData() # gets the artist's data-status.
        if(data_status==DATA_STATUS.FULL):
            self.__artist_path = DATA_PATH + f"\\{self.__artist_name}"
            return
        self.__existing_albums = []
        # if some of the artist's discography already exists (but not all).
        if (data_status == DATA_STATUS.SEMI_FULL):
            self.__existing_albums = os.listdir(DATA_PATH + f"\\{self.__artist_name}")
        self.setArtistPath() # sets the artist's path and reads their song.

        all_artists_lines = open(EXISTING_DATA_PATH, "r+").readlines() # all the data about the existed artists.
        # searches for the artist's name in the data list.
        # writes the artist's name or updates their last updating-date.
        with open(EXISTING_DATA_PATH, "w") as file:
            FOUND = False
            text = ""
            for line in all_artists_lines:
                # if the current line is the artist's line.
                if (line.strip().startswith(self.__artist_name)):
                    FOUND = True
                    text += f"\n{self.__artist_name}@{self.getDate()}@"
                else:
                    line = line.strip("\n")
                    text += f"\n{line}"
            # if the artist wasn't written as an existing data.
            if (not FOUND):
                text += f"\n{self.__artist_name}@{self.getDate()}@"
            file.write(text)

    """
    METHOD: checkExistingData.
    Checks if all of the artist's albums exist, some or none.
    INPUT: none.
    OUTPUT: the status of the artist's discography (DATA_STAUS).
    """
    def checkExistingData(self) -> DATA_STATUS:
        existing_data = open(EXISTING_DATA_PATH, "r+")
        artists_list = existing_data.readlines()
        # searches for the artist, and checks if their discography has been updated.
        for artist in artists_list:
            data_list = artist.split(DATA_SEPERATION_CHAR)
            if(data_list[0]!=self.__artist_name):
                continue
            new_albums = input(f"[?] Did {self.__artist_name} released new albums since {data_list[1].strip()}? (y/n) ")
            if(new_albums.lower() in ["n", "no"]):
                return DATA_STATUS.FULL
            else:
                return DATA_STATUS.SEMI_FULL
        existing_data.close()
        return DATA_STATUS.EMPTY


    """
    METHOD: setArtistPath.
    Sets an artist's path and reads their discography.
    INPUT: none.
    OUTPUT: the artist's path (str).
    """
    def setArtistPath(self) -> None:
        artist_page = self.getArtistPage()  # gets the artist's AZ-Lyrics page.
        # gets the artist's albums' names.
        all_artist_albums = artist_page.findAll('div', class_='album')
        all_artist_albums = all_artist_albums[0:len(all_artist_albums)-1]
        # checks which albums are needed.
        needed_artist_albums = [x.get_text().strip().replace('album: ', '').replace('"','') for x in all_artist_albums]
        needed_artist_albums = [x for x in needed_artist_albums if x not in self.__existing_albums]
        if(len(needed_artist_albums) > 0):
            self.setData(artist_page, needed_artist_albums)  # gets the songs which are missing.

    """
    METHOD: getArtistPage.
    Gets the artist's AZ-Lyrics page as a BeautifulSoup object.
    INPUT: none.
    OUTPUT: the artist's AZ-Lyrics page (BeautifulSoup).
    """
    def getArtistPage(self) -> BeautifulSoup:
        artist_url = f"https://www.azlyrics.com/{self.__artist_name[0]}/{self.__artist_name}.html"
        artist_page = requests.get(artist_url)  # tries to open the correct page.
        # if the program couldn't open the page.
        if(str(artist_page.status_code)[0]!='2'):
            print(f"[!] ERROR - the status code from {artist_url} was {artist_page.status_code}.")
            exit(1)
        return BeautifulSoup(artist_page.content, "html.parser")

    """
    METHOD: setData.
    Sets the artist's data, by creating a folder for each album and reading each of their songs.
    The method skips singles, EPs, remixes, demo's and audiobooks.
    INPUT: artist_page (BeautifulSoup): the artist's AZ-Lyrics page.
           needed_artist_albums (List[str]): the albums which don't exist in the data.
    OUTPUT: none.
    """
    def setData(self, artist_page: BeautifulSoup, needed_artist_albums: List[str]) -> None:
        album_count = 0 # the current album's index.
        current_album = f"({album_count}) {needed_artist_albums[0]}" # the current name of the album.
        current_path = self.__artist_path + f"\\{current_album}" # the current path (of the current album).
        skip_album = "" # an album the program should skip reading.
        try:
            os.mkdir(self.__artist_path)
        except FileExistsError:
            pass
        # finds all the albums and all the song's names and links.
        albums_and_songs = artist_page.findAll(True, {'class':["album", "listalbum-item"]})
        for item in albums_and_songs:
            should_skip = False # should the program skip this item?
            # if an item is a EP, remix, demo or audiobook: skips it.
            for skip in SKIP_LIST:
                if item.get_text().strip().replace('album: ', '').replace('"', '').startswith(skip):
                    skip_album = item.get_text().strip().replace('album: ', '').replace('"', '')
                    current_path = current_path.replace(current_album, skip_album)
                    current_album = skip_album
                    should_skip = True
                if should_skip:
                    continue

            # if the item is an album which wasn't read before.
            if item.get_text().strip().replace('album: ', '').replace('"','') in needed_artist_albums:
                # creates a folder with the album's name.
                new_album = item.get_text().strip().replace('album: ','').replace('"','')
                album_count += 1
                new_album = f"({album_count}) {new_album}"
                current_path = current_path.replace(current_album, new_album)
                try:
                    os.mkdir(current_path)
                except FileExistsError:
                    pass
                except:
                    print(f"[*] Couldn't create a folder for the album: {current_album}")
                current_album = new_album
                continue
            # if the item is an album which was read before, skip it.
            if item.get_text().strip().replace('album: ', '').replace('"', '') in self.__existing_albums:
                skip_album = item.get_text().strip().replace('album: ', '').replace('"', '')
                album_count += 1
                skip_album = f"({album_count}) {skip_album}"
                current_path = current_path.replace(current_album, skip_album)
                current_album = skip_album
                continue
            if(current_album==skip_album):
                continue

            # if the item is a song.
            time.sleep(10) # sleeps so AZ-Lyrics won't block the IP.
            try:
                # the program doesn't read singles.
                if(item.get_text().strip().startswith("other songs:")):
                    break
                # reads the song's lyrics.
                song_link = f"http://azlyrics.com{item.find('a')['href']}"
                self.setSongLyrics(song_link, current_path)
            except TypeError:
                print(f"[*] Couldn't reach the song: {item.get_text().strip()}")

    """
    METHOD: setSongLyrics.
    Sets a song's lyrics in its album's folder.
    INPUT: song_link (str): the link to the song's page.
           current_path (str): the current album's path.
    OUTPUT: none.
    """
    def setSongLyrics(self, song_link: str, current_path: str) -> None:
        # tries to gain access to the song's page.
        try:
            song_request = requests.get(song_link)
        except:
            return
        if(str(song_request.status_code)[0]!='2'):
            print(f"[!] ERROR - the status code from {song_link} was {song_request.status_code}.")
            exit(1)
        song_page = BeautifulSoup(song_request.content, "html.parser")
        # reads the song's lyrics from its html, and gets rid of irrelevant data.
        messy_song = song_page.findAll("div")[11].get_text().strip()
        start_char = 0
        enter_counter = 0
        while (start_char < len(messy_song) and enter_counter < 3 and messy_song[start_char]!='['):
            if (messy_song[start_char] == '\n'):
                enter_counter += 1
            else:
                enter_counter = 0
            start_char += 1
            if (enter_counter == 3 and messy_song[start_char] == '\n'):
                enter_counter = 0
        if(messy_song[start_char]!='['):
            start_char += 2
        end_char = start_char
        while(not(messy_song[end_char]=='\n' and messy_song[end_char+1]=='\n' and messy_song[end_char+2]=='\n')):
            end_char += 1
        clean_song = messy_song[start_char:end_char]

        # gets the song's title.
        song_title = song_page.findAll("b")[1].get_text()[1:-1]
        song_path = current_path +f"\\{song_title}.txt"
        # writes the lyrics to the file.
        if(os.path.isfile(song_path)):
            return
        try:
            song_file = open(song_path, "w+")
            chars_written = song_file.write(clean_song)
            if(chars_written != len(clean_song)):
                print(f"[*] Couldn't write all the lyrics to {song_title}.")
        except Exception as e:
            print(e)
        return

    @property
    def artist_name(self) -> str:
        return self.__artist_name

    @property
    def artist_path(self) -> str:
        return self.__artist_path

    def getDate(self) -> str:
        today = date.today()
        day = today.strftime("%d")
        month = today.strftime("%B")[0:3].upper()
        year = today.strftime("%Y")
        return f"{day}-{month}-{year}"