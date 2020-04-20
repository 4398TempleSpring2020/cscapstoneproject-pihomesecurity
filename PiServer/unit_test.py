#!usr/bin/python3
from sensor_manager import Sensor_Manager
from microphone import Microphone
from camera import Camera
from ultra_proc import UltraProc
from mic_proc import MicProc
import os
import unittest
from run_sensors import run_sensors

class TestSensors(unittest.TestCase):
    # ensure running sensors returns a tuple with 4 items, each containing non null information
    def test_running_sensors(self):
        bucket_name = "mypishield"
        acc_old_id = 11

        # run all sensors
        ret_vals = run_sensors(10, acc_old_id, bucket_name)

        # check length
        self.assertEquals(len(ret_vals), 4)        

        # unpack it and check existance
        ret_list, anomaly_dict, instance_id, acc_id = ret_vals
        self.assertTrue(ret_list not None)
        self.assertTrue(anomaly_dict not None)
        self.assertEquals(len(anomaly_dict), 3)
        self.assertTrue(instance_id not None)
        self.assertTrue(acc_id not 11)
        
    # test that we recognize far anomalies for ultra
    def test_ultra_proc_far(self):
        ultraProc = UltraProc()
        fname = "./data/ultra/far_anomaly.txt"
        isAnom = ultraProc.isAnomaly(fname)

        self.assertEquals(isAnom, True)

    # test that we recognize medium anomalies for ultra
    def test_ultra_proc_med(self):
        ultraProc = UltraProc()
        fname = "./data/ultra/medium_anomaly.txt"
        isAnom = ultraProc.isAnomaly(fname)

        self.assertEquals(isAnom, True)

    # test that we recognize close anomalies for ultra
    def test_ultra_proc_close(self):
        ultraProc = UltraProc()
        fname = "./data/ultra/close_anomaly.txt"
        isAnom = ultraProc.isAnomaly(fname)

        self.assertEquals(isAnom, True)

    # test that we do not recognize static anomalies for ultra
    def test_ultra_proc_close(self):
        ultraProc = UltraProc()
        fname = "./data/ultra/static_anomaly.txt"
        isAnom = ultraProc.isAnomaly(fname)

        self.assertEquals(isAnom, False)

    # test that we do not recognize distant walking anomalies for ultra
    def test_ultra_proc_close(self):
        ultraProc = UltraProc()
        fname = "./data/ultra/offscreenwalking.txt"
        isAnom = ultraProc.isAnomaly(fname)

        self.assertEquals(isAnom, False)

    # test that we recognize close anomalies for mic
    def test_mic_proc_close(self):
        ultraProc = MicProc()
        fname = "./data/mic/close_talking.wav"
        isAnom = micProc.isAnomaly(fname)

        self.assertEquals(isAnom, True)

    # test that we recognize loud clapping for mic
    def test_mic_proc_loud(self):
        ultraProc = MicProc()
        fname = "./data/ultra/medium_anomaly.wav"
        isAnom = micProc.isAnomaly(fname)

        self.assertEquals(isAnom, True)

    # test that we do not recognize silent fo mic
    def test_mic_proc_silent(self):
        ultraProc = MicProc()
        fname = "./data/mic/silent.wav"
        isAnom = ultraProc.isAnomaly(fname)

        self.assertEquals(isAnom, False)

    # test that exactly twice the number of files downloaded are in the downloads folder
    # (i.e. each face has a corresponding meta file)
    def test_s3_user_face_download_count(self):
        client = S3_Client()
        files = client.get_user_face_files("mypishield", 11)
        num_files = len(files)

        downloaded_contents = os.listdir('./faces')
        num_downloaded = len(downloaded_contents)
        self.assertEquals(num_files * 2, num_downloaded)

    # test that each meta file exists after downloading faces
    def test_s3_user_face_download_meta(self):
        client = S3_Client()
        files = client.get_user_face_files("mypishield", 11)

        meta_files = []
        for file_a in files:
            meta_files.append(path_a.split('.')[:-1][0] + "_meta.txt")

        for mfile in meta_files:
            assertEquals(os.path.exists(mfile), True)

    # test that each face file exists after downloading faces
    def test_s3_user_face_download(self):
        client = S3_Client()
        files = client.get_user_face_files("mypishield", 11)

        for file_a in files:
            assertEquals(os.path.exists(file_a), True)

if __name__ == '__main__':
    unittest.main()
