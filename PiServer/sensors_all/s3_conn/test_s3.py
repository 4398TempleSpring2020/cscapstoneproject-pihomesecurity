#!usr/bin/python3

from s3_client import s3_client

if __name__ == "__main__":    
        client = s3_client()

        # list all buckets in S3
        s3_buckets = client.list_buckets()

        bucket_name = 'whateverworks'        
        download_list = client.get_user_files(bucket_name)
        print(download_list)
        '''
        client.upload_file('../microphone.py', bucket_name, 'mic.py')
 
        client.create_bucket('lukes-new-test-bucket-boy')

        client.download_from_s3(bucket_name, './test_download.py', 'mic.py')

        client.delete_from_s3(bucket_name, 'mic.py')
'''
