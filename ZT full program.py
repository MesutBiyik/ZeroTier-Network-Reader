### Program has been designed to complete various ZeroTier Automations

import requests
import json
import jsonpath
import time


# Script to return all Zerotier networks and store as a Json file.
def get_all_zt_networks(auth_header):
    # URL
    URL = "https://my.zerotier.com/api/network"

    # Additional headers. Using API key from ZT website
    headers = auth_header
    # print(headers)

    # Send GET request to ZeroTier API
    response = requests.get(URL, headers=headers)
    # print(response.text)+

    # Adjust response structure to Json.
    responsejson = response.json()
    # print(responsejson)

    # return Json indented and sort keys
    return json.dumps(responsejson, indent=2, sort_keys=True)


def authorization(key):
    auth_key = key
    auth_bearer = 'bearer ' + key

    auth_header = {'Authorization': auth_bearer}

    # print(auth_header)

    return auth_header


# write data to Json file
def write_json(data):
    file1 = open(r"id.json", "w+")
    file1.write(data)
    file1.close()
    return


#Write ID and names
def network_id_to_text_names():
    with open('id.json') as f:
        json_file = json.load(f)
        # print(json_file)

    # Count for for loop
    count = 0
    # Arrays for nework ids
    networkIDs = []


    #Clear text file if it exists
    try:
        file = open("networkids_with_names.txt", "r+")
        file.truncate(0)
    except IOError:
        #If file does not exist move alone
        print("File does not exist..Move along")
    finally:
        f.close()


    # For loop to add network ids into array

    for count in range(0, len(json_file)):
        # print (data[count]['id'])
        #networkIDs += json_file[count]['id']
        file1 = open(r"networkids_with_names.txt", "a+")
        # Write Zerotier Name & ID
        file1.write(json_file[count]['description']+'\n'+json_file[count]['id'] + '\n' )

        file1.close()

#Write ID's only
def network_id_to_text():
    with open('id.json') as f:
        json_file = json.load(f)
        # print(json_file)

    # Count for for loop
    count = 0
    # Arrays for nework ids
    networkIDs = []

    #Clear text file if it exists
    try:
        file = open("networkids.txt", "r+")
        file.truncate(0)
    except IOError:
        #If file does not exist move alone
        print("File does not exist..Move along")
    finally:
        f.close()



    # For loop to add network ids into array

    for count in range(0, len(json_file)):
        # print (data[count]['id'])
        networkIDs += json_file[count]['id']
        # Write only Zerotier network name

        file = open(r"networkids.txt", "a+")

        # Write Zerotier Name & ID
        # file1.write(data[count]['description']+'\n'+data[count]['id'] + '\n' )

        # Write only Zerotier network name
        file.write(json_file[count]['id'] + '\n')
        file.close()

#Read network ID's into array
def network_to_array():
    with open('networkids.txt', 'r') as f:
        network = f.read().splitlines()  # puts the file into an array
        f.close()
    # print(network)
    return network

#Read User ID's into array
def read_userids():
    # Open file in read mode
    with open('userids.txt', 'r') as userids:
        # Read lines
        lines = userids.readlines();
        # print(lines)

    # Create blank variable
    userids = []

    # For loop to read all data
    for l in lines:
        # Read data and split by line (\n)
        as_list = l.split("\n")
        # Add data to variable
        userids.append(as_list[0])

    # Print user ids
    # print(userids)
    # print(type(userids))
    return userids

#Remove User ID's from networks
def remove_users(data, data1,key):
    networksIDs = data
    userIDs = data1
    # print(userIDs)

    totalNetworks = len(networksIDs)
    totalUsers = len(userIDs)

    # URL
    URLmain = "https://my.zerotier.com/api/network/"

    URLlast = "member/"
    URLnetwork = ""

    count = 0
    count1 = 0
    # For loop after this to delete members
    for count in range(0, len(userIDs)):
        # print(networksIDs)
        URLuser = userIDs[count]
        # print(URLuser)
        count += 1
        print("User No:", count, " Total Users: ", totalUsers)

        for count1 in range(0, len(networksIDs)):
            URLnetwork = networksIDs[count1] + "/"
            # print(URLnetwork)
            URL = URLmain + URLnetwork + URLlast + URLuser
            # print(URL)
            print("Network No:", count1, " Total Networks: ", totalNetworks)
            count += 1

            # Additional headers.
            headers = key
            response = requests.delete(URL, headers=headers)
            print("Status code (200 means good):", response.status_code)
            time.sleep(0.1)


def print_menu():  ## Your menu design here
    print(30 * "-", "MENU", 30 * "-")
    print("1. Create ZT Network List (ID's only)")
    print("2. Create ZT Network List (With Names)")
    print("3. Remove Users from ZT networks")
    print("4. Exit")
    print(67 * "-")


loop = True

while loop:  ## While loop which will keep going until loop = False
    print_menu()  ## Displays menu
    choice = input("Enter your choice [1-5]:")

    if choice == "1":
        print("Menu 1 has been selected")
        print("Creating list of ZT network id's")
        key = authorization('ZEROTIER-API-KEY-HERE')

        networks = get_all_zt_networks(key)
        write_json(networks)
        network_id_to_text()
        print("Created Network ID's text file")

    elif choice == "2":
        print("Menu 2 has been selected")
        print("Menu 1 has been selected")
        print("Creating list of ZT network id's")
        key = authorization('ZEROTIER-API-KEY-HERE')

        networks = get_all_zt_networks(key)
        write_json(networks)
        network_id_to_text_names()
        print("Created Network ID's text file")

    elif choice == "3":
        print("Menu 3 has been selected")
        networks = network_to_array()
        userids = read_userids()
        key = authorization('ZEROTIER-API-KEY-HERE')
        remove_users(networks, userids,key)

    else:
        # Any integer inputs other than values 1-5 we print an error message
        print("Wrong option selection. Enter any key to try again..")


def main():
    print_menu()


if __name__ == "__main__":
    main()
