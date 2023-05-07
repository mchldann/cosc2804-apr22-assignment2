from mcpi.minecraft import Minecraft
from mcpi import block
from memory import mem_read, mem_write, Registers, reg_read, reg_write
from utils import sign_extend, is_windows
import sys

if is_windows:
    import msvcrt
else:
    import getch


mc = Minecraft.create()


class Halt(Exception):
    """Thrown to indicate HALT instruction has been executed."""

    pass


def _GETC():
    """get character from keyboard,
    character is not echoed onto the console."""
    ch = msvcrt.getch() if is_windows else getch.getch()
    reg_write(Registers.R0, ord(ch))


def _OUT():
    """output a character"""
    sys.stdout.write(chr(reg_read(Registers.R0)))
    sys.stdout.flush()


def _PUTS():
    """output a word string"""
    for i in range(reg_read(Registers.R0), 2**16):
        ch = mem_read(i)
        if ch == 0:  # check if the char is not null then print this char
            break
        sys.stdout.write(chr(ch))
    sys.stdout.flush()  # equal to fflush() in c


def _IN():
    """input a single character, echoed onto the console"""
    sys.stdout.write("Enter a character: ")
    sys.stdout.flush()
    reg_write(Registers.R0, ord(sys.stdin.read(1)))


def _PUTSP():
    """output a byte string"""
    for i in range(reg_read(Registers.R0), 2**16):
        c = mem_read(i)
        if c == 0:
            break
        sys.stdout.write(chr(c & 0xFF))
        char = c >> 8
        if char:
            sys.stdout.write(chr(char))
    sys.stdout.flush()


def _HALT():
    """halt the program"""
    raise Halt()


# Same as reg_read, except returns a signed 16-bit integer instead of unsigned.
def reg_read_signed(which):
    unsigned = reg_read(which)
    return (unsigned + 2**15) % 2**16 - 2**15


def _CHAT_POST():
    message = ""
    for i in range(reg_read(Registers.R0), 2**16):
        c = mem_read(i)
        if c == 0:
            break
        message = message + chr(c & 0xFF)
        char = c >> 8
        if char:
            message = message + chr(char)

    mc.postToChat(message)


def _GET_PLAYER_TILE():
    playerTile = mc.player.getTilePos()
    reg_write(Registers.R0, playerTile.x)
    reg_write(Registers.R1, playerTile.y)
    reg_write(Registers.R2, playerTile.z)


def _SET_PLAYER_TILE():
    x = reg_read_signed(Registers.R0)
    y = reg_read_signed(Registers.R1)
    z = reg_read_signed(Registers.R2)

    mc.player.setTilePos(x, y, z)


def _GET_BLOCK():
    x = reg_read_signed(Registers.R0)
    y = reg_read_signed(Registers.R1)
    z = reg_read_signed(Registers.R2)

    block_id = mc.getBlock(x, y, z)
    reg_write(Registers.R3, block_id)


def _SET_BLOCK():
    x = reg_read_signed(Registers.R0)
    y = reg_read_signed(Registers.R1)
    z = reg_read_signed(Registers.R2)

    block_id = reg_read(Registers.R3)
    mc.setBlock(x, y, z, block_id)


def _GET_HEIGHT():
    x = reg_read_signed(Registers.R0)
    z = reg_read_signed(Registers.R2)

    height = mc.getHeight(x, z)
    reg_write(Registers.R1, height)


def _PRINT_REGISTERS():
    print("R0: " + str(reg_read(Registers.R0)))
    print("R1: " + str(reg_read(Registers.R1)))
    print("R2: " + str(reg_read(Registers.R2)))
    print("R3: " + str(reg_read(Registers.R3)))
    print("R4: " + str(reg_read(Registers.R4)))
    print("R5: " + str(reg_read(Registers.R5)))
    print("R6: " + str(reg_read(Registers.R6)))
    print("R7: " + str(reg_read(Registers.R7)) + "\n")


class Traps:
    GETC = 0x20  # get character from keyboard
    OUT = 0x21  # output a character
    PUTS = 0x22  # output a word string
    IN = 0x23  # input a string
    PUTSP = 0x24  # output a byte string
    HALT = 0x25  # halt the program
    CHAT_POST = 0x30
    GET_PLAYER_TILE = 0x31
    SET_PLAYER_TILE = 0x32
    GET_BLOCK = 0x33
    SET_BLOCK = 0x34
    GET_HEIGHT = 0x35
    PRINT_REGISTERS = 0x36


_traps = {
    Traps.GETC: _GETC,
    Traps.OUT: _OUT,
    Traps.PUTS: _PUTS,
    Traps.IN: _IN,
    Traps.PUTSP: _PUTSP,
    Traps.HALT: _HALT,
    Traps.CHAT_POST: _CHAT_POST,
    Traps.GET_BLOCK: _GET_BLOCK,
    Traps.SET_BLOCK: _SET_BLOCK,
    Traps.GET_HEIGHT: _GET_HEIGHT,
    Traps.GET_PLAYER_TILE: _GET_PLAYER_TILE,
    Traps.SET_PLAYER_TILE: _SET_PLAYER_TILE,
    Traps.PRINT_REGISTERS: _PRINT_REGISTERS,
}


def trap_routine(code):
    return _traps[code]
