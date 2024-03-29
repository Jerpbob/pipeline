import json
import requests
import csv
from datetime import datetime

def extract_winner_games(winner: str, tournament_id: str) -> list:
    '''
    Extracts values of games of the winner of a tournament in the tournament
    corresponding to the tournament ID

    Parameters:
        winner(str): winner name
        tournament_id(str): ID of desired tournament

    Returns:
        List: a list of lists with information of the winner's games in the
            tournament:
                tournament id, 
                game id, 
                variant, 
                duration, 
                ECO, 
                opening name, 
                ply(amount of moves that followed an opening), 
                white player (name), 
                black player (name),
                status (how game was ended), 
                winner (white or black)
            note**(all in order)
    '''
    response = requests.get(
    f'https://lichess.org/api/tournament/{tournament_id}/games',
    headers={'Accept': 'application/x-ndjson'},
    params={'player': winner, 'opening': True})

    #Decode content into readable 'nd-json' string
    response_content = response.content.decode('utf-8')

    #Split the string by '\n' b/c nd-json is separated by '\n' rather
    # than commas like in json
    #The last item is ommitted b/c it is a '\n'
    response_json = response_content.split("\n")[:-1]

    all_passes = []

    for json_item in response_json:
        try:
            current_pass = []
    
            game_info = json.loads(json_item)
            current_pass.append(tournament_id)
            current_pass.append(winner)
            current_pass.append(game_info['id'])
            current_pass.append(game_info['variant'])
            current_pass.append(round(((game_info['lastMoveAt'] - 
                                        game_info['createdAt']) / 60000), 2))
            
            #Converting the unix time into a readable date
            timestamp_start = datetime.fromtimestamp(
                game_info['createdAt'] / 1000)
            current_pass.append(timestamp_start.strftime(
                '%Y-%m-%d %H:%M:%S'))
            timestamp_end = datetime.fromtimestamp(
                game_info['lastMoveAt'] / 1000)
            current_pass.append(timestamp_end.strftime(
                '%Y-%m-%d %H:%M:%S'))

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
        print(all_passes)

    return all_passes

def winner_games_to_csv(winner_games: list) -> str:
    '''
    Turns a list of the winner's games and its corresponding information
    and turns it into a csv file stored in folder 'games'

    Parameters:
        winner_games(list): a list of lists containing the information of the
            winner's games
    
    Returns:
        String: name of the csv file created with format: 
            'games/' + datetime file was created + '.csv'
    '''
    current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    str_current_datetime = str(current_datetime)

    # Naming convention to better organize files that are extracted
    # ie. tournament/, winner_games/, etc.
    file_name = 'games/' + str_current_datetime + '.csv'

    print('Creating file...')

    with open(file_name, 'w') as fp:
        csvw = csv.writer(fp, delimiter='|')
        csvw.writerow(['tournament_id', 'tournament_winner', 'game_id',
                    'game_var', 'duration', 'createdAt', 'lastMoveAt',
                        'ECO', 'opening_name', 'opening_ply', 'white_id',
                            'black_id', 'status', 'game_winner'])
        csvw.writerows(winner_games)
    
    fp.close()

    return file_name
    

if __name__ == '__main__':
    array = extract_winner_games('indeec', '0tn2GQSi')
    csv_file = winner_games_to_csv(array)

    print('Extracted info: ', array)
    print('CSV file name: ' + csv_file)