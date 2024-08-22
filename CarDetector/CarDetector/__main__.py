
from CarDetector.core.wrapper import Wrapper

def LogInfoMethod(func, *args, **kwargs):
    print(*args)
    print(*kwargs)
    
    r = func(*args, **kwargs)
    print(r)



def add(x,y,z) -> int:
    return x+y+z
def main():
    # wrapper = Wrapper()
    # wrapper.run()
    LogInfoMethod(add,10,20,30)
    
if __name__ == "__main__":
    main()
    
    
