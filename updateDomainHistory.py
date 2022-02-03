import json
import datetime
import requests
import sys
import collections
from urllib.parse import urlparse
from browser_history.utils import default_browser

class DomainList:
  def __init__(self, name, freq, category):
    self.name = name
    self.freq = freq
    self.category = category

def browserhistory():
  BrowserClass = default_browser()
  if BrowserClass is None:
      # default browser could not be identified
      print("Could not get default browser!")
      return null
  else:
      b = BrowserClass()
      # his is a list of (datetime.datetime, url) tuples
      his = b.fetch_history().histories
      # getting list second element put into new list
      urlList = [item[1] for item in his]
      #set initial fetchlist to get only domain
      fetchlist = [] 
      for x in urlList:
        domain_name = urlparse(x).netloc
        fetchlist.append(DomainList(domain_name, 0, ""))
      return fetchlist

def uniqueList(list):
  seen = collections.OrderedDict()
  for obj in list:
    if obj.name not in seen:
      seen[obj.name] = obj
  testlist = seen.values()
  return testlist

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

def addDomain(domainlist, access_token):
  api_domains = "https://sadns.herokuapp.com/api/domains/"
  token = "Bearer " + str(access_token)
  # for x in domainlist:
  #   print(x.name , x.freq, x.category, sep=" ")
  print("\nStarting POST request UDH--------")
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

def readFile(filename, domainlist, category1, category2):
  for x in domainlist:
    file = open(filename, 'r')
    # with open(filename, 'r') as file:
    if x.category == "" or x.category == category2:
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

def calculateFreq(domainlist, historyList):
  for x in domainlist:
    for y in historyList:
      if x.name == y.name:
        x.freq = x.freq + 1
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


def main(access_token):
  """Get a list from browser history"""
  historyList = browserhistory() #return obj list
  """Make the list to be unique"""
  domainlist = uniqueList(historyList)
  """
  Compare the unique list with history list to get the freq of each domain list
  """
  domainlist = calculateFreq(domainlist, historyList)
  updatedDomainList = compareDomain(domainlist, access_token)
  addDomain(updatedDomainList, access_token)


if __name__ == "__main__":
  args = sys.argv
  access_token = args[1]
  main(access_token)
