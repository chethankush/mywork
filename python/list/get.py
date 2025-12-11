def getting(something):
    while True:
        n = int(input("Enter a number (0 to stop): "))
        if n == 0:
            break
        getting.append(n)
    return something