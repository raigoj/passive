# Passive OSINT Tool

This tool helps you find information using open-source investigative methods (OSINT).

## Features

- Search Full Name: Find address and phone number using a full name by querying the Belgium telephone directory.

- Search IP Address: Discover the internet service provider (ISP) and city associated with an IP address using the `geocoder` package.

- Search Social Networks: Check if a username exists on various social media platforms, including Facebook, Instagram, Steam, Reddit, and Twitch, by making HTTP requests and analyzing HTML content.

## OSINT

Open-Source Intelligence (OSINT) refers to intelligence produced by collecting, evaluating, and analyzing publicly available information to answer specific intelligence questions.

## How It Works

- The program's entry point is the `main` function. It checks the command-line arguments and executes the corresponding functionality based on the flag and input provided.

- If incorrect arguments are provided, the `cmd_help` function is displayed to guide the user.

- Using the flag `-fn` and a full name, the program calls the `search_full_name` function. This function fetches information by making an HTTP request to `whitepages.be` and uses regex to find the person's phone number and address.

- Using the flag `-ip` and an IP address, the program calls the `search_ip_address` function. This function uses the `geocoder` package to find the ISP and city associated with the provided IP address. If no information is found, it returns empty fields.

- Using the flag `-u` and a username, the program calls the `search_social_networks` function. This function makes HTTP requests to various social media sites and parses the HTML content to determine the existence of the username. The process is repeated multiple times if the username is not found initially, as it may not always provide 100% accurate results.

- After obtaining the results from the command-line input, the program prints the values and saves them into the `result.txt` file using the `save_results` function. Each time new results are obtained, the `next_filename` function is called to increase the txt file index, for example, `result1.txt`.

## Usage: How to Run
Since Ubuntu is by far the most popular distro all the commands provided are Ubuntu specific, if you don't have Ubuntu, Debian or related distros find your distro's equivalent

Ensure you have Python installed by running the following commands:

    sudo apt update
    sudo apt install python3

Navigate to the project folder and make the passive.py file executable:

    chmod +x passive.py

Determine the path to the passive tasks directory by running:

    pwd

Create a symbolic link with the following command (replace "YOUR PATH" with the path obtained in the previous step):

    sudo ln -s "YOUR PATH"/passive.py /usr/local/bin/passive

Install pip by running:

    sudo apt install python3-pip

Finally, install the geocoder package:

    pip install geocoder

## Examples:

To see available options:

    python3 passive.py --help

To search for a full name (e.g., "Jean Dupont"):

    python3 passive.py -fn "Jean Dupont"

To search for information based on an IP address (e.g., 157.240.11.9):

    python3 passive.py -ip 157.240.11.9

To search for a username on social media platforms (e.g., "@user01"):

    python3 passive.py -u "@user01"

To check your own IP, use the command:

    python3 passive.py -ip "me"

