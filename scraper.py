from bs4 import BeautifulSoup
from pprint import pprint
import sys
import csv
import time
import urllib.request

property_id = 7344
# property_id = sys.argv[0]
highest_id = 9050

def fetch_tds(url):    
    result = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(result, 'html.parser')
    table = soup.find('table', attrs = {'id': 'ctl00_Col2ContentPlaceholder_ucRentBoardUnitList_gvRentBoardUnitList'});
    table_data = table.find_all('td')
    return table_data 

def output(name, values):
    with open(name, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(values)

values = [['Unit Address', 'Unit Status', 'Tenancy Start', 'Rent Ceiling', 'Housing Services', 'Other']]
current = []
sleepCounter = 0
while (property_id <= highest_id):
    print(property_id)
    url = 'http://www.cityofberkeley.info/RentBoardUnitSearch.aspx?propertyId=' + str(property_id)
    try:
        table_data = fetch_tds(url)
    except AttributeError: 
        output('broken' + str(property_id) + '.csv', values)
    i = 0
    for data_tag in table_data:
        if (i == 0):
            if (data_tag['class'][0] == 'gridItemUnitFullAddress'):
                unit_address_one = data_tag.find('span', attrs = {'class': 'singleUnitMode'})
                unit_address_two = data_tag.findChildren()[0]
                if (unit_address_one): 
                    current.append(unit_address_one.get_text())
                elif (unit_address_two):
                    current.append(unit_address_two.get_text())
                else:
                    print("Check unit addressing at this id: " + str(property_id))
                    break
        else:
            # only one child
            child = data_tag.findChildren()
            current.append(child[0].get_text())
            if (i == 5):
                values.append(current)
                current = []
        i = (i + 1) % 6
    if (sleepCounter == 0):
        time.sleep(1)
    sleepCounter = (sleepCounter + 1) % 60
    property_id += 1

output('output.csv', values)


