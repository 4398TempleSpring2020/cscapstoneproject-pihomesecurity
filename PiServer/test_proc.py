from ultra_proc import UltraProc
from mic_proc import MicProc
import sys

ultraProc = UltraProc()
micProc = MicProc()

fname = [sys.argv[1]]

#isAnom = ultraProc.isAnomaly(fname)
isAnom = micProc.isAnomaly(fname)

print(isAnom)

