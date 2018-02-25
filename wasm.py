import gdb
import re
import subprocess


def get_current_arch():
    arch = gdb.newest_frame().architecture().name()
    #list 'borrowed' from pwndbg
    arches = ['x86-64', 'i386', 'mips', 'powerpc', 'sparc', 'arm', 'aarch64', arch]
    arch = next(a for a in arches if a in arch)
    if arch == "x86-64":
        arch = "amd64"

    return arch

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
    """Write assembler on the fly into memory
wasm                              - Shows context used
wasm <assembler code ... >        - Write at current $pc
wasm <addr> <assembler code ... > - Write at address <addr>
wasm context <context>            - Set context for pwntools asm to <context>. no argument unsets context
    """
    def __init__(self):
        super(WAsm, self).__init__ ("wasm", gdb.COMMAND_USER)
        self.context = None


    def invoke(self, arg, from_tty):
        cmd = arg.split(" ", 1)
        cmd.append(None)

        if arg == "":
            self.show_context()
        elif cmd[0] == "context":
            self.set_context(cmd[1])
        elif re.match("^0x[0-9a-fA-F]+$", cmd[0]):
            self.patch_addr(int(cmd[0], 16), cmd[1])
        else:
            self.patch_pc(arg)

    def show_context(self):
        if self.context == None:
            if gdb.selected_inferior().pid != 0:
                print("Context determined automatically as: {}".format(get_current_arch()))
            else:
                print("No Context set, and not in a running target")
        else:
            print("Context for pwntool asm: {}".format(self.context))


    def set_context(self, context):
        self.context = context

    def patch_pc(self, code):
        if gdb.selected_inferior().pid == 0:
            print("Target is not running, no $pc register available")
            return

        ip = get_reg("pc")
        self.patch_addr(ip, code)

    def patch_addr(self, addr, code):
        inf = gdb.selected_inferior()

        if inf.pid == 0:
            print("Target is not running, there is no memory")
            return

        context = self.context
        if context == None:
            context = get_current_arch()

        cmd = ['pwn', 'asm', '-f','raw', '-c', context, code]
        opcodes = subprocess.check_output(cmd)

        inf.write_memory(addr, opcodes)


WAsm()
