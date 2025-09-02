import checkphoneNumber
import time


def readphoneFile(filename):
    phone_numbers = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line:  # Ensure the line is not empty
                phone_numbers.append(line)
    return phone_numbers


def main():
    test_country = checkphoneNumber.read_scam_cc_file("testDatasets/testcountry.txt")
    test_phone = readphoneFile("testDatasets/testphone.txt")
    print(f"array of country code tested{test_country}")
    print(f"array of phone numbers tested{test_phone}")


    #test country code, 5 are correct in the database, 5 are not in the database
    inCC = 0
    notinCC = 0
    start_timeCC = time.time()
    for i in test_country:
        if checkphoneNumber.searchCCmain(i):
            inCC += 1
        else:
            notinCC +=1 
    end_timeCC = time.time()

    #test phone number, 100 are in the database, 100 are not in the database
    inDB = 0
    notinDB = 0
    start_timeHP = time.time()
    for phone in test_phone:

        current = checkphoneNumber.searchHPmain(phone)
        print(f"Checking phone number:{phone} Found with {current} occurence")
        if current > 0:
            inDB += 1
        else:
            notinDB += 1
    end_timeHP = time.time()


    print(f"Time taken to search 10 country codes: {end_timeCC - start_timeCC} seconds")
    print(f"Country Codes found In DB: {inCC}")
    print(f"Country Codes not found DB: {notinCC}")

    print(f"Time taken to search 100 phone numbers: {end_timeHP - start_timeHP} seconds")
    print(f"Phone Numbers found In DB: {inDB}")
    print(f"Phone Numbers Not in DB: {notinDB}")


if __name__ == "__main__":
    main()
