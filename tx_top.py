from migen import *

from prbs import *


class _TX(Module):
	def __init__ (self,data_width=20):
		#self.tx_produce_square_wave = tx_produce_square_wave = Signal(reset = 0)
		self.tx_prbs_config = tx_prbs_config = Signal(2)

		self.txdata = txdata = Signal(data_width)

		prbs_tx = PRBSTX(data_width)
		self.submodules += prbs_tx

		self.comb += [
			prbs_tx.config.eq(tx_prbs_config),
			txdata.eq(prbs_tx.o)
		]


def tb(dut,data_width):
	yield dut.tx_prbs_config.eq(0b10)
	for i in range(3):
		yield
		print("{0:0{1}b} ".format((yield dut.txdata),data_width))

if __name__ == "__main__":
	data_width = 20
	dut = _TX(data_width)
	run_simulation(dut,tb(dut,data_width),vcd_name = "tx_mod")
