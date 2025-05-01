import serial
import time

# Set the COM port (replace 'COM5' with your actual port)
ser = serial.Serial('COM5', 115200)

# File to save the backup
outfile = open("winbond_backup.bin", "wb")

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
    print(f"Connected to chip with ID: {chip_id}")
    return chip_id

# Check the chip ID before proceeding
chip_id = check_chip_id()

# Sending dump command to start the process
print("Sending dump command...")
ser.write(b'dump\n')

# Waiting for the BEGIN_DUMP message to start reading data
print("Waiting for data...")
started = False
while True:
    line = ser.readline()
    if b'BEGIN_DUMP' in line:
        print("Started receiving data...")
        started = True
        break

# Read 8MB of data and save it to the file
total_size = 8388608  # 8MB
read_size = 0  # Start with 0 bytes read

while read_size < total_size:
    # Read data in chunks
    chunk = ser.read(1024)
    read_size += len(chunk)
    outfile.write(chunk)
    
    # Show progress
    show_progress(read_size, total_size)

# Close the output file
outfile.close()

print(f"✅ Backup complete! File saved as winbond_backup.bin")
