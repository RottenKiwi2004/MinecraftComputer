import sys
from makeSchem import convertFromROMtoSchematic

# Remove arg for program name
args = sys.argv[1:]

asmFile = args[0] if len(args) >= 1 else "test.asm"

symbolTableCounter = 0
symbolTable = dict()
# First pass (generate address symbol table)
try:
    with open(asmFile) as file:
        lines = file.read()
        lines = lines.split('\n')
        for line in lines:
            if line.strip() == '':          # Skip blank lines
                continue

            line = line.split(';')[0]  # Remove comment from asm line
            line = line.strip()  # Remove excess spaces
            line = line.lower()  # Ignore case
            label = line.split(':')  # Split instruction by space
            if len(label) > 1:
                label = label[0]
                symbolTable[label] = symbolTableCounter
            symbolTableCounter += 1

except FileNotFoundError:
    print(f"No file named {asmFile}")

print("First pass: ")
print(f"Address symbol table: {symbolTable}")

# Utility functions
def parseNum(word: str) -> int:
    try:
        if word.startswith('0b'): return int(word[2:], 2)
        if word.startswith('0x'): return int(word[2:], 16)
        return int(word, 10)
    except:
        lookup = symbolTable[word]
        if lookup is None:
            raise ValueError("Unknown label")
        return lookup

def getRegisterNum(r: str) -> int:
    return int(r[1:])

def setRd(r: str) -> int:
    return getRegisterNum(r) << 9

def setRa(r: str) -> int:
    return getRegisterNum(r) << 3

def setRb(r: str) -> int:
    return getRegisterNum(r)


ROMdata = [0 for i in range(256)]
instructionCounter = 0
lineCounter = 0

# Second pass
try:
    with open(asmFile) as file:
        lines = file.read()
        lines = lines.split('\n')
        for line in lines:

            lineCounter += 1
            line = line.split(';')[0]       # Remove comment from asm line

            if line.strip() == '':          # Skip blank lines
                continue

            line = line.split(':')[-1]      # Remove label
            line = line.strip()             # Remove excess spaces
            line = line.lower()             # Ignore case
            instruction = line.split(' ')   # Split instruction by space
            # print(instruction)

            binary = 0x0000

            opcode = instruction[0]

            match opcode:
                case 'nop': binary |= 0x0000
                case 'hlt': binary |= 0x1000
                case 'ldi': binary |= 0x2000 | setRd(instruction[1]) | parseNum(instruction[2])
                case 'ldm': binary |= 0x3000 | setRd(instruction[1]) | setRb('r7')
                case 'stm': binary |= 0x4000 | setRa(instruction[1]) | setRb('r7')
                case 'jmp': binary |= 0x5000 | parseNum(instruction[1])
                case 'bin': binary |= 0x6000 | parseNum(instruction[1])
                case 'biz': binary |= 0x7000 | parseNum(instruction[1])
                case 'add': binary |= 0x8000 | setRd(instruction[1]) | setRa(instruction[2]) | setRb(instruction[3])
                case 'sub': binary |= 0x9000 | setRd(instruction[1]) | setRa(instruction[2]) | setRb(instruction[3])
                case 'or' : binary |= 0xa000 | setRd(instruction[1]) | setRa(instruction[2]) | setRb(instruction[3])
                case 'and': binary |= 0xb000 | setRd(instruction[1]) | setRa(instruction[2]) | setRb(instruction[3])
                case 'xor': binary |= 0xc000 | setRd(instruction[1]) | setRa(instruction[2]) | setRb(instruction[3])
                case 'inc': binary |= 0xd000 | setRd(instruction[1]) | setRa(instruction[2]) | setRb('r0')
                case 'dec': binary |= 0xe000 | setRd(instruction[1]) | setRa(instruction[2]) | setRb('r0')
                case 'shr': binary |= 0xf000 | setRd(instruction[1]) | setRa(instruction[2]) | setRb('r0')
                case _:
                    raise ValueError("Invalid instruction")

            ROMdata[instructionCounter] = binary
            instructionCounter += 1

            # binstr = bin(binary)[2:]
            # print('0'*(16 - len(binstr))+binstr)

except FileNotFoundError:
    print(f"\033[31mNo file named {asmFile}\033[0m")
    exit()

except IndexError:
    print(f"\033[31mSyntax error at line {lineCounter}\033[0m")
    exit()

except ValueError as e:
    print(f"\033[31m{e} at line {lineCounter}\033[0m")
    exit()


convertFromROMtoSchematic(ROMdata, asmFile.replace(".asm", ""))
outFileName = asmFile.replace(".asm", ".machine")
st = ''
for i in range(len(ROMdata)):
    binstr = bin(ROMdata[i])[2:]
    st += '0'*(16 - len(binstr)) + binstr + '\n'

with open(outFileName, "w") as outFile:
    outFile.write(st)

print(f"\033[32mSuccessfully assembled {asmFile}\033[0m")
