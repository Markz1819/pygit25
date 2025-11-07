# (String) Methods
# Author: Ubial
# 6 October 2025

# Ask the user what the weather is like
weather = input("What's the weather like today? ")

if weather.lower().strip("!.?, ") == "rainy":
    # Rainy, RAINY, RAiny
    # Rainy!
    # Rainy.
    print("You should bring an umbrella.")
else:
    print("I see...")

# Ask the customer if they want fries
fries_reply = input("Do you want fries?")

# "Yes!"
if "yes" in fries_reply.lower():
    print("Here are your fries.")
else:
    print("OK. You will not have fries.")
