import urllib.parse
import logging
from botocore.exceptions import ClientError
from app.api.dependencies import client


async def upload_file_to_s3(file, file_name, bucket_name):
    try:
        client.upload_fileobj(
            Fileobj=file,
            Bucket=bucket_name,
            Key=file_name,
        )
    except ClientError as e:
        logging.error(e)
        return None

    response = client.generate_presigned_url('get_object',
                                             Params={'Bucket': bucket_name,
                                                     'Key': file_name},
                                             ExpiresIn=999999)
    return response
