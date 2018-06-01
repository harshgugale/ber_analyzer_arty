from migen import *

from tx_top import _TX
from rx_top import _RX

class top(Module):
	def __init__(self,data_width=20):
		self.tx_config = Signal(2)
		self.rx_config = Signal(2)
		#self.errors = Signal(32) 
		self.global_error = bit_error = Signal(32)
		self.bit_wise_errors = Signal(data_width)
		self.bit_error = Signal(8)
		self.mask = Signal(data_width)
		self.mask_config = Signal(2)

		mask50 = 1
		for i in range(data_width):
			if(mask50 < 2**data_width):
				mask50 = mask50 << 2
				mask50 = mask50 + 1

		tx = _TX(data_width)
		rx = _RX(data_width)
		self.submodules += tx, rx

		self.comb += [
			tx.tx_prbs_config.eq(self.tx_config),
			rx.rx_prbs_config.eq(self.rx_config),
			If(
			self.mask_config == 00, self.mask.eq(0)
			).Else(
			self.mask.eq(mask50)
			),
			rx.rxdata.eq(tx.txdata ^ self.mask),
			#self.errors.eq(rx.errors),
			self.bit_wise_errors.eq(rx.bit_wise_errors)
		]

		valadd = Signal(32)

		for i in range(data_width):
			valadd = valadd + self.bit_wise_errors[i]

		self.sync += self.bit_error.eq(valadd)
		self.sync += self.global_error.eq(self.global_error + self.bit_error)


def tb(dut):
	yield dut.tx_config.eq(0b01)
	yield dut.rx_config.eq(0b00)
	for i in range(16):
		yield
    # start rx and verify we dont have errors:
	yield dut.mask_config.eq(0b01)
	yield dut.tx_config.eq(0b01)
	yield dut.rx_config.eq(0b01)
	for i in range(64):
		yield
		#print("cycle:{0}, errors: {1} err : {2}".format(i, (yield dut.bit_error), (yield dut.bit_wise_errors)))
    # change tx and verify that we now have errors on rx
	yield dut.mask_config.eq(0b00)
	yield dut.tx_config.eq(0b01)
	yield dut.rx_config.eq(0b01)
	for i in range(64):
		yield

		#print("cycle:{0}, errors: {1} err : {2}".format(i, (yield dut.bit_error) , (yield dut.bit_wise_errors)))


if __name__ == "__main__":
	data_width = 20
	dut = top(data_width)
	run_simulation(dut,tb(dut),vcd_name="top_prbs.vcd")

