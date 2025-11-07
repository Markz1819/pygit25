# In your `work-functions.py` file, create a function that calculates the average of three numbers. Here are the requirements in detail:
#
# * call it `average`
# * it should accept three parameters: `num_one`, `num_two`, and `num_three`
# * it should calculate the average value of the three numbers:
# 	* recall that to calculate the average, you add the values then divide by the number of values you have
# * return the result
#


def average(num_one: float, num_two: float, num_three: float) -> float:
    return (num_one + num_two + num_three) / 3


print(average(94, 94, 91))


#  *Optional*: write another version that accepts a list and returns the average of all things inside the list
