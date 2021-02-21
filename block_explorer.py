#!/usr/bin/env python
from datetime import datetime
import urllib.request
from urllib.error import HTTPError
from urllib.error import URLError
import json
import csv
import os

try:
    
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
    
    #dict_list is the Global JSON list of dict objects
    dict_list = []

    print('\nBlock Explorer Started (reading csv Input...)\n')

    with open('addresses.csv', newline='') as inputfile:
        file_reader = csv.reader(inputfile)

        #Check and Remove the existing file and then populate it with updated records
        if open('balance report.csv', 'a', newline=''):
            os.remove('balance report.csv')  

        pointer=0
        now = datetime.now()
        dateTimeToday = now.strftime("%Y-%m-%d %H:%M:%S")
        
        for address_line in file_reader:

            ticker = (address_line[0].strip(" ")).upper()
            address = address_line[1].strip(" ")

            if pointer == 0:
                
                pointer += 1
                print(ticker+" : "+address+"\n")

            elif pointer >= 1 and ticker =="FTC" or ticker =="DASH" or ticker == "DGB":

                pointer+=1
                print(ticker+" : "+address)   

                api_url = f"https://chainz.cryptoid.info/{ticker.lower()}/api.dws?q=getbalance&a={str(address)}"

                api_request = urllib.request.Request(api_url, headers=hdr)
                api_reply = urllib.request.urlopen(api_request).read()
                api_json=json.loads(api_reply)
                
        
                dict_object = {"assets_symbol": ticker,"address": address, "balance": api_json, "date": dateTimeToday}
                dict_list.append(dict_object)

            elif pointer >= 1 and ticker == "NEO":

                pointer+=1

                api_url = f"https://api.neoscan.io/api/main_net/v1/get_balance/{str(address)}"
                api_request = urllib.request.Request(api_url, headers=hdr)
                api_reply = urllib.request.urlopen(api_request).read()
                api_json=json.loads(api_reply)
                api_data=api_json['balance']

                for dict_item in api_data:

                    if dict_item['asset_symbol'].lower() == "NEO".lower():
                        dict_object = {"assets_symbol": dict_item['asset_symbol'], "address": address, "balance": dict_item['amount'], "date": dateTimeToday}             
                        dict_list.append(dict_object)
                    
            elif pointer >= 1 and ticker == "ETC":

                pointer+=1
                print(ticker+" : "+address)   
                
                api_url = f"https://blockscout.com/etc/mainnet/api?module=account&action=balance&address={str(address)}"

                
                api_request = urllib.request.Request(api_url, headers=hdr)
                api_reply = urllib.request.urlopen(api_request).read()
                api_json=json.loads(api_reply.decode())
            

                dict_object = {"assets_symbol": ticker, "address": address, "balance": int(api_json['result'])/(10**18), "date": dateTimeToday}
                dict_list.append(dict_object)

            elif pointer >= 1 and ticker == "EWT":

                pointer+=1
                print(ticker+" : "+address)   
                
                api_url = f"https://explorer.energyweb.org/api?module=account&action=balance&address={str(address)}"


                api_request = urllib.request.Request(api_url, headers=hdr)
                api_reply = urllib.request.urlopen(api_request).read()
                api_json=json.loads(api_reply.decode())

                dict_object = {"assets_symbol": ticker, "address": address, "balance": int(api_json['result'])/(10**18), "date": dateTimeToday}
                dict_list.append(dict_object)
                
            elif pointer >= 1 and ticker == "ONT":

                pointer+=1
                print(ticker+" : "+address)   
                
                api_url = f"https://explorer.ont.io/v2/addresses/{str(address)}/native/balances"


                api_request = urllib.request.Request(api_url, headers=hdr)
                api_reply = urllib.request.urlopen(api_request).read()
                api_json = json.loads(api_reply.decode())
                api_data = api_json["result"]
                
                #print(json.dumps(api_data, sort_keys=True, indent=2))

                for dict_item in api_data:

                    if dict_item['asset_name'].lower()  == "ONT".lower():
                        dict_object = {"assets_symbol": dict_item['asset_name'].upper(), "address": address, "balance": dict_item['balance'], "date": dateTimeToday}             
                        dict_list.append(dict_object)
                  
            elif pointer >= 1 and ticker == "ALGO":

                pointer+=1
                print(ticker+" : "+address)   
                
                api_url = f"https://api.algoexplorer.io/idx2/v2/accounts/{str(address)}"


                api_request = urllib.request.Request(api_url, headers=hdr)
                api_reply = urllib.request.urlopen(api_request).read()
                api_json = json.loads(api_reply.decode())
                api_data = api_json["account"]
                
                #print(json.dumps(api_data, sort_keys=True, indent=2))

                dict_object = {"assets_symbol": ticker, "address": address, "balance": int(api_data['amount'])*(10**12), "date": dateTimeToday}             
                dict_list.append(dict_object)
                
            elif pointer >= 1 and ticker == "BTS":

                pointer+=1
                print(ticker+" : "+address)   
                
                api_url = f"https://cryptofresh.com/api/account/balances?account={str(address)}"


                api_request = urllib.request.Request(api_url, headers=hdr)
                api_reply = urllib.request.urlopen(api_request).read()
                api_json = json.loads(api_reply.decode())
                api_data = api_json["BTS"]
                
                #print(json.dumps(api_data, sort_keys=True, indent=2))

                dict_object = {"assets_symbol": ticker, "address": address, "balance": api_data['balance'], "date": dateTimeToday}             
                dict_list.append(dict_object)
            
            elif pointer >= 1 and ticker == "RDD":

                pointer+=1
                print(ticker+" : "+address)   
                
                api_url = f"https://live.reddcoin.com/api/addr/{str(address)}/balance"


                api_request = urllib.request.Request(api_url, headers=hdr)
                api_reply = urllib.request.urlopen(api_request).read()
                api_json = json.loads(api_reply.decode())
                
                #print(json.dumps(api_json, sort_keys=True, indent=2))

                dict_object = {"assets_symbol": ticker, "address": address, "balance": int(api_json)*(10**12), "date": dateTimeToday}             
                dict_list.append(dict_object)
            
            elif pointer >= 1 and ticker == "SC":

                pointer+=1
                print(ticker+" : "+address)   
                
                api_url = f"https://siastats.info:3500/navigator-api/hash/{str(address)}"


                api_request = urllib.request.Request(api_url, headers=hdr)
                api_reply = urllib.request.urlopen(api_request).read()
                api_json = ((json.loads(api_reply.decode()))[1])["balanceSc"]
                
                #print(json.dumps(api_json, sort_keys=True, indent=2))

                dict_object = {"assets_symbol": ticker, "address": address, "balance": int(api_json)/(10**18), "date": dateTimeToday}             
                dict_list.append(dict_object)
            
            elif pointer >= 1 and ticker == "DCR":

                pointer+=1
                print(ticker+" : "+address)   
                
                api_url = f"https://dcrdata.decred.org/api/address/{str(address)}/totals"


                api_request = urllib.request.Request(api_url, headers=hdr)
                api_reply = urllib.request.urlopen(api_request).read()
                api_json = json.loads(api_reply)
                
                #print(json.dumps(api_json["dcr_spent"], sort_keys=True, indent=2))

                dict_object = {"assets_symbol": ticker, "address": address, "balance": int(api_json["dcr_unspent"]), "date": dateTimeToday}             
                dict_list.append(dict_object)
                        
                        
                        
        print("\nCreating APIs Global JSON....\n")            
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