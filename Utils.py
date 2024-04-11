def getValidReaders(appVersion) -> list[str]:
  if appVersion == "01": return ["01", "02"]
  else: return ["NaN"]

def checkValidHeader(header, supportedVersions):
  if header[0:3] == ["46","48","56"]:
    
    if header[3] in supportedVersions:
      print("Running Code...")
    
    else:
      print("ERR: Wrong Version!")
      print(f"App uses {header[3]}, meanwhile this reader is version {supportedVersions[0]}!")
      print(f"Valid readers are {getValidReaders(header[3])}")
      
      if getValidReaders(header[3])[0] == "NaN":
        print("File uses unknown reader! Try:\n  - A newer version\n  - Check if version in file is correct")
      
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
  if a - value == 0: return 0b10
  else:
    if   a > value: return 0b100
    elif a < value: return 0b1000
    else: return 0
