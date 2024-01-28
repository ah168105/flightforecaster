import json
import re
import requests
import csv
import serial
import time


# Define the URL of the API

date = input("Enter the date of the desired flight Format YYYY-MM-DD: ")

values = date.split('-')
Year = str(date[0].strip() + date[1].strip() + date[2].strip() + date[3].strip())
Month = str(date[5].strip() + date[6].strip())
Day = str(date[8].strip() + date[9].strip())

Origin = str(input("\nEnter the Origin of the Flight (Airport Code): "))
print(Origin)

Destination = str(input("\nEnter the Destination of the Flight (Airport Code): "))

api_url = 'http://localhost:4000/flights?date='+Year+'-'+Month+'-'+Day+'&origin='+Origin+'&destination='+Destination

# Send a GET request to the API
response = requests.get(api_url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

    # Define the CSV file name
    csv_filename = "data2.csv"

    # Open the CSV file in write mode
    with open(csv_filename, mode='w', newline='') as csv_file:
        # Create a CSV writer object
        csv_writer = csv.writer(csv_file)

        # Write the header row
        csv_writer.writerow(data[0].keys())

        # Write each data row to the CSV file
        for row in data:
            csv_writer.writerow(row.values())

    print(f"Data successfully saved to {csv_filename}")
else:
    print("Failed to fetch data from the API")

def preprocess_line(line):
    # Replace single quotes with double quotes
    return line.replace("'", '"')

def read_csv_file(filename):
    data = []
    with open(filename, 'r') as csvfile:
        csvfile.readline()
        for line in csvfile:
            # print(line)
            # line = preprocess_line(line.strip())
            fields = re.split(r',(?!\s)', line)
            # print(fields)
            # print(type(fields[1]))
            asort = {
                "flight_num": int(fields[0]),
                "origin" : json.loads(fields[1]),
                "destination" : json.loads(fields[2]),
                "duration" : json.loads(fields[4]),
            }
            data.append(asort)
    return data

def print_flight_info_after(data, target_flight_num):
    found = False
    for flight in data:
        
        if found:
            break  # Stop printing after the next newline
        elif flight["flight_num"] == target_flight_num:
            found = True
            print(flight)  # Print the found flight

# Example usage:
filename = 'data2.csv'
data = read_csv_file(filename)

# Ask user for a flight number
target_flight_num = int(input("Enter the flight number to search for: "))

# Print flight info after the specified flight number
print_flight_info_after(data, target_flight_num)


flight_info = None
for flight in data:
    if flight["flight_num"] == target_flight_num:
        flight_info = flight
        break

if flight_info:
    # Convert flight_info to JSON string
    flight_json = json.dumps(flight_info)
    
    # Send flight data over serial
    ser = serial.Serial('COM4', 9600)
    ser.write(flight_json.encode())
    ser.close()
else:
    print("Flight not found")