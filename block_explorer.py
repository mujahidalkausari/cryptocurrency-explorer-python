#!/usr/bin/env python
import sys
import platform
import time
from datetime import datetime
import urllib.request as urllib2
from urllib.error import HTTPError
from urllib.error import URLError
import json
import csv
import sys
import os

try:
    
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}

    # ---------------hold Output Dictionaries {}---------------
    dict_list = []
    # -----Add addresses to lists for all addresses-----
    subscan_dic = []
    blockscout_dic = []
    # ------------API KEY----------------
    cryptoid_key = '45510f721dc1'
    # --------------------------------------

    #COPY API LINK FROM CSV FILE & ADDING TO api_link
    print('Input Ticker & Address...\n')

    #open a file for writing 
    with open('./parameters/addresses.csv', newline='') as inputfile:
        file_reader = csv.reader(inputfile)

        #Check and Remove existing file first then populate updated records
        if open('./api reports/balance.csv', 'a', newline=''):
            os.remove('./api reports/balance.csv')  

        pointer=0
        dateToday=datetime.today().strftime('%Y-%m-%d')
        
        for address_line in file_reader:

            ticker = address_line[0].strip(" ")
            address = address_line[1].strip(" ")

            if pointer == 0:
                
                pointer += 1
                print(ticker+" : "+address+"\n")

            elif pointer >= 1 and ticker =="FTC" or ticker =="DASH" or ticker == "DGB":

                pointer+=1
                print(ticker+" : "+address)   

                url_cryptoid = f"https://chainz.cryptoid.info/{ticker.lower()}/api.dws?q=getbalance&a=" + str(address)

                api_request = urllib2.Request(url_cryptoid, headers=hdr)
                api_reply = urllib2.urlopen(api_request).read()
                api_json=json.loads(api_reply)
                
        
                cryptoid_dic = {"balance": api_json, "assets_symbol": ticker, "address": address,"date": dateToday}
                dict_list.append(cryptoid_dic)

            elif pointer >= 1 and ticker =="NEO":

                pointer+=1

                url_neoscan = f"https://api.neoscan.io/api/main_net/v1/get_balance/" + str(address)
                api_request = urllib2.Request(url_neoscan, headers=hdr)
                api_reply = urllib2.urlopen(api_request).read()
                api_json=json.loads(api_reply)
                api_data=api_json['balance']

                for dict_item in api_data:
                    
                    neoscan_dic = {"balance": dict_item['amount'], "assets_symbol": dict_item['asset_symbol'], "address": address,"date": dateToday}             
                    dict_list.append(neoscan_dic)
                    
                    
                    
                    
        print("\nGlobal JSON Create....\n")            
        print(json.dumps(dict_list, sort_keys=True, indent=2))  
        
        #open a file for writing 
        with open('./api reports/balance.csv', 'a', newline='') as outputfile:

                #create the csv writer object 
                csv_writer = csv.writer(outputfile) 
                
                #headers to the CSV file       
                header=['Ticker', 'Balance', 'Address', 'Date']
                #Writing headers of CSV file 
                csv_writer.writerow(header) 
                
                print("\nWrite to CSV Report...\n")
                
                for dict_item in dict_list:
                    csv_writer.writerow(dict_item.values())
                    print(dict_item.values())
        
        outputfile.close()
        print("\nWrite to CSV completed!!!!File Closed!!!....\n")
        
        
        
except HTTPError as e:
    print("The server returned an HTTP error - "+str(e))
except URLError as e:
    print("The server could not be found! - "+str(e))
