import csv
import os

# Function to add "Source" column to CSV files
def add_source_column_to_csv(directory):
    # Iterate over each CSV file in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            filepath = os.path.join(directory, filename)
            
            # Create a temporary file to write the modified CSV data
            temp_filepath = filepath + '.tmp'
            with open(filepath, mode='r', newline='', encoding='utf-8') as csv_file:
                reader = csv.reader(csv_file)
                
                # Read the header row
                header = next(reader)
                
                # Add "Source" to the header
                header.append("Source")
                
                # Write the data with the modified header to the temporary file
                with open(temp_filepath, mode='w', newline='', encoding='utf-8') as temp_file:
                    writer = csv.writer(temp_file)
                    writer.writerow(header)
                    
                    # Write the remaining rows with "point2homes" as the source
                    for row in reader:
                        row.append("point2homes")
                        writer.writerow(row)
            
            # Replace the original file with the temporary file
            os.replace(temp_filepath, filepath)

# Example usage
directory = "./data"  # Directory containing your CSV files
add_source_column_to_csv(directory)
print("finished")
