import sys 
sys.path.append('..')

from litex.soc.tools.remote import RemoteClient
from control_prbs import *

wb = RemoteClient()
wb.open()
prcon = PRBSControl(wb.regs,"top")
prcon.setErrMask(0,20)
prcon.setPRBSConfig(7,7)
print(prcon.calcBER(5,20))
prcon.setErrMask(0.2,20)
print(prcon.calcBER(5,20))
