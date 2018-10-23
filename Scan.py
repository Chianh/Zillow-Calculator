import zillow
import requests
import numpy as np
from bs4 import BeautifulSoup
import pandas as pd

def GetSearchResults(key,address,zip_code, result_list, rentzestimate):
    base_url = "https://www.zillow.com/webservice"
    request_url = base_url + '/GetSearchResults.htm?zws-id=' + str(key) + '&citystatezip=' + str(zip_code) + '&address=' + address + '&rentzestimate=true'
    user_request = requests.get(request_url)
    content = user_request.content
    soup = BeautifulSoup(content, 'lxml')
    f = open('organize_xml.xml', 'w')
    f.writelines(soup.prettify())
    f.close()
    good_flag = 1
    try:
        rent_group = soup.find('rentzestimate')
    except:
        good_flag = 0
    if good_flag:
        try:
            rent_query = rent_group.find('amount')
        except:
            rent = 0
            good_flag = 0
        if good_flag == 1:
            rent = (rent_query.get_text())
        else:
            rent = 0
    else:
        rent = str(0)
    market_price_group = soup.find('zestimate')
    market_price_query = market_price_group.find('amount')
    market_price = (market_price_query.get_text())
    return_percentage = float(rent)/float(market_price)*100
    new_list = [[address,round(return_percentage, 2)]]
    new_list = np.array(new_list)
    result_list = np.concatenate((result_list, new_list),axis = 0)
    return result_list



def main():
    key = '_______'
    file_name = input('Enter Zip Code: ')
    file_name = file_name + '.csv'
    csv = pd.read_csv(file_name).as_matrix()
    start = 0
    result_list = [['Address' , 'Return Percentage']]
    result_list = np.array(result_list)
    for start in range(len(csv)):
        address = str(csv[start][0]) + " " + str(csv[start][1])
        zip_code = str(csv[start][2])
        result_list = GetSearchResults(key,address,zip_code,result_list,rentzestimate=True)
    result_filename = str(zip_code) + '_Results.csv'
    print(result_list)
    result = pd.DataFrame(result_list)
    result.to_csv(result_filename,index = False,header = False)

        

main()