import time

class PRBSControl:
	def __init__ (self,regs,name):
		self.regs = regs
		self.name = name
		self.build()

	def build(self):
		for key, value in self.regs.d.items():
			if self.name == key[:len(self.name)]:
				key = key.replace(self.name + "_", "")
				setattr(self, key, value)

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
			self.tx_config.write(Txval)
			time.sleep(0.001)
		
		if Rxval is not None:
			self.rx_config.write(Rxval)
			time.sleep(0.001)

	def setErrMask(self,error_fraction, data_width):
		mask = 1
		for i in range(round(data_width*error_fraction) - 1):
			mask = mask <<1
			mask = mask + 1

		if error_fraction is 0:
			self.mask.write(0)
		else:
			self.mask.write(mask)
		time.sleep(0.001)

	def calcBER(self,timems, data_width):
		self.enable_err_count.write(0b00)
		time.sleep(0.001)
		self.enable_err_count.write(0b11)

		c1 = int(self.total_bit_count.read())
		err1 = int(self.global_error.read())

		self.enable_err_count.write(0b01)
		time.sleep(timems*0.001)
		self.enable_err_count.write(0b11)

		err2 = int(self.global_error.read())
		c2 = int(self.total_bit_count.read())

		ber = ((err2-err1)/(data_width*(c2-c1)))
		return ber





