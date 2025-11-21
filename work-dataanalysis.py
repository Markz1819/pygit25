# Data Analysis
# Author: Mark Zhang

# Analyse the data provided in class


file_name = "NYC_Central_Park_weather_1869-2022.csv"


def combined_tasks():
    count = 0  # total count of data points
    total_rainfall = 0  # total rainfall
    total_min_temperature = 0  # total minimum temperature
    count_june = 0  # total count of data points in June
    total_max_temperature_in_june = 0  # total maximum temperature in June

    file = open(file_name)

    for line in file:  # loop through each line in the file
        if line.startswith("DATE"):
            continue

        count += 1  # increment count for each data point
        total_rainfall += float(line.split(",")[1])  # add the PRCP to the total
        try:
            total_min_temperature += float(
                line.split(",")[4]
            )  # add the TMIN to the total
        except ValueError:
            continue

        date = line.split(",")[0]
        month = float(date.split("-")[1])

        if month == 6:
            count_june += 1  # increment count for each data point in June
            total_max_temperature_in_june += float(
                line.split(",")[5]
            )  # add the TMAX to the total

    print("Total data points:", count)

    average_rainfall = total_rainfall / count
    print("Average rainfall:", average_rainfall)

    average_min_temperature = total_min_temperature / count
    print("Average minimum temperature:", average_min_temperature)

    average_max_temperature_in_june = total_max_temperature_in_june / count_june
    print("Average maximum temperature (in June):", average_max_temperature_in_june)

    file.close()


def main():
    combined_tasks()


if __name__ == "__main__":
    main()
