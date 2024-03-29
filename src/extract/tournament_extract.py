import requests
import json
import csv
from datetime import datetime

def extract_tournament() -> list:
    '''
    Extracts response from lichess API and creates a list containing the 
    information

    Parameters:
        None

    Returns:
        list: a list of lists with each inner list containing values for: 
            tournament id, 
            fullName, 
            variant, 
            perf(bullet, rapid, etc.),
            maxRating(if applicable), 
            winner id,
            winner name, 
            duration 
                note**(all in order)
    '''
    response = requests.get('https://lichess.org/api/tournament')
    response_json = json.loads(response.content)
    
    all_passes = []
    
    for response in response_json['finished']:
    
        try:
            current_pass = []
            current_pass.append(response['id'])
            current_pass.append(response['fullName'])
            current_pass.append(response['variant']['key'])
            current_pass.append(response['perf']['key'])
            try:
                current_pass.append(response['maxRating']['rating'])
            except(KeyError):
                current_pass.append('null')
            current_pass.append(response['winner']['id'])
            current_pass.append(response['winner']['name'])
            current_pass.append((response['finishesAt'] 
                                 - response['startsAt']) / 60000)

            #Converting the unix time into a readable date
            timestamp_start = datetime.fromtimestamp(
                response['startsAt'] / 1000)
            current_pass.append(timestamp_start.strftime(
                '%Y-%m-%d %H:%M:%S'))
            timestamp_end = datetime.fromtimestamp(
                response['finishesAt'] / 1000)
            current_pass.append(timestamp_end.strftime(
                '%Y-%m-%d %H:%M:%S'))
            all_passes.append(current_pass)
        except(Exception):
            continue
    
    return all_passes


def tournament_to_csv(tournament: list) -> str:
    '''
    Turns a list of tournament values and converts it into a csv file, stored 
    in folder 'tournament'

    Parameters:
        tournament(list): list of lists containing the values of the 
            tournament
    
    Returns:
        String: the name of the csv file that was created w/ format for name:
        'tournament' + the datetime the file was created + '.csv'
    '''
    current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    str_current_datetime = str(current_datetime)

    # Naming convention to better organize files
    # that are extracted ie. tournament/, winner_games/, etc.
    file_name = 'tournament/' + str_current_datetime + '.csv'

    print('Creating file...')

    with open(file_name, 'w') as fp:
        csvw = csv.writer(fp, delimiter='|')
        csvw.writerow(['tournament_id', 'fullName', 'variant', 'perf',
                        'maxRating', 'winner_id', 'winner_name', 'duration',
                        'startsAt', 'finishesAt'])
        csvw.writerows(tournament)
    
    fp.close()

    return file_name


if __name__ == '__main__':
    array = extract_tournament()
    csv_file = tournament_to_csv(array)

    print('Extracted info: ',  array)
    print('CSV file name: ' + csv_file)