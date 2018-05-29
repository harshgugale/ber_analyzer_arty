from migen import *

from tx_top import _TX
from rx_top import _RX

class top(Module):
	def __init__(self,data_width=20):
		self.config = config = Signal(2)
		self.txdata = txdata = Signal(data_width)
		self.bit_error = bit_error = Signal(32)
		self.prbs_error = Signal(data_width)

		tx = _TX(data_width)
		rx = _RX(data_width)
		self.submodules += tx, rx

		self.comb += [
			tx.tx_prbs_config.eq(config),
			rx.rx_prbs_config.eq(config),
			rx.inp.eq(txdata),
			self.bit_error.eq(rx.error),
			self.txdata.eq(tx.txdata),
			self.prbs_error.eq(rx.prbs_error)
		]

def tb(dut):
	yield dut.config.eq(0b01)
	for i in range(64):
		yield
		print("tx: {0:0{1}b} Err: {2} Err place: {3:0{1}b}".format(
			(yield dut.txdata),
			data_width,
			(yield dut.bit_error),
			(yield dut.prbs_error)))

if __name__ == "__main__":
	data_width = 20
	dut = top(data_width)
	run_simulation(dut,tb(dut))

