with open('Readings/ORT/sun_slw26novS1.dat', 'rb') as input_file, open('Readings/ORT/sun_slw26novS1.txt', 'w') as output_file:
    # read binary data from input file
    binary_data = input_file.read()
    # convert binary data to string
    ascii_data = binary_data.decode('base64')
    # write string data to output file
    output_file.write(ascii_data)
