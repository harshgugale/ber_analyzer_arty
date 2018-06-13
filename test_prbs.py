from migen import *

from prbs import PRBSTX, PRBSRX

class DUT(Module):
    def __init__(self, width, delay=16):
        self.submodules.tx = PRBSTX(width)
        self.submodules.rx = PRBSRX(width)
        # connect tx to rx
        data = self.tx.o
        for i in range(delay):
            new_data = Signal(32)
            self.sync += new_data.eq(data)
            data = new_data
        self.comb += self.rx.i.eq(data)


def tb(dut):
    # start tx and wait some cycles to allow rx to synchronize
    yield dut.tx.config.eq(0b01)
    yield dut.rx.config.eq(0b00)
    for i in range(128):
        yield
    # start rx and verify we dont have errors:
    yield dut.tx.config.eq(0b01)
    yield dut.rx.config.eq(0b01)
    for i in range(64):
        yield
        print("cycle:{}, errors: {}".format(i, (yield dut.rx.bit_wise_errors)))
    # change tx and verify that we now have errors on rx
    yield dut.tx.config.eq(0b11)
    yield dut.rx.config.eq(0b00)
    for i in range(16):
        yield
    yield dut.tx.config.eq(0b11)
    yield dut.rx.config.eq(0b01)
    for i in range(64):
        yield
        print("cycle:{}, errors: {}".format(i, (yield dut.rx.bit_wise_errors)))

if __name__ == "__main__":
    dut = DUT(32)
    run_simulation(dut, tb(dut), vcd_name="test_prbs.vcd")
