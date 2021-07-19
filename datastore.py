import boto3
import json

from botocore.errorfactory import ClientError

s3 = boto3.resource('s3')

class Datastore():
    """Datastore allows us to persist some data outside the application.
    
    The data property is loaded initially from S3 and then cached for the
    lifetime of the application (subsequent reads will not pull from S3).
    """
    def __init__(self, s3_bucket="porkbutts-discoball", s3_key="data.json"):
        self.s3_obj = s3.Object(s3_bucket, s3_key)
        self.__data = None
        
    @property
    def data(self):
        """Return data if we have it cached otherwise retrieve from S3.

        Returns:
            object: arbitrary json data deserialized to a python dict
        """
        if not self.__data:
            try:
                self.__data = json.load(self.s3_obj.get()['Body'])
            except ClientError:
                self.__data = {}
        return self.__data
     
     
    def save(self):
        """Serializes self.__data as json and saves the result to S3.
        """
        self.s3_obj.put(Body=json.dumps(self.__data))
        
