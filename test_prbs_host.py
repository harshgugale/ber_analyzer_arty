#!/usr/bin/env python3

from litex.soc.tools.remote import RemoteClient
import time

wb = RemoteClient()
wb.open()

# # #
wb.regs.top_enable_err_count.write(0)
wb.regs.top_tx_config.write(0x01)
wb.regs.top_rx_config.write(0x00)
time.sleep(0.001)

wb.regs.top_tx_config.write(0x01)
wb.regs.top_rx_config.write(0x01)
wb.regs.top_mask.write(0b0)

wb.regs.top_enable_err_count.write(1)
for i in range(10):
    print(int(wb.regs.top_global_error.read()))
    time.sleep(0.01)

wb.regs.top_enable_err_count.write(0)

wb.regs.top_tx_config.write(0x01)
wb.regs.top_rx_config.write(0x00)
time.sleep(0.001)

wb.regs.top_rx_config.write(0x01)
wb.regs.top_mask.write(0xFFFFF)
for i in range(10):
	wb.regs.top_enable_err_count.write(1)
	c1 = int(wb.regs.top_total_bit_count.read())
	err1 = int(wb.regs.top_global_error.read())
	time.sleep(0.5)
	err2 = int(wb.regs.top_global_error.read())
	c2 = int(wb.regs.top_total_bit_count.read())
	ber = ((err2-err1)/(20*(c2-c1)))
	print("c1 {} c2 {} e1 {} e2 {}".format(c1,c2,err1,err2))
	print("Bit error ratio : {}".format(ber))
	wb.regs.top_enable_err_count.write(0)
	time.sleep(0.001)
# # #

wb.close()
