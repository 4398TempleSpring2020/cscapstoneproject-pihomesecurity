#from scipy import stats
#import scipy
#import statistics
#from scipy import stats
#import scipy.stats
from ultra_proc import UltraProc
from mic_proc import MicProc
import sys
#from s3_client import S3_Client

#scipy.stats.zscore([1,2,3,4])

ultraProc = UltraProc()
micProc = MicProc()

fname = [sys.argv[1]]

#isAnom = ultraProc.isAnomaly(fname)
isAnom = micProc.isAnomaly(fname)

#client = S3_Client()
#files = client.get_user_face_files("mypishield", 11)
#print(files)

print(isAnom)

