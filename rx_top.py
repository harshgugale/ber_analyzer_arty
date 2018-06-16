from migen import *
from litex.soc.cores.code_8b10b import *
from prbs import *

class _RX(Module):
	def __init__(self, data_width = 40):
		self.rx_prbs_config = rx_prbs_config = Signal(2)
		self.en8b10b = Signal()
		self.mask = Signal(data_width)
		self.rxdata = rxdata = Signal(data_width)
		self.bit_wise_errors = Signal(data_width)

		prbs_rx = PRBSRX(data_width)
		dec0 = Decoder()
		dec1 = Decoder()
		dec2 = Decoder()
		dec3 = Decoder()
		self.submodules += prbs_rx, dec0, dec1, dec2, dec3

		self.comb += [
			prbs_rx.config.eq(rx_prbs_config),
			prbs_rx.mask.eq(self.mask),
			If(self.en8b10b == 0,
			prbs_rx.i.eq(rxdata),
			self.bit_wise_errors.eq(prbs_rx.bit_wise_errors)
			).Else(
			dec0.input.eq(rxdata[:10]),
			dec1.input.eq(rxdata[10:20]),
			dec2.input.eq(rxdata[20:30]),
			dec3.input.eq(rxdata[30:]),
			prbs_rx.i[:8].eq(dec0.d),
			prbs_rx.i[8:16].eq(dec1.d),
			prbs_rx.i[16:24].eq(dec2.d),
			prbs_rx.i[24:32].eq(dec3.d),
			self.bit_wise_errors.eq(prbs_rx.bit_wise_errors & 0x00FFFFFFFF)
			)
		]
