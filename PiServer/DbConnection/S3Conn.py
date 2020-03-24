import boto


# http://boto.cloudhackers.com/en/latest/s3_tut.html


class S3Conn:

    def __init__(self):
        self.key = None
        self.connection = None
        self.bucket = None

    def connect(self):
        conn = boto.connect_s3('<AKIAIDZRKUSDQLB2QRZA>', '<Cz0DRacat119j1NsPEgnTVXawElfwVzBSWMMcemv>')
        return conn


if __name__ == '__main__':
    db = S3Conn()
    S3Conn.connection = S3Conn.connect(db)
    print(S3Conn.connection)
