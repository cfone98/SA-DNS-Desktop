import csv
import sys
import requests
import json

class DomainList:
  def __init__(self, name, freq, category):
    self.name = name
    self.freq = freq
    self.category = category

def getDomainFromCSV(csv_user):
    file = open(csv_user)
    csvreader = csv.reader(file)
    header = next(csvreader)
    rows = []
    for row in csvreader:
        rows.append(row)
    file.close()
    new_rows = list(filter(None, rows))
    fetchlist = []
    for x in new_rows:
      name = x[0]
      freq = int(x[3])
      domain_name = name[:-1]
      fetchlist.append(DomainList(domain_name, freq, ""))
    return fetchlist

def compareDomain(domainlist, access_token):
    category = getCategory(access_token)
    socialmed, adult, gambling, malware, others = '', '', '', '', ''
    for cat in category:
        if cat['name'] == "Social Media":
            socialmed = cat['id']
        elif cat['name'] == "Adult":
            adult = cat['id']
        elif cat['name'] == "Gambling":
            gambling = cat['id']
        elif cat['name'] == "Malware":
            malware = cat['id']
        elif cat['name'] == "Others":
            others = cat['id']
    """
    Compare the domain list 1 by 1 starting from
    1. Social Media
    2. Adult
    3. Gambling
    4. Security
    5. Others
    """
    domainlist1 = readFile("socialmedia.txt", domainlist, socialmed, others)
    domainlist2 = readFile("porn.txt", domainlist1, adult, others)
    domainlist3 = readFile("gambling.txt", domainlist2, gambling, others)
    domainlist4 = readFile("malware.txt", domainlist3, malware, others)
    return domainlist4

def readFile(filename, domainlist, category1, category2):
  for x in domainlist:
    file = open(filename, 'r')
    # with open(filename, 'r') as file:
    if x.category == "" or x.category == category2:
        """Option 1 - compare last string domain.com only"""
        # splitstring = x.name.split('.')
        # lastindex = len(splitstring) - 1
        # second_lastindex = lastindex - 1
        # # mod_string - Modified domain name string
        # mod_string = splitstring[second_lastindex] + "." + splitstring[lastindex]
        # if (mod_string in file.read()):
        #     # print("Found " + x.name + " in "+ filename +" file")
        #     x.category = category1
        #     file.close()
        """Option 2 - compare whole string domain.com"""
        if (x.name in file.read()):
            # print("Found " + x.name + " in "+ filename +" file")
            x.category = category1
            file.close()
        else:
            # print("Not Found " + x.name + " in "+ filename +" file")
            x.category = category2
            file.close()
    file.close()
  return domainlist

def getCategory(access_token):
  api_url = "https://sadns.herokuapp.com/api/category/"
  token = "Bearer " + str(access_token)
  headers = {
    "Authorization": token
  }
  response2 = requests.get(url = api_url, headers = headers)
  data = response2.json()
  return data

def addDomain(domainlist, access_token):
  api_domains = "https://sadns.herokuapp.com/api/domains/"
  token = "Bearer " + str(access_token)
  # for x in domainlist:
  #   print(x.name , x.freq, x.category, sep=" ")
  print("\nStarting POST request UDL --------")
  for x in domainlist:
    try:
        headers = {
        "Authorization": token
        }
        data = {
        "domain" : x.name,
        "freq" : x.freq,
        "cat_id" : x.category
        }
        response = requests.post(url=api_domains, headers=headers, data=data)
    except AttributeError as error:
        print(error)
  print("\nPOST request COMPLETED!! --------")


def main(csv_user, access_token):
  domainlist = getDomainFromCSV(csv_user)
  updatedDomainList = compareDomain(domainlist, access_token)
  addDomain(updatedDomainList, access_token)


if __name__ == "__main__":
  args = sys.argv
  csv_user = args[1]
  access_token = args[2]
  # print(access_token)
  main(csv_user, access_token)