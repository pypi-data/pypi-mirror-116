import requests
import json

response = requests.get("https://data.iana.org/TLD/tlds-alpha-by-domain.txt")

# remove lines that do not contain TLDs
tld_list = []
for line in response.content.split('\n'):
    if len(line.split()) == 1:
        tld_list.append(line.lower())
    else:
        print line

with open("swimbundle_utils/tld_list.json", 'w') as f:
    f.write(json.dumps(tld_list, indent=2))
