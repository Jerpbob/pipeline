import configparser
import boto3

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
    from tournament_extract import extract_tournament, tournament_to_csv
    
    array = extract_tournament()
    csv_file = tournament_to_csv(array)
    csv_to_s3(csv_file)