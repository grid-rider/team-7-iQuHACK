import csv

def interleave_csv(file_path1, file_path2, output_file_path):
    with open(file_path1, 'r', newline='') as file1, open(file_path2, 'r', newline='') as file2, open(output_file_path, 'w', newline='') as outfile:
        reader1 = csv.reader(file1)
        reader2 = csv.reader(file2)
        writer = csv.writer(outfile)

        # Assuming both files have headers and they are identical,
        # write the header into the output file and move the readers to the next line
        headers1 = next(reader1)
        headers2 = next(reader2)
        if headers1 == headers2:
            writer.writerow(headers1)  # Write header into the output file
        else:
            raise ValueError("CSV files have different headers")

        # Interleave rows from both files
        for row1, row2 in zip(reader1, reader2):
            writer.writerow(row1)
            writer.writerow(row2)

        # If file1 has more rows, append them
        for row1 in reader1:
            writer.writerow(row1)

        # If file2 has more rows, append them
        for row2 in reader2:
            writer.writerow(row2)

# Paths to the input CSV files and the output file
file_path1 = './data/MITQute (Responses) - Straight Female.csv'
file_path2 = './data/MITQute (Responses) - Straight Male.csv'
output_file_path = './data/Combined_Responses.csv'

# Call the function
interleave_csv(file_path1, file_path2, output_file_path)