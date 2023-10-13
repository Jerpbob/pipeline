import requests
import json

response = requests.get('https://lichess.org/api/tournament')
response_json = json.loads(response.content)

tournament_types = []

for headers in response_json:
        tournament_types.append(headers)

if __name__ == '__main__':
    print(tournament_types)
    print(len(response_json['finished']))