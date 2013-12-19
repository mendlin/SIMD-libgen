from AbstractFuncGener import AbstractFuncGener

decl_temp = '''\
SIMD_type llvm_constant_{fw}({c_type} val);
'''

impl_temp = '''\
define {vec_type} @llvm_constant_{fw}(i{fw} %val) alwaysinline {{
entry:
  %0 = insertelement {vec_type} undef, i{fw} %val, i32 0
  %1 = shufflevector {vec_type} %0, {vec_type} undef, {zero_vec_type} {zero_vec}
  ret {vec_type} %1
}}
'''


class Constant(AbstractFuncGener):

    def get_zero_vec_type(self, fw):
        return "<{n} x i32>".format(n=self.get_n(fw))

    def get_zero_mask(self, fw):
        # Different from zero constant vector
        res = "<" + "i32 0, " * self.get_n(fw) + ">"
        return res.replace(", >", ">")

    def get_decl(self, fw, c_type):
        return decl_temp.format(fw=fw, c_type=c_type)

    def get_impl(self, fw, c_type):
        return impl_temp.format(vec_type=self.config.get_vec_type(fw), fw=fw,
                                zero_vec_type=self.get_zero_vec_type(fw),
                                zero_vec=self.get_zero_mask(fw))

    def drive(self):
        AbstractFuncGener.drive(self, c_type=True)
