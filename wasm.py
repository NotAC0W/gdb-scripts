import gdb
import subprocess


def get_reg(reg):
    reg = gdb.execute("info registers %s" %(reg), to_string=True)
    if reg:
        reg = reg.splitlines()
        if len(reg) > 1:
            return None
        else:
            result = int(reg[0].split()[1],0)
            return result
    return reg

class WAsm(gdb.Command):
    def __init__(self):
        super(WAsm, self).__init__ ("wasm", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        cmd = ['pwn', 'asm', '-f','raw', '-c','amd64', arg]
        result = subprocess.check_output(cmd)
        opcodes = bytearray(result)

        ip = get_reg("pc")
        for i in range(0, len(opcodes)):
            cmd = "set *((char *)0x{:x}) = 0x{:x}".format(ip+i, opcodes[i])
            #print(cmd)
            gdb.execute(cmd)

WAsm()
