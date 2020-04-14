from ultra_proc import UltraProc
import sys

ultraProc = UltraProc()

fname = [sys.argv[1]]

isAnom = ultraProc.isAnomaly(fname)
print(isAnom)

