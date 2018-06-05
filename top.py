from migen import *
from litex.soc.interconnect.csr import *
from tx_top import _TX
from rx_top import _RX

class _Top(Module):
	def __init__(self,data_width=20):
		self.tx_config = Signal(2)
		self.rx_config = Signal(2)
		self.global_error = Signal(32)
		self.bit_wise_errors = Signal(data_width)
		self.bit_error = Signal(8)
		self.mask = Signal(data_width)
		self.enable_err_count = Signal(2)
		self.total_bit_count = Signal(32)

		tx = _TX(data_width)
		rx = _RX(data_width)
		self.submodules += tx, rx

		self.comb += [
			tx.tx_prbs_config.eq(self.tx_config),
			rx.rx_prbs_config.eq(self.rx_config),
			rx.rxdata.eq((tx.txdata ^ self.mask)),
			self.bit_wise_errors.eq(rx.bit_wise_errors)
		]

		valadd = Signal(32)

		for i in range(data_width):
			valadd = valadd + self.bit_wise_errors[i]

		self.sync += self.bit_error.eq(valadd)
		self.sync += [
			If(self.enable_err_count == 0b01,
			self.global_error.eq(self.global_error + self.bit_error),
			self.total_bit_count.eq(self.total_bit_count + 1)
			).Elif(self.enable_err_count == 0b11,
			self.global_error.eq(self.global_error),
			self.total_bit_count.eq(self.total_bit_count)
			).Elif(self.enable_err_count == 0b00,
			self.global_error.eq(0),
			self.total_bit_count.eq(0)
			)]

class Top(Module, AutoCSR):
	def __init__ (self):
		self.tx_config = CSRStorage(2)
		self.rx_config = CSRStorage(2)
		self.mask = CSRStorage(20)
		self.global_error = CSRStatus(32)
		self.total_bit_count = CSRStatus(32)
		self.enable_err_count = CSRStorage(2)

		_top = _Top()
		self.submodules += _top

		self.comb += [
		_top.tx_config.eq(self.tx_config.storage),
		_top.rx_config.eq(self.rx_config.storage),
		_top.mask.eq(self.mask.storage),
		_top.enable_err_count.eq(self.enable_err_count.storage),
		self.global_error.status.eq(_top.global_error),
		self.total_bit_count.status.eq(_top.total_bit_count)
		]


def tb(dut):
	yield dut.tx_config.eq(0b01)
	yield dut.rx_config.eq(0b00)
	for i in range(16):
		yield
    
	yield dut.mask.eq(0x0)
	yield dut.enable_err_count.eq(0b00)
	yield dut.tx_config.eq(0b01)
	yield dut.rx_config.eq(0b01)

	for i in range(8):
		yield
	
	yield dut.enable_err_count.eq(0b01)

	for i in range(64):
		yield

	yield dut.enable_err_count.eq(0b11)

	for i in range(8):
		yield

	yield dut.enable_err_count.eq(0b00)

	yield dut.mask.eq(0x55555)
	yield dut.tx_config.eq(0b00)
	yield dut.rx_config.eq(0b00)

	for i in range(8):
		yield
	
	yield dut.enable_err_count.eq(0b01)

	for i in range(64):
		yield

	yield dut.enable_err_count.eq(0b11)

	for i in range(8):
		yield

if __name__ == "__main__":
	data_width = 20
	dut = _Top(data_width)
	run_simulation(dut,tb(dut),vcd_name="top_prbs.vcd")

