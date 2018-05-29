from migen import *
from transceiver_test.transceiver.prbs import *

class _RX(Module):
	def __init__(self,data_width):
		self.rx_prbs_config = rx_prbs_config = Signal(2)
		self.inp = inp = Signal(data_width)
		self.error = error = Signal(32)
		self.prbs_error = Signal(data_width)

		prbs_rx = PRBSRX(data_width)

		self.submodules+=prbs_rx

		self.comb+=[prbs_rx.config.eq(rx_prbs_config),prbs_rx.i.eq(inp),self.error.eq(prbs_rx.errors),
		self.prbs_error.eq(prbs_rx.prbs_errors)]

class RX(Module):
	def __init__ (self, data_width):
		self.rx_prbs_config = Signal(2)
		self.inp1 = inp1 = Signal(data_width)
		self.error = CSRStatus(32)

		_rx = _RX(data_width)

		self.submodules+= _rx

		self.comb+=[_rx.rx_prbs_config.eq(self.rx_prbs_config),_rx.inp.eq(inp1),self.error.status.eq(_rx.error)]
