from selenium import webdriver
import pandas as pd


driver = webdriver.Chrome()
df = pd.DataFrame(columns=['Name', 'Address', 'Phone'])

# Scrape all dat from 1 page - 20 results at a time 
def extract_page():
    for i in range(20):
        elem = driver.find_element('xpath', "/html/body/div[6]/div[2]/div[1]/section/div[3]/div[4]/ul/li["+ str(i+1) +"]")
        data = elem.text
        li = data.split('\n')
      
        #check if in Austin
        flag = False
        for strr in li:
            if "Austin, TX" in strr:
                flag = True
                break
        if flag:
            #name
            name = li[0]
            #address
            address = 'null'
            for strr in li:
                if "Austin, TX" in strr:
                    address = strr
            #phone
            phone = 'null'
            for strr in li:
                if "(" in strr and ') ' in strr and '-' in strr and len(strr)==14:
                    phone = strr
            #print(name, address, phone)
            df.loc[len(df.index)] = [name, address, phone]


# Loop through all the pages 
for i in range(500):
    url = 'https://www.avvo.com/all-lawyers/tx/austin.html?page=' +str(i+1)+ '&sort=client_rating'
    driver = webdriver.Chrome()
    driver.get(url)#put here the address of your page

    extract_page()

    #Keep count on which page the program is 
    print('Just did', i+1, 'page')

# Save all results as csv
df.to_csv('Austin-lawyers.csv', index=False)

# Save only the results with phone number
df1 = df[df['Phone']!='null']
df1.to_csv('Austin-lawyers-name-addr-phone.csv', index=False)

# Save only the results without phone number
df1 = df[df['Phone']=='null']
df1.to_csv('Austin-lawyers-name-addr-no_phone.csv', index=False)