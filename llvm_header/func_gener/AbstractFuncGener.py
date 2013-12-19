class AbstractFuncGener:

    def __init__(self, doth, dotll, config):
        self.doth = doth
        self.dotll = dotll
        self.config = config

    def get_decl(self):
        print("Func Decl")

    def get_impl(self):
        print("Func Implementation")

    def drive(self, c_type=False):
        # Driver, append function decl and impl to doth and dotll
        if c_type:
            # Drive with c_type
            for c_type in self.config.c_type_fw:
                fw = self.config.c_type_fw[c_type]
                self.doth.write(self.get_decl(fw, c_type))
                self.dotll.write(self.get_impl(fw, c_type))
        else:
            # Drive with fw in fw_set
            for fw in self.config.fw_set:
                self.doth.write(self.get_decl(fw))
                self.dotll.write(self.get_impl(fw))
