class AbstractFuncGener:
	def __init__(self, doth, dotll, config):
		self.doth = doth
		self.dotll = dotll
		self.config = config

	def get_decl(self, fw, ir_func):
		print("Func Decl")

	def get_impl(self, fw, ir_func):
		print("Func Implementation")

	def drive(self, ir_func=None):
		# Driver, append function decl and impl to doth and dotll
		for fw in self.config.fw_set:
			self.doth.write(self.get_decl(fw, ir_func))
			self.dotll.write(self.get_impl(fw, ir_func))
