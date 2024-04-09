import Utils
import sys

if __name__ != "__main__":
  print("Do not use as import!")
  quit()

"""
SPECS:
> 8.2kB RAM
> 256 Slots of Stack
REGISTERS:
A: Main Reg. for work
X,Y: Short Memory
"""
ram = [0,]*65536 # 8192 Bytes (8.2kB) of RAM
stack = [] # Cap at 256 items
version = "01"
flags = 0b00000  # Less, More, Zero, Negative, --Carry [DEPRECATED]--

a,x,y = 0,0,0

code = []
if len(sys.argv) > 1:
  for i in open(sys.argv[0], "rb").read(): code.append(hex(i)[2:].upper().rjust(2, "0"))
else:
  for i in open("program", "rb").read(): code.append(hex(i)[2:].upper().rjust(2, "0"))

codeStr = ""
for i in code: codeStr += i
print(f"Code Loaded: {codeStr}")

reader = 0

while True:
  if len(sys.argv) > 1:
    if "-PC" in sys.argv: print(reader)

  match code[reader]:
    case "00":
      print(f"Exit Code 00 ran at 0x{hex(reader)[2:].rjust(6, "0").upper()}")
      break
    
    case "05":
      bufLength = int(code[reader+1], 16)
      address = Utils.hexAddressToDec(code[reader+2] + code[reader+3])
      for i in range(0, bufLength):
        ram[address+i] = int(code[reader+4+i], 16)
      reader += 3+bufLength

    case "08":
      stack.append(a)
    case "09":
      stack.append(reader+1)
      reader += 1
    case "0A":
      stack.append(ram[
        Utils.hexAddressToDec(code[reader+0] + code[reader+1])
      ])
      reader += 2
    case "0B":
      a = stack.pop()

    case "11":
      a = int(code[reader+1], 16)
      reader += 1
    case "13":
      x = int(code[reader+1], 16)
      reader += 1
    case "14":
      y = int(code[reader+1], 16)
      reader += 1
    
    case "21":
      a = ram[Utils.hexAddressToDec(code[reader+1] + code[reader+2])]
      reader += 2
    case "23":
      x = ram[Utils.hexAddressToDec(code[reader+1] + code[reader+2])]
      reader += 2
    case "24":
      y = ram[Utils.hexAddressToDec(code[reader+1] + code[reader+2])]
      reader += 2
    
    case "41": a += 1
    case "42": x += 1
    case "43": y += 1
    
    case "44": a -= 1
    case "45": x -= 1
    case "46": a += x + (flags & 0b01)
    case "47": a += y + (flags & 0b01)
    case "48":
      a += int(code[reader+1], 16) + (flags & 0b01)
      reader += 1
    case "49":
      a += ram[Utils.hexAddressToDec(code[reader+1] + code[reader+2])] + (flags & 0b1)
      reader += 2
    
    case "4A":
      a = round(a/code[reader+1])
      reader += 1
    case "4B":
      a = round(a/ram[Utils.hexAddressToDec(code[reader+1] + code[reader+2])])
      reader += 2

    case "51":
      ram[Utils.hexAddressToDec(code[reader+1] + code[reader+2])] = a
      reader += 2
    case "52":
      ram[Utils.hexAddressToDec(code[reader+1] + code[reader+2])] = x
      reader += 2
    case "53":
      ram[Utils.hexAddressToDec(code[reader+1] + code[reader+2])] = y
      reader += 2
    
    case "55": y -= 1
    case "56": a -= x
    case "57": a -= y
    case "58":
      a -= int(code[reader+1], 16)
      reader += 1
    case "59":
      a -= ram[Utils.hexAddressToDec(code[reader+1] + code[reader+2])]
      reader += 2
    
    case "5A":
      a *= code[reader+1]
      reader += 1
    case "5B":
      a *= ram[Utils.hexAddressToDec(code[reader+1] + code[reader+2])]
      reader += 2
    
    case "60":
      flagsChange = Utils.compare(a, int(code[reader+1], 16))
      flags |= flagsChange
      reader += 1
    case "61":
      flagsChange = Utils.compare(a, x)
      flags |= flagsChange
      reader += 1
    
    case "63":
      if 0b100 == flags & 0b100:
        reader = Utils.hexAddressToDec(code[reader+1:reader+5])-1
      else: reader += 4
    case "64":
      if 0b10000 == flags & 0b10000:
        reader = Utils.hexAddressToDec(code[reader+1:reader+5])-1
      else: reader += 4
    
    case "66":
      a = round(a/x)
    case "67":
      a = round(a/y)

    case "68":
      a &= code[reader+1]
      reader += 1
    case "69":
      a &= Utils.hexAddressToDec(code[reader+1] + code[reader+2])
      reader += 2

    case "6A":
      a ^= code[reader+1]
      reader += 1
    case "6B":
      a ^= Utils.hexAddressToDec(code[reader+1] + code[reader+2])
      reader += 2

    case "70":
      flagsChange = Utils.compare(a, ram[
        Utils.hexAddressToDec(code[reader+1] + code[reader+2])
      ])
      flags |= flagsChange
      reader += 2
    case "71":
      flagsChange = Utils.compare(a, y)
      flags |= flagsChange
      reader += 1
    
    case "73":
      if 0b0 == flags & 0b100:
        reader = Utils.hexAddressToDec(code[reader+1:reader+5])-1
      else: reader += 4
    case "74":
      if 0b1000 == flags & 0b1000:
        reader = Utils.hexAddressToDec(code[reader+1:reader+5])-1
      else: reader += 4
    
    case "76":
      a *= x
    case "77":
      a *= y

    case "78":
      a |= code[reader+1]
      reader += 1
    case "79":
      a |= Utils.hexAddressToDec(code[reader+1] + code[reader+2])
      reader += 2
    
    case "7A":
      a = code[reader+1] >> 1
      reader += 1
    case "7B":
      a = Utils.hexAddressToDec(code[reader+1] + code[reader+2]) >> 1
      reader += 2
    case "7C":
      a = code[reader+1] << 1
      reader += 1
    case "7D":
      a = Utils.hexAddressToDec(code[reader+1] + code[reader+2]) << 1
      reader += 2

    case "C8":
      bufLength = int(code[reader+1], 16)
      address = Utils.hexAddressToDec(code[reader+2] + code[reader+3])
      buffer = ""
      for i in range(0, bufLength):
        buffer += chr(ram[address+i])
      reader += 3
      print(buffer)
    case "C9":
      address = Utils.hexAddressToDec(code[reader+1] + code[reader+2])
      reader += 2
      print(ram[address])
    
    case "CA":
      bufLength = int(code[reader+1], 16)
      address = Utils.hexAddressToDec(code[reader+2] + code[reader+3])
      buffer = input("$ ")[:bufLength]
      for i in range(0, bufLength):
        ram[address+i] = ord(buffer[i])
      reader += 3
    case "CB":
      address = Utils.hexAddressToDec(code[reader+1] + code[reader+2])
      try:
        ram[address] = int(input("# "))
      except ValueError:
        print(f"ERR: String given as input! Operation at 0x{hex(reader)[2:].rjust(6, "0").upper()}")
        quit()
      reader += 2

    case "D9":
      buffer = code[reader+1]
      print(buffer)
      reader += 1

    case "E0": print(f"X: 0x{hex(x)[2:].upper()}, Y: 0x{hex(y)[2:].upper()}, A: 0x{hex(a)[2:].upper()}\nFlags: 0b{bin(flags)[2:].rjust(2, "0")}")
    case "E1": x,y,a = 0,0,0
    case "E2": flags = 0b0

    case "F0":
      if 0b1 == flags & 0b1: flags -= 1
    case "F1":
      if 0b10 == flags & 0b10: flags -= 2
    case "F2":
      if 0b10000 == flags & 0b10000: flags -= 16
    case "F3":
      if 0b1000 == flags & 0b1000: flags -= 8
    case "F4":
      if 0b100 == flags & 0b100: flags -= 4
    
    case "FF":
      Utils.checkValidHeader(code[reader+1:6], version)
      reader += 4
    case _:
      print(f"Illegal Operation Code {code[reader]} used at 0x{hex(reader)[2:].rjust(6, "0").upper()}! Continuing....")

  reader += 1
  if reader >= len(code):
    print("OUT OF BOUNDS! Force quitting program (EOF Reached)")
    quit()
