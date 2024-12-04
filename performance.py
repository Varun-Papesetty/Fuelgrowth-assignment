import csv

#Read the filenames from a CSV file
filenames = []
with open('duplicates.csv', 'r') as csvfile:
    csvreader = csv.DictReader(csvfile)
    for row in csvreader:
        filenames.append(row['duplicate'])  

#removing the ".png" extension
numbers = [float(name.replace(".png", "")) for name in filenames]

total_sum = sum(numbers)

average = total_sum / len(numbers)

# Output the results
print(f"Total Sum: {total_sum}")
print(f"Average: {average}")
