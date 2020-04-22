import csv
import os
from bs4 import BeautifulSoup
import wikipedia
import requests


# Uses Wikipdia to grab all country artists
def get_country_artists():
    wiki_country_artists = wikipedia.page("List of country music performers")
    # Artists can come with unnecessary additional description
    cleaned_artists = [x.replace('(band)', '').replace('(musician)', '').strip() for x in wiki_country_artists.links]
    return cleaned_artists


def get_song_data(song):
    song_url = song.get('href')
    title = song.get_text()
    lyrics = ""
    try:
        response = requests.get(song_url)
        song_data = BeautifulSoup(response.content, "html.parser")
        # Lyrics are separated into <p> tags with class "verse"
        verses = song_data.find_all("p", class_="verse")
        for verse in verses:
            # Lyric scrape has multiple <br> tags. Text manipulation / bs4 used to replace with newlines
            verse_with_blank_lines = verse.get_text(separator="\n").strip()
            lyrics += "\n".join([line for line in verse_with_blank_lines.split("\n") if line != ''])
            # Indicates that a chorus has ended
            if "[Chorus]" in verse_with_blank_lines:
                lyrics += "\n[End Chorus]\n"
            else:
                lyrics += "\n"
    except Exception as e:
        print("Requests error:")
        print(e)
    return {'lyrics': lyrics, 'title': title}


def get_artist_data(artist):
    base_url = "http://www.metrolyrics.com/"
    # Attempts to find artist by generating a URL in Metrolyrics format
    metrolyrics_artist_url = base_url + artist.replace(' ', '-') + '-lyrics'
    response = requests.get(metrolyrics_artist_url)
    artist_data = {
        'artist_url': metrolyrics_artist_url,
        'artist_name': artist,
        'artist_content': BeautifulSoup(response.content, "html.parser")
    }
    return artist_data


def scrape_and_save(artists):
    for artist in artists:
        # TODO: target try/except more directly
        try:
            song_items = []
            artist_data = get_artist_data(artist=artist)
            songs = artist_data['artist_content'].find_all("a", href=True, class_="title")
            for song in songs:
                song_data = get_song_data(song=song)
                song_item = {
                    'artist': artist_data['artist_name'],
                    'title': song_data['title'],
                    'lyrics': song_data['lyrics'],
                }
                song_items.append(song_item)
            # Write out all artist lyrics to file with artist name separated by underscores
            parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            lyrics_directory = os.path.join(parent_directory, 'lyric_data')
            file_path = os.path.join(lyrics_directory, artist_data['artist_name'].replace(' ', '_') + '.csv')
            print(file_path)
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['artist', 'title', 'lyrics']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for item in song_items:
                    writer.writerow({'artist': item['artist'], 'title': item['title'], 'lyrics': item['lyrics']})
        except Exception as e:
            print(e)
            pass


def all_lyrics_to_txt():
    parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    lyrics_directory = os.path.join(parent_directory, 'lyric_data')
    for root, dirs, files in os.walk(lyrics_directory, topdown=False):
        for file in files:
            print(os.path.join(root, file))
            with open(os.path.join(root, file), newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    print(row['artist'])
                    with open("combined_files.txt", "a", encoding='utf-8') as txtfile:
                        if row['lyrics'] != '':
                            txtfile.write(row['lyrics'])



