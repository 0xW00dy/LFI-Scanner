from items import payloads
  
def injection_usage():
    print("Invalid type for inject option.")
    print("Syntax:")
    print("lfiscan.py --url=url --inject [type] [resource]")
    print("You can use on of these option:")
    for key in payloads:
        print(f"{key} : {payloads[key]}")
    