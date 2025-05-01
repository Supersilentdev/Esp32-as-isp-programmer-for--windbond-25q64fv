import serial
import time
import os

# Set the COM port (replace 'COM5' with your actual port)
ser = serial.Serial('COM5', 115200, timeout=1)

# File to read from
filename = r"C:\Users\YourUser\Documents\firmware.bin"  # Change this to your .bin file path

# Function to show progress
def show_progress(current, total):
    percent = (current / total) * 100
    print(f"Progress: {current}/{total} bytes ({percent:.2f}%)")

# Function to check the chip ID
def check_chip_id():
    print("Checking chip ID...")
    ser.write(b'id\n')  # Send the command to get chip ID
    time.sleep(0.1)  # Wait for the chip to respond
    chip_id = ser.readline().decode().strip()
    
    # Handle incorrect responses and retry if needed
    if not chip_id:
        print("Error: Failed to read chip ID. Please check the connection and try again.")
        return None

    print(f"Connected to chip with ID: {chip_id}")
    return chip_id

# Check the chip ID before proceeding
chip_id = check_chip_id()
if not chip_id:
    exit(1)  # Exit if the chip ID cannot be read

# Sending write command to start the process
print("Sending write command...")
ser.write(b'write\n')

# Waiting for the BEGIN_WRITE message to start writing data
print("Waiting for chip to be ready for writing...")
timeout = 10  # Timeout in seconds
start_time = time.time()

while True:
    line = ser.readline().decode().strip()
    print(f"Received: {line}")  # Debugging the received response
    if line == "BEGIN_WRITE":
        print("Started writing data to chip...")
        break
    elif time.time() - start_time > timeout:
        print("Timeout waiting for chip to be ready.")
        break

# Open the .bin file to read
with open(filename, "rb") as infile:
    total_size = os.path.getsize(filename)  # Get the total file size
    read_size = 0  # Start with 0 bytes written

    # Ensure we read and write data in chunks
    while read_size < total_size:
        chunk = infile.read(1024)  # Read 1024 bytes per chunk
        if not chunk:
            break
        
        read_size += len(chunk)

        # Send the data chunk to the ESP32
        ser.write(chunk)
        
        # Show progress after each chunk is written
        show_progress(read_size, total_size)

# Close the serial connection and notify the user
print(f"✅ Write complete! {filename} has been successfully written to the chip.")
