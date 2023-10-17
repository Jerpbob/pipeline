import requests
import json

def extract_tournament():
    '''
    Extracts id, fullName, variant, perf(bullet, rapid, etc.), maxRating(if applicable), winner id and name, duration
    from url and returns information as lists within a list for inputting into a csv file
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
            current_pass.append((response['finishesAt'] - response['startsAt']) / 60000)
            all_passes.append(current_pass)
        except(Exception):
            continue
    
    return all_passes


if __name__ == '__main__':
    for passes in extract_tournament():
        print(passes)
        print('---------------------------')