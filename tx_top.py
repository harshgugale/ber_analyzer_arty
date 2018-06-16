from migen import *
from litex.soc.cores.code_8b10b import *
from prbs import *


class _TX(Module):
	def __init__ (self,data_width=40):
		self.tx_prbs_config = tx_prbs_config = Signal(2)
		self.input = Signal(data_width)
		self.txdata_int = txdata_int = Signal(data_width)
		self.txdata = txdata = Signal(data_width)
		self.seldata = Signal()
		self.en8b10b = Signal()
		self.mask = Signal(data_width)

		prbs_tx = PRBSTX(data_width)
		enc = Encoder(4)
		self.submodules += prbs_tx,enc

		#seldata 0 - PRBS output
		#seldata 1 - input to module

		self.comb += [
			If(self.seldata == 0,
			prbs_tx.config.eq(tx_prbs_config),
			txdata_int.eq(prbs_tx.o ^ self.mask)
			).Else(
			txdata_int.eq(self.input)
			)
		]

		self.comb += [
			enc.d[0].eq(txdata_int[:8]),
			enc.d[1].eq(txdata_int[8:16]),
			enc.d[2].eq(txdata_int[16:24]),
			enc.d[3].eq(txdata_int[24:32]),
			If(self.en8b10b == 1,
			txdata[:10].eq(enc.output[0]),
			txdata[10:20].eq(enc.output[1]),
			txdata[20:30].eq(enc.output[2]),
			txdata[30:40].eq(enc.output[3])
			).Else(
			txdata.eq(txdata_int),
			)

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
