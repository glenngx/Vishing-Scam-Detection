'''
Function to search if a country code is a scam

1. Store the known scam country codes in an array
2. check if the array is sorted, if not sorted, perform merge sort
3. User input country code
4. Binary search on the array to see if the country code is known scam 

source of country code: https://www.aura.com/learn/scammer-phone-numbers

mergesort to arrange the country code in sorted arrangement so that we can perform binary search properly
'''

'''
Take the user's phone number input and do a check against our database to see if it exists

methodology: store the value and number of occurence in a hashmap
search the hashmap, return whether found or not.
'''

import streamlit as st
from riskValue import risk_manager


#read the file with countrycodes into an array
def read_scam_cc_file(file_path):
    arr = []
    with open(file_path, 'r') as file:
        for line in file:
            stripped_line = line.strip()
            cleaned_line = stripped_line.lstrip('+').strip()
            try:
                integer = int(cleaned_line)
                if integer not in arr:
                    arr.append(integer)
            except ValueError:
                print(f"Skipping invalid integer: {stripped_line}")
    return arr

#check if the array is sorted
def checkifsorted(arr):
    for i in range(len(arr) - 1):
        if arr[i] > arr[i + 1]:
            return False
    return True

#if the array is not sort, do merge sort
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    
    # Divide the array into two halves
    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]

    # Recursively sort both halves
    left_sorted = merge_sort(left_half)
    right_sorted = merge_sort(right_half)

    # Merge the sorted halves
    return merge(left_sorted, right_sorted)

#continue with merge function
def merge(left, right):
    sorted_array = []
    left_index = 0
    right_index = 0

    # Merge the two halves together while maintaining sorted order
    while left_index < len(left) and right_index < len(right):
        if left[left_index] < right[right_index]:
            sorted_array.append(left[left_index])
            left_index += 1
        else:
            sorted_array.append(right[right_index])
            right_index += 1

    # If there are remaining elements in the left half, add them to the sorted array
    sorted_array.extend(left[left_index:])
    # If there are remaining elements in the right half, add them to the sorted array
    sorted_array.extend(right[right_index:])

    return sorted_array


#save the array back into the text file
def saveSCC(file_path,arr):
    with open(file_path, 'w') as file:
        for num in arr:
            file.write(f"{num}\n")

#binary search on the text file based on the user's input to check whether the country code has been identified as a common scam 
def binarysearchSCC(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return True
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
            
    return False

#main function to call all the different functions to enable the searching of country code function
def searchCCmain(input):
    ScamCCFile = 'Datasets/ScamCountryCode.txt' #read country codes that are identified as common scam into an array
    scamCountryCodes = read_scam_cc_file(ScamCCFile) #return an array with the scam country country codes

    #check if the array is sorted, if not sorted, perform merge sort.
    if checkifsorted(scamCountryCodes):
        sorted_SCC = scamCountryCodes
    else:
        sorted_SCC = merge_sort(scamCountryCodes)
    
    saveSCC(ScamCCFile,sorted_SCC) #save the sorted array into the text file to remove duplicates and other misc problems

    #perform binary search on the sorted list
    if binarysearchSCC(sorted_SCC,input):
        return True
    else:
        return False

 #read the list of phone numbers and the number of times they have been reported into a dictionary   
def read_phone_counts(filename):
    phone_dict = {}
    
    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    phone_number, count = line.split(',')
                    phone_dict[phone_number] = int(count)
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    
    return phone_dict

#search the dictionary and return the number of times the phone number input has beeen reproted
def search_phone_number(phone_dict, search_number):
    reported_times = phone_dict.get(search_number, 0)  # Default to 0 if not found
    return reported_times


#main function consisting of all the functions to enable searching if the phone number has been reported and return the number of times it has been reported
def searchHPmain(input_number):
    filename = 'Datasets/HP_db.txt'
    HP_hashmap = read_phone_counts(filename)
    return search_phone_number(HP_hashmap, input_number) 

#After a phone number has been identified as a scam, add the phone number into our text file database
def update_database(phone_number):
    filename = 'Datasets/HP_db.txt'
    updated = False

    # Read the current database
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Check if the number exists and update its count
    for i, line in enumerate(lines):
        existing_number, count = line.strip().split(',')
        if existing_number == phone_number:
            count = int(count) + 1
            lines[i] = f"{phone_number},{count}\n"
            updated = True
            break

    # If the number doesn't exist, add it with a count of 1
    if not updated:
        lines.append(f"{phone_number},1\n")

    # Write the updated database back to the file
    with open(filename, 'w') as file:
        file.writelines(lines)

    return updated

#Streamlit/ frontend functions to enable the reporting of phone numbers function
def report_phone_number():
    if 'last_checked_number' in st.session_state:
        reported_number = st.session_state.last_checked_number
        total_risk = risk_manager.get_total_risk()

        if total_risk > 50:
            updated = update_database(reported_number)
            st.session_state.phone_number_reported = True
            st.session_state.report_message = (
                f"Phone number {reported_number} was already in the database. Its count has been increased."
                if updated else
                f"Phone number {reported_number} has been added to the database."
            )
            return True
        else:
            st.warning(
                "This phone number may not be a scam based on the current risk assessment. It cannot be added to the database.")
            return False
    else:
        st.warning("No phone number to report. Please check a phone number first.")
        return False


#main function to enable streamlit/frontend by calling the 2 main functions to check for country code and phone number 
def phonenumberChecker():
    st.subheader('Check a Phone Number')
    country_code = st.text_input('Enter country code (optional)')
    phone_number = st.text_input('Enter phone number')

    if st.button('Search Phone Number'):
        # Reset the phone number risk before processing new submission
        risk_manager.reset_risk('phone_number')

        if not phone_number:
            st.error('Please enter a phone number.')
        else:
            # Save the entered phone number in the session state
            st.session_state.last_checked_number = phone_number
            total_risk = 0

            if country_code:
                try:
                    # Convert country_code to integer
                    country_code_int = int(country_code)
                    
                    # Check if the country code is valid and associated with scams
                    if searchCCmain(country_code_int):
                        total_risk += 5
                        if country_code.startswith('+'):
                            st.success(f'The country code {country_code} is commonly associated with vishing scams')
                        else:
                            st.success(f'The country code +{country_code} is commonly associated with vishing scams')
                    else:
                        st.warning('This country code has not been identified as a origin for vishing scams')
                except ValueError:
                    st.error('Please enter only numbers for the country code.')

            try:
                phone_number = phone_number.strip()  # Keep the number as a string
                HPrisk = searchHPmain(phone_number)
                if HPrisk > 0 and HPrisk < 10: 
                    total_risk += 5
                    st.success(f'The phone number {phone_number} has been reported {HPrisk} times.')
                elif HPrisk >= 10 and HPrisk < 50: 
                    total_risk += 7.5
                    st.success(f'The phone number {phone_number} has been reported {HPrisk} times.')
                elif HPrisk >= 50: 
                    total_risk += 10
                    st.success(f'The phone number {phone_number} has been reported {HPrisk} times.')
                else:
                    st.warning(f'The phone number {phone_number} has not been reported as vishing')
            except ValueError:
                st.error('Please enter a valid phone number.')

            # Update the phone number risk with the total calculated risk
            risk_manager.update_risk(total_risk, source='phone_number')
