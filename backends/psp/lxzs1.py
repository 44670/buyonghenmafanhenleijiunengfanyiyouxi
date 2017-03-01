import time
from backends.ppsspp import readPspUserRam, writePspUserRam
from struct import pack, unpack


GAME_DIALOG_MEM_OFFSET = 0x9170dc
GAME_TEXT_MEM_OFFSET = 0x906588
GAME_PATCH_OFFSET = 0x807b9c
GAME_CHAR_INFO_OFFSET = 0x905EE0+0x4000
GAME_CHAR_INFO_OFFSET_2 = 0x905EE0+0x3d58

def appendStrToResultObj(ret, row, col, v):
    if (row < 0):
        return
    if (len(v) == 0):
        return
    ret['r'].append(row)
    ret['c'].append(col)
    ret['v'].append(v)


def readGameString2():
    global ramBaseAddr
    bufStr = u''
    (cnt,) = unpack('I', readPspUserRam( GAME_CHAR_INFO_OFFSET_2, 4))
    if (cnt != 0):
        return None
    ret =  {
        'status': 'ok',
        'backend': 'psp.4lxzs1',
        'r': [],
        'c': [],
        'v': []
    }
    (itemCount,) = unpack('I', readPspUserRam( GAME_CHAR_INFO_OFFSET, 4))
    if (itemCount > 256):
        itemCount = 256
    buf = readPspUserRam( GAME_TEXT_MEM_OFFSET, itemCount * 0x1C)
    lastRow = -1
    lastCol = -1
    for i in range(0, itemCount):
        tmp = buf[i*0x1c:i*0x1c + 0x1c]
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
    return  ret

def readGameStringForHttpApi():
    cnt = 0
    lastStr = None
    for i in range(0, 5):
        ret = readGameString2()
        if (ret is None):
            continue
        if (lastStr is None):
            lastStr = ret
        if (lastStr != ret):
            cnt = 0
        lastStr = ret
        cnt += 1
        if (cnt >= 3):
            break
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            exit(0)
    if (cnt >= 3):
        return lastStr
    return None


writePspUserRam(GAME_PATCH_OFFSET, '\x00\x40\xe2\xac')
