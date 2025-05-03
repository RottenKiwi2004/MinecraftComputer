import mcschematic

def convertFromROMtoSchematic(ROM: list[int], asmFile):
    schem = mcschematic.MCSchematic()

    def write(address: int, data: int):
        width = 14
        offset = 5

        row = (address & 0b11000000) >> 6
        depth = address & 0b00011111
        direction = ((address & 0b00100000) >> 4) - 1
        nudge = address & 0b00000001

        x = -2 * depth
        z = width * row + direction * (offset - nudge) + offset

        for i in range(16):
            bit = data & 0b0000_0000_0000_0001
            schem.setBlock((x, i * 2, z), "minecraft:composter[level=1]" if bit == 1 else "minecraft:black_concrete")
            data >>= 1

    for i in range(len(ROM)):
        write(i, ROM[i])

    schem.save("D:\\MultiMC\\MultiMC\\instances\\1.20.1\\.minecraft\\schematics\\Assembly", "test", mcschematic.Version.JE_1_18_2)
