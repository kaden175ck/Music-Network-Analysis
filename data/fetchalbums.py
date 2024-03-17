import csv, requests
from requests.exceptions import RequestException, JSONDecodeError

# Function to get artist information from Spotify API
def getArtistAlbums(headers, id):
    try:
        BASE_URL = 'https://api.spotify.com/v1/artists/'+id+'/albums?market=US'
        r = requests.get(BASE_URL, headers=headers)
        albms = r.json()
        listofalbums = []
        for i in albms['items']:
            listofalbums.append(i)
        return listofalbums
    except:
        print("Failed get artist: " + r.text)
        exit()

def getArtistLinks(headers, albums):
    try:
        album_ids = [album.get("id") for album in albums]
        albums_str = ','.join(album_ids[:20])
        BASE_URL = 'https://api.spotify.com/v1/albums?ids=' + albums_str
        
        r = requests.get(BASE_URL, headers=headers)
        r.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        
        edges = []
        res = r.json()
        if 'albums' not in res:
            return edges
        
        album_owner = res['albums'][0]['artists'][0]['id']
        
        for artist in res['albums']:
            for track in artist.get('tracks', {}).get('items', []):
                for sub_artist in track.get('artists', []):
                    sub_artist_id = sub_artist.get('id')
                    if sub_artist_id and sub_artist_id != album_owner:
                        edges.append(f"{album_owner}:{sub_artist_id}")
        
        return edges
    
    except RequestException as e:
        print(f"Request Exception: {e}")
        return []
    except JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        return []
    except KeyError as e:
        print(f"KeyError occurred: {e}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Spotify API credentials and authorization
AUTH_URL = 'https://accounts.spotify.com/api/token'
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': 'e8d47edc9deb470797e482d27e043381',
    'client_secret': 'ac6a80c2ce2948e993de097f98ad02e4',
})
auth_response_data = auth_response.json()
access_token = auth_response_data['access_token']
headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}

total = 0
with open("newnodes.csv", 'r', encoding='latin-1') as csv_file, open('edges.csv', 'w', newline='', encoding='utf-8') as updated_csv_file:
    reader = csv.DictReader(csv_file)
    fieldnames = ['id_1','id_2']
    writer = csv.DictWriter(updated_csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for row in reader:
        spotify_id = row['id']
        albums = getArtistAlbums(headers, spotify_id)
        links = getArtistLinks(headers, albums)
        for link in links:
            id_1, id_2 = link.split(":") 
            writer.writerow({'id_1': id_1, 'id_2': id_2})
        total += 1
        print("Artists added: " + str(total))