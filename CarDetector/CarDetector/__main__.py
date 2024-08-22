from CarDetector.core.wrapper import Wrapper
import torch
def main():
    print(torch.cuda.is_available())
    print(torch.cuda.device_count())
    
    wrapper = Wrapper()
    wrapper.run()
    
if __name__ == "__main__":
    main()
    
    
