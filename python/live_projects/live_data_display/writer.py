import time
from datetime import datetime
import random

while True:
    with open("data.txt", "a") as f:
        f.write(f"{datetime.now()} CPU={random.randint(1,100)}%\n")
    time.sleep(5)
