import csv, requests

# Function to get artist information from Spotify API
def getArtistInfo(headers, id):
    BASE_URL = 'https://api.spotify.com/v1/artists/'
    r = requests.get(BASE_URL + id, headers=headers)
    return r.json()

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
with open("test.csv", 'r', encoding='latin-1') as csv_file, open('newnodes.csv', 'w', newline='', encoding='utf-8') as updated_csv_file:
    reader = csv.DictReader(csv_file)
    fieldnames = ['id','name', 'popularity', 'followers']
    writer = csv.DictWriter(updated_csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for row in reader:
        spotify_id = row['id']
        info = getArtistInfo(headers, spotify_id)
        row['name'] = info['name']
        row['popularity'] = info['popularity']
        row['followers'] = info['followers']['total']
        writer.writerow(row)
        total += 1
        print("Artists added: " + str(total))