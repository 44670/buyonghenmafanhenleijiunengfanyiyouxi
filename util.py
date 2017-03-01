import psutil
from ctypes import *
from ctypes.wintypes import *
from struct import pack, unpack

OpenProcess = windll.kernel32.OpenProcess
ReadProcessMemory = windll.kernel32.ReadProcessMemory
WriteProcessMemory = windll.kernel32.WriteProcessMemory
CloseHandle = windll.kernel32.CloseHandle
PROCESS_ALL_ACCESS = 0x1F0FFF

def getProcessByName(pname):
    for proc in psutil.process_iter():
        if proc.name() == pname:
            return proc
    return None

def getModuleBase(proc, modname):
    mmap = proc.memory_maps(grouped=False)
    for mem in mmap:
        if mem.path.endswith(modname):
            return int(mem.addr, 16)
    return 0

def openProcess(pid):
    return OpenProcess(PROCESS_ALL_ACCESS, False, pid) 

def readMemory(processHandle, address, bufSize):
    buffer = create_string_buffer(bufSize)
    ret = ReadProcessMemory(processHandle, address, buffer, bufSize, None)
    return buffer.raw

def writeMemory(processHandle, address, buf):
    buffer = create_string_buffer(len(buf))
    buffer.raw = buf
    ret = WriteProcessMemory(processHandle, address, buffer, len(buf), None)


def binStrToHexArray(buf):
    ret = ''
    for i in range(0, len(buf)):
        ret += '%02x ' % ord(buf[i])
    return ret

def failure(msg):
    print(msg)
    print('exiting...')
    exit(0)