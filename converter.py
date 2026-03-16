def universal_converter():
    print("--- Universal Python Converter ---")
    print("1. Unit Conversion (Length: km to miles)")
    print("2. Data Type Casting (String to Integer)")
    print("3. Base Conversion (Decimal to Hexadecimal)")
    print("4. Temperature (Celsius to Fahrenheit)")
    
    choice = input("\nSelect what you want to convert (1-4): ")

    if choice == '1':
        # Unit Conversion
        km = float(input("Enter kilometers: "))
        miles = km * 0.621371
        print(f"Result: {km} km is {miles:.2f} miles")

    elif choice == '2':
        # Data Type Casting (Explicit Conversion)
        user_str = input("Enter a number as a string (e.g., '123'): ")
        try:
            num = int(user_str) # Using the int() function for casting
            print(f"Result: {num} is now an {type(num)}")
        except ValueError:
            print("Error: That input cannot be converted to an integer.")

    elif choice == '3':
        # Base Conversion
        dec_num = int(input("Enter a decimal (base-10) integer: "))
        hex_val = hex(dec_num) # Built-in function for hex conversion
        print(f"Result: {dec_num} in Hexadecimal is {hex_val}")

    elif choice == '4':
        # Temperature Conversion
        celsius = float(input("Enter temperature in Celsius: "))
        fahrenheit = (celsius * 9/5) + 32
        print(f"Result: {celsius}°C is {fahrenheit:.2f}°F")

    else:
        print("Invalid selection. Please try again.")

# Run the converter
if __name__ == "__main__":
    universal_converter()
