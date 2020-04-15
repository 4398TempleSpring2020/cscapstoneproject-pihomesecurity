#!usr/bin/python3

import logging
import boto3
from botocore.exceptions import ClientError
import os

class S3_Client():
    s3_client = None
    session = None
    s3 = None
    
    def __init__(self):
        keys = []
        with open('/home/pi/Desktop/secrets.txt', 'r') as secFile:
            sec_file = secFile.readlines()
            for line in sec_file:
                keys.append((line.split(',')[-1]).strip())

        self.session = boto3.Session(
            aws_access_key_id=keys[0],
            aws_secret_access_key=keys[1]
        )

        self.s3 = self.session.resource("s3")
        
        self.s3_client = self.session.client('s3')

    def list_buckets(self):
        # Retrieve the list of existing buckets
        response = self.s3_client.list_buckets()
        
        # Output the bucket names
        print('Existing buckets:')
        for bucket in response['Buckets']:
            print(bucket['Name'])

    def create_bucket(self, bucket_name):
        # Create bucket
        try:
            self.s3_client.create_bucket(Bucket=bucket_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def upload_file(self, file_name, bucket, object_name=None):
        """Upload a file to an S3 bucket
        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """
        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = file_name

        # Upload the file
        try:
            print("Uploading [" + object_name + "]")
            response = self.s3_client.upload_file(file_name, bucket, object_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def upload_image_file(self, file_name, bucket, object_name=None):
        """Upload a file to an S3 bucket
        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """
        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = file_name

        # Upload the file
        try:
            response = self.s3_client.upload_file(file_name, bucket, object_name,
                                                  ExtraArgs={"ContentType" : "image/jpeg"})
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def get_user_files(self, bucket_name):
        result = self.s3_client.list_objects_v2(Bucket=bucket_name)
        print('-----------')
        print(result)
        print('-----------')
        keys = []
        total_size = 0.0
        if 'Contents' in result:
            for obj in result.get('Contents'):
                cur_file = obj.get('Key')                
                keys.append(cur_file)
        return keys

    # stores face files from s3 on local machine
    def get_user_face_files(self, bucket_name, acc_id):
        face_path = str(acc_id) + '/faces/'
        result = self.s3_client.list_objects_v2(Bucket=bucket_name)

        keys = []
        total_size = 0.0
        if 'Contents' in result:
            for obj in result.get('Contents'):
                cur_file = obj.get('Key')                
                cur_meta = obj.get("LastModified")
                if(cur_file.startswith(face_path)):
                    keys.append((cur_file, cur_meta))

        ret_files = []
        meta_files = []
        for face_file, meta in keys:
            path_a = face_file.split('/')[1:]
            path_a = path_a[0] + '/' + path_a[1]
            ret_files.append(path_a)

            meta_path = path_a.split('.')[:-1][0] + "_meta.txt"
            meta_files.append(meta_path)
            
            if(not os.path.exists(face_file) or not os.path.exists(meta_path)):
                # if files are not already downloaded, download images, remake meta
                self.download_from_s3(bucket_name, path_a, face_file)                
                with open(meta_path, "w") as meta_file:
                    meta_file.write(str(meta))

            # read meta data
            meta_old = None        
            with open(meta_path, 'r') as meta_file:
                meta_old = meta_file.readlines()[0]

            if(not str(meta) == meta_old):
                # if files are not up to date, download images, remake meta
                self.download_from_s3(bucket_name, path_a, face_file)                
                with open(meta_path, "w") as meta_file:
                    meta_file.write(str(meta))

        # remove files from local machine that do not exist in s3
        local_files = os.listdir("faces/")
        for lfile in local_files:
            lfile = 'faces/' + lfile
            if(not(lfile in ret_files or lfile in meta_files)):
                print('deleting [' + lfile + "]")
                os.remove(lfile)
        return ret_files
    
    def delete_from_s3(self, bucketname, filename):
        # Upload the file
        obj = self.s3.Object(bucketname, filename)
        obj.delete()
        
    def download_from_s3(self, bucketname, filename, object_name):
        self.s3_client.download_file(bucketname, object_name, filename)
