#To identify the input whether it is integer, float , string or special character
num = input("Enter anything ")
try:
    val = int(num)
    print("Input is an integer number. Value =", val)
except ValueError:
    try:
        val = float(num)
        print("Input is a float number. Value =", val)
    except ValueError:
        if num.isalpha():
            print("Input is a string. Value =", num)
        else:
            print("Input is a special character. Value =", num)

    
    