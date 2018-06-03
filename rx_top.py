from migen import *

from prbs import *

class _RX(Module):
	def __init__(self, data_width):
		self.rx_prbs_config = rx_prbs_config = Signal(2)
		self.rxdata = rxdata = Signal(data_width)
		self.bit_wise_errors = Signal(data_width)

		prbs_rx = PRBSRX(data_width)
		self.submodules += prbs_rx

		self.comb += [
			prbs_rx.config.eq(rx_prbs_config),
			prbs_rx.i.eq(rxdata),
			If(
			rx_prbs_config == 00, 
			self.bit_wise_errors.eq(0)
			).Else(
			self.bit_wise_errors.eq(prbs_rx.bit_wise_errors)
			)
		]