from AbstractFuncGener import AbstractFuncGener

decl_temp = '''\
SIMD_type llvm_ifh_{fw}(SIMD_type mask, SIMD_type a, SIMD_type b);
'''

impl_temp = '''\
define {vec_type} @llvm_ifh_{fw}({vec_type} %mask, {vec_type} %a, {vec_type} %b) alwaysinline {{
entry:
    %0 = icmp slt {vec_type} %mask, {zero_vec}
    %1 = select {bool_vec_type} %0, {vec_type} %a, {vec_type} %b
    ret {vec_type} %1
}}
'''

class IFH(AbstractFuncGener):
	def get_decl(self, fw, ir_func=None):		
		return decl_temp.format(fw=fw)

	def get_zero_vec(self, fw):
		n = self.config.register_bits / fw
		res = "<" + "i{fw} 0, ".format(fw=fw) * n + ">"		
		return res.replace("0, >", "0>")

	def get_impl(self, fw, ir_func=None):
		vt = self.config.get_vec_type(fw)
		bvt = self.config.get_bool_vec_type(fw)
		return impl_temp.format(vec_type=vt, bool_vec_type=bvt, fw=fw,
								zero_vec=self.get_zero_vec(fw))
