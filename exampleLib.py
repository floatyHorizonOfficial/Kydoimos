import sys

def LibReader(opcode, args:str):
  _args = [args[i:i+2] for i in range(2, len(args), 2)]
  match opcode:
    case "05":
      print("Lib worked!")
      return 0
    
if sys.argv[1] == "0F":
  try:
    LibReader(sys.argv[2][0:2], sys.argv[2])
  except IndexError:
    print("Set \"Argument Count\" to zero!")
    while True:
      input("[Press Any Key to Crash Program]")
      break
