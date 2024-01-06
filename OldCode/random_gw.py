import time
import random

def generate_values():
    current1 = round(random.uniform(2.20, 2.48), 2)
    current2 = round(random.uniform(1.08, 1.5), 2)
    return current1, current2

if __name__ == "__main__":
    while True:
        values = generate_values()
        print(values[0]) 
        print(values[1])  
        time.sleep(5)

