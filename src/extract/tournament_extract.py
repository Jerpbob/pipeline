import requests
import json
import csv
import configparser
import boto3
from datetime import datetime

def extract_tournament():
    '''
    Extracts tournament id, fullName, variant, perf(bullet, rapid, etc.), maxRating(if applicable), winner id and name, duration
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


def tournament_to_csv(tournament):
    current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    str_current_datetime = str(current_datetime)
    file_name = 'tournament/' + str_current_datetime + '.csv'

    print('Creating file...')

    with open(file_name, 'w') as fp:
        csvw = csv.writer(fp, delimiter='|')
        csvw.writerow(['tournament id', 'fullName', 'variant', 'perf', 'maxRating', 'winner id', 'winner name', 'duration'])
        csvw.writerows(tournament)
    
    fp.close()

    return file_name

def csv_to_s3(csv_file):
    parser = configparser.ConfigParser()
    parser.read("/home/jerp/repos/pipeline/pipeline.conf")
    access_key = parser.get('aws_boto_credentials', 'access_key')
    secret_key = parser.get('aws_boto_credentials', 'secret_key')
    bucket_name = parser.get('aws_boto_credentials', 'bucket_name')

    print('Connecting to s3...')

    s3 = boto3.client(
        's3',
        aws_access_key_id = access_key,
        aws_secret_access_key = secret_key
    )

    print('Uploading file...')

    s3.upload_file(
        csv_file,
        bucket_name,
        csv_file
    )


if __name__ == '__main__':
    array = extract_tournament()
    csv_file = tournament_to_csv(array)
    csv_to_s3(csv_file)