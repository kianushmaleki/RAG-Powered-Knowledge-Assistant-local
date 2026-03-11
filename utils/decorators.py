import functools
import time


def timer_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 1. Record the start time
        start_time = time.perf_counter()
        
        # 2. Execute the actual function
        result = func(*args, **kwargs)
        
        # 3. Record the end time
        end_time = time.perf_counter()
        
        # 4. Calculate and print the duration
        duration = end_time - start_time
        print('***' * 20)
        print(f">>> NOTE >>> Function '{func.__name__}' took {duration:.4f} seconds to run.")
        print('***' * 20)
        
        # 5. Return the original function's result
        return result
    
    return wrapper