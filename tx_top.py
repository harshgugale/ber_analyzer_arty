from migen import *
from transceiver_test.transceiver.prbs import *
#from 

class tx(Module):
	def __init__ (self,data_width = 20):
		self.tx_produce_square_wave = tx_produce_square_wave = Signal(reset = 0)
		self.tx_prbs_config = tx_prbs_config = Signal(2)

		#self.rx_prbs_config = rx_prbs_config = Signal(2)
		#self.rx_prbs_errors = rx_prbs_errors = Signal(32)

		self.txdata = txdata = Signal(data_width)
		#self.rxdata = Signal(data_width)

		prbs_tx = PRBSTX(data_width)

		self.submodules+=prbs_tx

		self.comb+=[prbs_tx.config.eq(tx_prbs_config),txdata.eq(prbs_tx.o)]




def tb(dut,data_width):
	yield dut.tx_prbs_config.eq(0b10)
	#for i in range(50):
	yield
	print("{0:0{1}b} ".format((yield dut.txdata),data_width))

if __name__ == "__main__":
	data_width = 40
	dut = tx(data_width)
	run_simulation(dut,tb(dut,data_width),vcd_name = "tx_mod")







