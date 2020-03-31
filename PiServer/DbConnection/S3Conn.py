import boto3


# boto/s3 tutorial http://boto.cloudhackers.com/en/latest/s3_tut.html


class S3Conn:

    def __init__(self):
        self.key = None
        self.connection = None
        self.bucket = None

    def connect(self):
        #read akey and skey
        conn = boto3.connect_s3('<AKIAJPS6AE2SDVHWCTUA>', '</xqBOSjc7mRYdVpmWKfbnyyei5jHjh3T7umxtwbz>')
        return conn



