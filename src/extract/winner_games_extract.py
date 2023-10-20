import json
import requests

def extract_winner_games(winner, tournament_id):
    '''
    Extracts (through inputs winner, tournament_id) tournament id (for grouping), game id, variant, duration, ECO, opening name, 
    ply(amount of moves that followed an opening), white player, black player, status (how game was ended),
    winner (white or black)
    '''
    response = requests.get(
    f'https://lichess.org/api/tournament/{tournament_id}/games',
    headers={'Accept': 'application/x-ndjson'},
    params={'player': winner, 'opening': True})

    #Decode content into readable 'nd-json' string
    response_content = response.content.decode('utf-8')

    #Split the string by '\n' b/c nd-json is separated by '\n' rather than commas like in json
    #The last item is ommitted b/c it is a '\n'
    response_json = response_content.split("\n")[:-1]

    all_passes = []

    for json_item in response_json:
        try:
            current_pass = []

            game_info = json.loads(json_item)
            current_pass.append(tournament_id)
            current_pass.append(game_info['id'])
            current_pass.append(game_info['variant'])
            current_pass.append(round(((game_info['lastMoveAt'] - game_info['createdAt']) / 60000), 2))
            current_pass.append(game_info['opening']['eco'])
            current_pass.append(game_info['opening']['name'])
            current_pass.append(game_info['opening']['ply'])
            current_pass.append(game_info['players']['white']['user']['id'])
            current_pass.append(game_info['players']['black']['user']['id'])
            current_pass.append(game_info['status'])
            current_pass.append(game_info['winner'])

            all_passes.append(current_pass)
        except(Exception):
            continue

    return all_passes

if __name__ == '__main__':
    for passes in extract_winner_games('mvarela', 'eztiV8ax'):
        print(passes)
        print('----------------')