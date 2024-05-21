import boto3
import os

def main():
    # Get AWS credentials and region from environment variables
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    region = os.getenv('AWS_DEFAULT_REGION')
    
    if not aws_access_key_id or not aws_secret_access_key or not region:
        print("AWS credentials or region not set in environment variables.")
        return
    
    s3_bucket_name = input('Enter the S3 bucket name: ')
    dynamodb_table_name = input('Enter the DynamoDB table name: ')
    
    # Create a session with the provided credentials
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region
    )
    
    # Create S3 bucket
    s3 = session.client('s3')
    try:
        if region == 'us-east-1':
            s3.create_bucket(Bucket=s3_bucket_name)
        else:
            s3.create_bucket(
                Bucket=s3_bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
        print(f'S3 bucket "{s3_bucket_name}" created successfully.')
    except Exception as e:
        print(f'Error creating S3 bucket: {e}')
    
    # Create DynamoDB table
    dynamodb = session.client('dynamodb')
    try:
        response = dynamodb.create_table(
            TableName=dynamodb_table_name,
            KeySchema=[
                {
                    'AttributeName': 'LockID',
                    'KeyType': 'HASH'  # Partition key
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'LockID',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        dynamodb.get_waiter('table_exists').wait(TableName=dynamodb_table_name)
        print(f'DynamoDB table "{dynamodb_table_name}" created successfully.')
    except Exception as e:
        print(f'Error creating DynamoDB table: {e}')

if __name__ == '__main__':
    main()
