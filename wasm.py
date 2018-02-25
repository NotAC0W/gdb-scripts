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
        inf = gdb.selected_inferior()

        if inf.pid == 0:
            print("Target is not running")
            return

        if arg == "":
            print("No arguments")
            return

        ip = get_reg("pc")
        #arch = gdb.newest_frame().architecture().name().split(":")[0]
        arch = "amd64"

        cmd = ['pwn', 'asm', '-f','raw', '-c', arch, arg]
        opcodes = subprocess.check_output(cmd)

        inf.write_memory(ip, opcodes)

WAsm()
