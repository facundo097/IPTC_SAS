import requests
import csv
import time

# URL to request
GAS_ID = "type-gas-id"
url = f"https://script.google.com/macros/s/{GAS_ID}/exec?action=readA1"
counter = 1
# CSV file to save data
csv_file = "response_times.csv"

def write_to_csv(counter, elapsed_time, response_text):
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        # Write header if file is empty
        if file.tell() == 0:
            writer.writerow(['counter', 't', 'msg'])
        writer.writerow([counter, elapsed_time, response_text])

# Infinite loop
while True:
    start_time = time.time()
    response = requests.get(url)
    elapsed_time = time.time() - start_time
    print(f"Number of requests: {counter}")
    print(f"Time taken: {elapsed_time:.6f} seconds")
    print("Response received:", response.text)
    print("------------------------------------------------------------------------------------------------------------------------------------------------")
    write_to_csv(counter, elapsed_time, response.text)
    counter += 1
    time.sleep(4)