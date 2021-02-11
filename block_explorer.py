#!/usr/bin/env python
import os
import sys
import platform
from datetime import datetime
import urllib.request
from urllib.error import HTTPError
from urllib.error import URLError
import json
import csv

try:
    
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}

    # ---------------Dictionaries {}---------------
    dict_list = []
    # ------------API KEY----------------
    cryptoid_key = '45510f721dc1'
    # --------------------------------------

    #COPY API LINK FROM CSV FILE & ADDING TO api_link
    print('\nBlock Explorer Started (reading csv Input...)\n')

    #open a file for writing 
    with open('addresses.csv', newline='') as inputfile:
        file_reader = csv.reader(inputfile)

        #Check and Remove existing file first then populate updated records
        if open('balance report.csv', 'a', newline=''):
            os.remove('balance report.csv')  

        pointer=0
        now = datetime.now()
        dateToday = now.strftime("%Y-%m-%d %H:%M:%S")
        
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

                api_request = urllib.request.Request(url_cryptoid, headers=hdr)
                api_reply = urllib.request.urlopen(api_request).read()
                api_json=json.loads(api_reply)
                
        
                cryptoid_dic = {"assets_symbol": ticker,"address": address, "balance": api_json, "date": dateToday}
                dict_list.append(cryptoid_dic)

            elif pointer >= 1 and ticker == "NEO":

                pointer+=1

                url_neoscan = f"https://api.neoscan.io/api/main_net/v1/get_balance/" + str(address)
                api_request = urllib.request.Request(url_neoscan, headers=hdr)
                api_reply = urllib.request.urlopen(api_request).read()
                api_json=json.loads(api_reply)
                api_data=api_json['balance']

                for dict_item in api_data:

                    if dict_item['asset_symbol'].lower() == "NEO".lower():
                        neoscan_dic = {"assets_symbol": dict_item['asset_symbol'], "address": address, "balance": dict_item['amount'], "date": dateToday}             
                        dict_list.append(neoscan_dic)
                    
            elif pointer >= 1 and ticker == "ETC":

                pointer+=1
                print(ticker+" : "+address)   
                
                api_url = f"https://blockscout.com/etc/mainnet/api?module=account&action=balance&address=" + str(address)

                
                api_request = urllib.request.Request(api_url, headers=hdr)
                api_reply = urllib.request.urlopen(api_request).read()
                api_json=json.loads(api_reply.decode())
            

                reddcoin_dic = {"assets_symbol": ticker, "address": address, "balance": api_json['result'], "date": dateToday}
                dict_list.append(reddcoin_dic)

            elif pointer >= 1 and ticker == "EWT":

                pointer+=1
                print(ticker+" : "+address)   
                
                api_url = f"https://explorer.energyweb.org/api?module=account&action=balance&address=" + str(address)


                api_request = urllib.request.Request(api_url, headers=hdr)
                api_reply = urllib.request.urlopen(api_request).read()
                api_json=json.loads(api_reply.decode())

                reddcoin_dic = {"assets_symbol": ticker, "address": address, "balance": api_json['result'], "date": dateToday}
                dict_list.append(reddcoin_dic)
                
            elif pointer >= 1 and ticker == "ONT":

                pointer+=1
                print(ticker+" : "+address)   
                
                api_url = f"https://explorer.ont.io/v2/addresses/" + str(address) +"/native/balances"


                api_request = urllib.request.Request(api_url, headers=hdr)
                api_reply = urllib.request.urlopen(api_request).read()
                api_json = json.loads(api_reply.decode())
                api_data = api_json["result"]
                
                #print(json.dumps(api_data, sort_keys=True, indent=2))

                for dict_item in api_data:

                    if dict_item['asset_name'].lower()  == "ONT".lower():
                        ont_dic = {"assets_symbol": dict_item['asset_name'].upper(), "address": address, "balance": dict_item['balance'], "date": dateToday}             
                        dict_list.append(ont_dic)
                    
                                            
        print("\nAPIs Global JSON Creating....\n")            
        print(json.dumps(dict_list, sort_keys=True, indent=2))  
        
        #open a file for writing 
        with open('balance report.csv', 'a', newline='') as outputfile:

                #create the csv writer object 
                csv_writer = csv.writer(outputfile) 
                
                #headers to the CSV file       
                header=['Ticker', 'Address', 'Balance', 'Date']
                #Writing headers of CSV file 
                csv_writer.writerow(header) 
                
                for dict_item in dict_list:
                    csv_writer.writerow(dict_item.values())
                    #print(dict_item.values())
        
        outputfile.close()
        print("\nCSV Report Generated succesfully!!!!File Closed!!!....\n")
        
        
        
except HTTPError as e:
    print("The server returned an HTTP error - "+str(e))
except URLError as e:
    print("The server could not be found! - "+str(e))



