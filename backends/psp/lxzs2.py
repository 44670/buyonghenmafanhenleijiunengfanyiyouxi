import time
from backends.ppsspp import readPspUserRam, writePspUserRam
from struct import pack, unpack


GAME_TEXT_MEM_OFFSET = 0xa2f740
TEXT_MEM_MAX_ENTRY = 256
lastTextMem = []
lastCharCount = 0
lastRet = {}

def appendStrToResultObj(ret, row, col, v):
    if (row < 0):
        return
    if (len(v) == 0):
        return
    ret['r'].append(row)
    ret['c'].append(col)
    ret['v'].append(v)

def readTextMem():
    return readPspUserRam( GAME_TEXT_MEM_OFFSET, TEXT_MEM_MAX_ENTRY * 0x1C)

def getChangedCharCount(mem1, mem2):
    for i in range(TEXT_MEM_MAX_ENTRY-1, -1, -1):
        if (mem1[i*0x1c:i*0x1c + 0x1c] != mem2[i*0x1c:i*0x1c + 0x1c]):
            return i + 1
    return 0

def readGameString2():
    global ramBaseAddr, lastTextMem
    textMem = readTextMem()
    changedCharCount = getChangedCharCount(lastTextMem, textMem)
    #print(changedCharCount)
    if changedCharCount <= 0:
        return None
    lastTextMem = textMem
    ret =  {
        'status': 'ok',
        'backend': 'psp.lxzs2',
        'r': [],
        'c': [],
        'v': []
    }
    lastRow = -1
    lastCol = -1
    bufStr = u''
    for i in range(0, changedCharCount):
        tmp = textMem[i*0x1c:i*0x1c + 0x1c]
        (col, row) = unpack('II', tmp[0:8])
        if (tmp[0x18] == '\0'):
            continue
        flag = ord(tmp[0x17])
        if (flag == 2): continue
        if (row != lastRow):
            appendStrToResultObj(ret, lastRow, lastCol, bufStr)
            lastRow = row
            lastCol = col
            bufStr = u''
        dec = tmp[0x10:0x10+2].decode('shift_jis', 'ignore')
        bufStr += dec
    appendStrToResultObj(ret, lastRow, lastCol, bufStr)
    return ret

def readGameStringForHttpApi():
    global lastRet
    cnt = 0
    for i in range(0, 5):
        ret = readGameString2()
        if (ret is None):
            cnt += 1
        else:
            lastRet = ret
            cnt = 0 
        if (cnt >= 3):
            break
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            exit(0)
    if (cnt >= 3):
        return lastRet

lastTextMem = readTextMem()
