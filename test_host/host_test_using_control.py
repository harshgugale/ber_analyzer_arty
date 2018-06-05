from control_prbs import *

prcon = PRBSControl()
prcon.openCon()
prcon.setErrMask(0,20)
prcon.setPRBSConfig(7,7)
print(prcon.calcBER(5))
prcon.setErrMask(0.5,20)
print(prcon.calcBER(5))
