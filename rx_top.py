from migen import *

from prbs import *

class _RX(Module):
	def __init__(self, data_width):
		self.rx_prbs_config = rx_prbs_config = Signal(2)
		self.rxdata = rxdata = Signal(data_width)
		#self.errors = errors = Signal(32)
		self.bit_wise_errors = Signal(data_width)

		prbs_rx = PRBSRX(data_width)
		self.submodules += prbs_rx

		self.comb += [
			prbs_rx.config.eq(rx_prbs_config),
			prbs_rx.i.eq(rxdata),
			If(
			rx_prbs_config == 00, 
			#self.errors.eq(0) ,
			self.bit_wise_errors.eq(0)
			).Else(
			#self.errors.eq(prbs_rx.errors),
			self.bit_wise_errors.eq(prbs_rx.bit_wise_errors)
			)
		]

class RX(Module):
	def __init__ (self, data_width):
		self.rx_prbs_config = Signal(2)
		self.inp1 = inp1 = Signal(data_width)
		self.errors = CSRStatus(32)

		_rx = _RX(data_width)
		self.submodules+= _rx

		self.comb += [
			_rx.rx_prbs_config.eq(self.rx_prbs_config),
			_rx.inp.eq(inp1),
			self.errors.status.eq(_rx.errors)
		]
