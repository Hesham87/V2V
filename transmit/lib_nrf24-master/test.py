
from threading import *
def multiply(x,y):
    print(x * y)

if __name__ == "__main__":
   thread_mul =Thread(target=multiply, args= (1,2))
   thread_mul.start()
   thread_mul.join()