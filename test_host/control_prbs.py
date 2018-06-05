from litex.soc.tools.remote import RemoteClient
import time

class PRBSControl:
	def __init__ (self):
		self.wb = RemoteClient()

	def openCon(self):
		self.wb.open()

	def setPRBSConfig(self,txConfig,rxConfig):
		Txval = 0
		Rxval = 0
		if txConfig is 7:
			Txval = 0b00
		elif txConfig is 15:
			Txval = 0b01
		elif txConfig is 23:
			Txval = 0b10
		elif txConfig is 31:
			Txval = 0b11
		else:
			Txval = None

		if rxConfig is 7:
			Rxval = 0b00
		elif rxConfig is 15:
			Rxval = 0b01
		elif rxConfig is 23:
			Rxval = 0b10
		elif rxConfig is 31:
			Rxval = 0b11
		else:
			Rxval = None

		if Txval is not None: 
			self.wb.regs.top_tx_config.write(Txval)
			time.sleep(0.001)
		
		if Rxval is not None:
			self.wb.regs.top_rx_config.write(Rxval)
			time.sleep(0.001)

	def setErrMask(self,error_fraction, data_width):
		mask = 1
		for i in range(round(data_width*error_fraction) - 1):
			mask = mask <<1
			mask = mask + 1

		if error_fraction is 0:
			self.wb.regs.top_mask.write(0)
		else:
			self.wb.regs.top_mask.write(mask)
		time.sleep(0.001)

	def calcBER(self,timems):
		self.wb.regs.top_enable_err_count.write(0b00)
		time.sleep(0.001)

		self.wb.regs.top_enable_err_count.write(0b11)

		c1 = int(self.wb.regs.top_total_bit_count.read())
		err1 = int(self.wb.regs.top_global_error.read())

		self.wb.regs.top_enable_err_count.write(0b01)

		time.sleep(timems*0.001)

		self.wb.regs.top_enable_err_count.write(0b11)

		err2 = int(self.wb.regs.top_global_error.read())
		c2 = int(self.wb.regs.top_total_bit_count.read())

		ber = ((err2-err1)/(20*(c2-c1)))
		#print("c1 {} c2 {} e1 {} e2 {}".format(c1,c2,err1,err2))
		#print("Bit error ratio : {}".format(ber))
		return ber

	def closeCon(self):
		self.wb.close()




