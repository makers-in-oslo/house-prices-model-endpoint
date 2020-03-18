import pickle
import boto3


def stream_pickle(aws_access_key_id, aws_secret_access_key, Bucket, Key):
    """
    stream pickle object from AWS S3 so that the object is not stored temporary on disk
    
    Parameters:
    -----------
    aws_acces_key_id: str
        AWS acces key id
    aws_secret_access_key: str
        AWS secret access key
    Bucket: str
        Bucket name
    Key: str
        File name
    
    returns:
    --------
    Depends on the stored object
    """
    session = boto3.session.Session()
    s3client = session.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )
    response = s3client.get_object(Bucket=Bucket, Key=Key)
    body_string = response["Body"].read()
    return pickle.loads(body_string)
