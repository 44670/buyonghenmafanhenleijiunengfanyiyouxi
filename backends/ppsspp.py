import psutil
import time
from ctypes import *
from ctypes.wintypes import *
from struct import pack, unpack
from util import getProcessByName, getModuleBase, openProcess, readMemory, writeMemory, failure

PPSSPP_RAM_BASE_POINTER_OFFSET = 0xCEBF24

def readPspUserRam(address, bufSize):
    global processHandle, ppssppBaseAddr
    return readMemory(processHandle, ramBaseAddr + address, bufSize)
    

def writePspUserRam(address, buf):
    global processHandle, ppssppBaseAddr
    return writeMemory(processHandle, ramBaseAddr + address, buf)


proc = getProcessByName('PPSSPPWindows.exe')
if proc is None:
    print('PPSSPP(32bit) is not running!')
    exit(0)

pid = proc.pid
ppssppBaseAddr = getModuleBase(proc, 'PPSSPPWindows.exe')
if ppssppBaseAddr == 0: 
    failure('PPSSPP module not found!')

processHandle = openProcess(pid)

(ramBaseAddr, ) = unpack('I', readMemory(processHandle, ppssppBaseAddr + PPSSPP_RAM_BASE_POINTER_OFFSET, 4))
print('PPSSPP: PSP user ram base addr: %08x' % ramBaseAddr)
if ramBaseAddr == 0:
    failure('No psp game running in the emulator.')
