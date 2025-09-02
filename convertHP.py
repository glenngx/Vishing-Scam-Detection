'''
This is used initially to count how many occurence there are of each phone number in the text file
and convert it into the new format
'''

def count_phone_numbers(filename):
    phone_dict = {}
    
    # Open and read the text file
    with open(filename, 'r') as file:
        for line in file:
            phone_number = line.strip()  # assuming each line contains a phone number
            
            # Check if phone number already exists in dictionary
            if phone_number in phone_dict:
                phone_dict[phone_number] += 1
            else:
                phone_dict[phone_number] = 1
    
    return phone_dict

def export_to_file(phone_dict, output_file):
    with open(output_file, 'w') as file:
        for phone_number, count in phone_dict.items():
            file.write(f"{phone_number},{count}\n")

# Example usage:
input_file = 'Datasets/SMSwithoutCC.txt'  # old file format
output_file = 'Datasets/HP_db.txt'  #new file format


phone_dict = count_phone_numbers(input_file)
export_to_file(phone_dict, output_file)