def checkValidHeader(header, version):
  if header[0:3] == ["46","48","56"]:
    if header[3] == version:
      print("Running Code...")
    else:
      print("ERR: Wrong Version!")
      print(f"App uses {header[3]}, meanwhile this reader is version {version}!")
      quit()
  else:
    print("App not made using FHV build!")
    quit()

def hexAddressToDec(address) -> int:
  addressInt = ""
  for i in address:
    addressInt += str(i)
  return int(addressInt, 16)

def compare(a, value) -> int:
  if a - value == 0: return 0b100
  else:
    if   a > value: return 0b1000
    elif a < value: return 0b10000
    else: return 0
