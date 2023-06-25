# decorator_test.py

def my_decorator(func):
	print("Decorator function called.")
	
	def wrapper(*args, **kwargs):
		print("Wrapper function called.")
		return func(*args, **kwargs)
	
	return wrapper


@my_decorator
def my_function():
	print("Original function called.")

# print("Module imported.")
