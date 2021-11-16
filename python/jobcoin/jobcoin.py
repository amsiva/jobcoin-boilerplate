import sys
import os
import requests
import json
from  config import *



            


def mixer(addresses,request_balance, post_transaction): 
    
    
    
    file_exists = os.path.exists('users.json')
    
    if file_exists :
        current_key=0
        jsonFile = open("users.json", "r") # Open the JSON file for reading
        data = json.load(jsonFile) # Read the JSON into the buffer
        jsonFile.close() # Close the JSON file
        for address in addresses:
            for key in data.keys():
               
                
                
                if address in data[key]:
                    current_key=key
                    break
        if current_key==0:
            new_key=int(max(data.keys()))+1
            data[new_key]=addresses
            current_key=new_key
        else :
            new_list=data[current_key]+addresses
            data[current_key]=list(dict.fromkeys(new_list))            
    else :
        current_key=1
        data={}
        data[current_key]=addresses

    jsonFilewrite = open("users.json", "w+")
    jsonFilewrite.write(json.dumps(data))
    jsonFilewrite.close()

   
    
    amount_value=0.0
    for address in addresses:
        
        dr=requests.get(f"{request_balance}/{address}")
        
            
        all_transactions = dr.json()
        print(all_transactions)
        amount_value=float(all_transactions['balance']) +amount_value              
        print(amount_value)
        response_value=requests.post(f"{post_transaction}", data = {'fromAddress':address,'toAddress':current_key, "amount":str(amount_value)}) 
        
        if response_value == 422:
            
            raise "Insufficient Funds"


    file_exists_amount = os.path.exists('users_amount.json')
    
    if file_exists_amount :
        jsonFileamount = open("users_amount.json", "r") # Open the JSON file for reading
        data_amount = json.load(jsonFileamount) # Read the JSON into the buffer
        jsonFileamount.close() 
        if current_key in data_amount.keys() :
            data_amount[current_key]=data_amount[current_key]+ amount_value
        else :
            data_amount[current_key]= amount_value 

    else : 
        data_amount={}
        data_amount[current_key]= amount_value
    jsonFilewriteamount = open("users_amount.json", "w+")
    jsonFilewriteamount.write(json.dumps(data_amount))
    jsonFilewriteamount.close()

    print(amount_value)
    print(current_key)
    print(amount_value)
    response_value_new=requests.post(f"{post_transaction}", data = {'fromAddress':str(current_key),'toAddress':'household_account', "amount":str(amount_value)})   
    print(response_value_new)
    if response_value_new == 422:
        raise "Insufficient Funds"



def withdrawal(withdrawal_account, withdrawal_amount, post_transaction):
    fee=withdrawal_amount*0.05
    current_key=0
    jsonFile = open("users.json", "r") 
    data = json.load(jsonFile)
    jsonFile.close()
    print(data)
    for key in data.keys():
        if withdrawal_account in data[key]:
            current_key=key
            break

    if current_key==0:
        raise "No user Found"    

    jsonFileamount = open("users_amount.json", "r") 
    data_amount = json.load(jsonFileamount) 
    jsonFileamount.close() 

    print(data_amount[current_key])
    print(current_key)

    if data_amount[current_key]>= (withdrawal_amount+fee) :
        data_amount[current_key]=data_amount[current_key]- (withdrawal_amount+fee)  

    else :
        raise "Insufficient funds for the particular user and dont retrieve funds from others account"    

    jsonFilewriteamount = open("users_amount.json", "w+")
    jsonFilewriteamount.write(json.dumps(data_amount))
    jsonFilewriteamount.close()     

    requests.post(f"{post_transaction}", data = {'fromAddress':'household_account','toAddress':withdrawal_account, "amount":str((withdrawal_amount+fee))})




if __name__=='__main__':
    print(API_ADDRESS_URL)
    mixer(sys.argv[1],API_ADDRESS_URL,API_TRANSACTIONS_URL )
    withdrawal(sys.argv[2],sys.argv[3],API_TRANSACTIONS_URL)
    #mixer(['Alice'],API_ADDRESS_URL,API_TRANSACTIONS_URL )
    #withdrawal('Alice',10,API_TRANSACTIONS_URL)





