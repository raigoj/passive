import os
import sys
import requests
import re
import geocoder

def search_full_name(full_name):
    result = {
        "First name": full_name.split(" ")[0],
        "Last name": full_name.split(" ")[1],
        "Address": None,
        "Number": None,
    }
    first_name, last_name = full_name.split()

    url = f"https://www.whitepages.be/Search/Person/?what={first_name}+{last_name}&where="
    response = requests.get(url)
    html_content = response.content.decode("utf-8")
    match_address = re.search(r'class="wg-address">\s+([^<\r\n]+)', html_content)
    match_number = re.search(r"phone\D*(\+\d+)", html_content)

    if match_address:
        result["Address"] = match_address.group(1)
    if match_number:
        result["Number"] = match_number.group(1)
    return result

def search_ip_address(ip_address):
    location = geocoder.ip(ip_address)
    city = location.city if hasattr(location, "city") else "cannot find"
    isp = location.org if hasattr(location, "org") else "cannot find"
    latitude = location.latlng[0] if hasattr(location, "latlng") else "-"
    longitude = location.latlng[1] if hasattr(location, "latlng") else "-"
    return {"ISP": isp, "City": city, "Latitude": latitude, "Longitude": longitude}

def search_social_networks(username):
    user = username.split("@")[1]

    social_networks = {
        "Facebook": (f"https://www.facebook.com/{user}", 5),
        "Instagram": (f"https://www.instagram.com/{user}", 5),
        "Steam": (f"https://steamcommunity.com/id/{user}", 5),
        "Reddit": (f"https://www.reddit.com/user/{user}", 15),
        "Twitch": (f"https://www.twitch.tv/{user}", 15),
    }

    found_networks = {}

    for network, (url, attempts) in social_networks.items():
        response = requests.get(url)
        html_content = response.content.decode("utf-8")
        if any(keyword in html_content for keyword in ["userVanity", "username=", "personaname", "profileId", "channel="]):
            found_networks[network] = "yes"
        else:
            found_networks[network] = "no"
    return found_networks

def next_filename(filename):
    filename, extension = os.path.splitext(filename)
    index = 1
    while os.path.exists(f"{filename}{index}{extension}"):
        index += 1
    return f"{filename}{index}{extension}"

def save_results(results, filename):
    if not os.path.exists(filename):
        with open(filename, "w") as file:
            for key, value in results.items():
                file.write(f"{key}: {value}\n")
            file.write("\n")
    else:
        new_filename = next_filename(filename)
        with open(new_filename, "w") as file:
            for key, value in results.items():
                file.write(f"{key}: {value}\n")
            file.write("\n")
        return new_filename

def cmd_help():
    print("Welcome to passive v1.0.0\n")
    print("OPTIONS:")
    print("    -fn         Search with full-name")
    print("    -ip         Search with ip address")
    print("    -u          Search with username")

def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--help" or len(sys.argv) != 3:
        cmd_help()
        return

    flag = sys.argv[1]
    search_input = sys.argv[2]

    if flag == "-fn":
        results = search_full_name(search_input)

        print(f"First name: {results['First name']}")
        print(f"Last name: {results['Last name']}")
        print(f"Address: {results['Address']}")
        print(f"Number: {results['Number']}")

        filename = save_results(results, "result.txt")
        print(f"Saved in {filename if filename else 'result.txt'}")
    elif flag == "-ip":
        results = search_ip_address(search_input)

        print(f"ISP: {results['ISP']}")
        print(f"City: {results['City']}")
        print(f"Lat/Lon: {results['Latitude']} / {results['Longitude']}")

        filename = save_results(results, "result.txt")
        print(f"Saved in {filename if filename else 'result.txt'}")
    elif flag == "-u":
        results = search_social_networks(search_input)

        for network, status in results.items():
            print(f"{network}: {status}")

        filename = save_results(results, "result.txt")
        print(f"Saved in {filename if filename else 'result.txt'}")
    else:
        cmd_help()
        return

if __name__ == "__main__":
    main()
