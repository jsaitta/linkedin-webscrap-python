#LINKEDIN Web Scraping

# imports
import parameters
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from parsel import Selector
import pandas as pd
from pandas import ExcelWriter
import itertools
import datetime 
import os

#set web driver and selenium directories
options = Options()
options.binary_location = "C:\\Users\\jsaitta\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe"
driver = webdriver.Chrome(chrome_options = options, executable_path=r'C:\Python\chromedriver.exe')

#log into Linkedin
driver.get('https://www.linkedin.com')
time.sleep(5)
# locate login form 
username = driver.find_element_by_name("session_key")
# send_keys() to simulate key strokes
username.send_keys(parameters.linkedin_username)
time.sleep(1)

# locate login pass form 
password = driver.find_element_by_name("session_password")
# send_keys() to simulate key strokes
password.send_keys(parameters.linkedin_password)
time.sleep(1)

# locate submit button 
sign_in_button = driver.find_element_by_class_name('sign-in-form__submit-btn')

#sign in
sign_in_button.click()
time.sleep(1)

#create blank dicionaries
college_ind_comp_data= {} 
ind_college = {}  
comp_college = {}   
alum_total={}

#loop through different colleges
for x in parameters.colleges:
    #go to ind campus website
    driver.get(parameters.colleges_urls[x])
    time.sleep(7)
    
    #download website text
    sel = Selector(text=driver.page_source)
    time.sleep(.5)
    
    #scrap alum text
    alum_tot = sel.xpath("//html/body/div[5]/div[4]/div[3]/div/div[2]/div/div[2]/div[1]/div[1]/span/text()").extract_first()
    alum_tot = alum_tot.strip()
    alum_tot = [alum_tot.replace(" alumni","")]
    time.sleep(.5)
     
    #go to post 2000 year campus site
    driver.get(parameters.colleges_urls[x] + '?educationStartYear=2000')
    time.sleep(7)
    
    # locate next button by_xpath
    next_button1 = driver.find_element_by_xpath('//html/body/div[5]/div[4]/div[3]/div/div[2]/div/div[2]/div[1]/div[2]/div/artdeco-carousel/artdeco-carousel-heading/artdeco-carousel-navigation/artdeco-pagination/button[2]/span')
    #sign in
    next_button1.click()
    time.sleep(2)
    
    #download website text
    sel = Selector(text=driver.page_source)
    time.sleep(.5)
    
    #scrap other text
    ind_names = [sel.xpath("//html/body/div[5]/div[4]/div[3]/div/div[2]/div/div[2]/div[1]/div[2]/div/artdeco-carousel/artdeco-carousel-content/ul/li[3]/div/div/div/div[" + str(i) + "]/div/span/text()").extract_first() for i in range(2,parameters.top_15)]
    ind_vals = [sel.xpath("//html/body/div[5]/div[4]/div[3]/div/div[2]/div/div[2]/div[1]/div[2]/div/artdeco-carousel/artdeco-carousel-content/ul/li[3]/div/div/div/div[" + str(i) + "]/div/strong/text()").extract_first() for i in range(2,parameters.top_15)]
    co_names = [sel.xpath("//html/body/div[5]/div[4]/div[3]/div/div[2]/div/div[2]/div[1]/div[2]/div/artdeco-carousel/artdeco-carousel-content/ul/li[2]/div/div/div/div[" + str(i) + "]/div/span/text()").extract_first() for i in range(2,parameters.top_15)]
    co_vals = [sel.xpath("//html/body/div[5]/div[4]/div[3]/div/div[2]/div/div[2]/div[1]/div[2]/div/artdeco-carousel/artdeco-carousel-content/ul/li[2]/div/div/div/div[" + str(i) + "]/div/strong/text()").extract_first() for i in range(2,parameters.top_15)]
    
    #create blank dicts
    industries = {}
    ind_co = {}
    college_ind_comp_data["" + str(x) + ""] = {}  
    
    #create dictioary from lists
    ind_college["" + str(x) + ""]=dict(zip(ind_names, ind_vals))
    comp_college["" + str(x) + ""]=dict(zip(co_names, co_vals))
    alum_total["" + str(x) + ""]=dict(zip('alumini', alum_tot))
          
    #create blank dicts
    for z in ind_names:
        industries[z] = []
        ind_co[z] = []
        
   #loop through campus ind lists
    for z in ind_names:      
        driver.get(parameters.colleges_urls[x] + '?educationStartYear=2000&keywords=' + str(z) + '')
        time.sleep(3.5)
        
        #rescrap
        selector = Selector(text=driver.page_source)
        industries[z] = [selector.xpath("//html/body/div[5]/div[4]/div[3]/div/div[2]/div/div[2]/div[1]/div[2]/div/artdeco-carousel/artdeco-carousel-content/ul/li[2]/div/div/div/div[" + str(x) + "]/div/span/text()").extract_first() for x in range(2, parameters.top_15)]
        ind_co[z] = [selector.xpath("//html/body/div[5]/div[4]/div[3]/div/div[2]/div/div[2]/div[1]/div[2]/div/artdeco-carousel/artdeco-carousel-content/ul/li[2]/div/div/div/div[" + str(x) + "]/div/strong/text()").extract_first() for x in range(2, parameters.top_15)]
       
    #put data into dict
    for z in industries:
        college_ind_comp_data["" + str(x) + ""]["" + str(z) + ""]=dict(zip(industries["" + str(z) + ""], ind_co["" + str(z) + ""]))


driver.close() 

#flip/invert dictionary - by industry
ind_college_comp_data=dict([(x, dict([(k, college_ind_comp_data[k][x]) for k,v in college_ind_comp_data.items() if x in college_ind_comp_data[k]])) for x in set(itertools.chain(*[z for z in college_ind_comp_data.values()]))])

#get list of all industries across all campuses
industries_all=[*ind_college_comp_data]

#create dfs
df_ind=pd.DataFrame.from_dict(ind_college).T
df_co=pd.DataFrame.from_dict(comp_college)
df_alum=pd.DataFrame.from_dict(alum_total).T
df_alum.columns = ['# of alum on LinkedIn']
            
#write to excel                   
writer = ExcelWriter("output_linkedin_ivy_"+ str(datetime.date.today())+".xlsx",
                        engine='xlsxwriter',
                        options={'strings_to_numbers': True})
df_alum.to_excel(writer, 'number of alum')
df_ind.to_excel(writer, 'industry by college')
df_co.to_excel(writer, 'comp by college')

for x in parameters.colleges:
    pd.DataFrame.from_dict(college_ind_comp_data["" + str(x) + ""], orient='index').T.to_excel(writer, "" + str(x[0:30]) + "")

for x in industries_all:
    pd.DataFrame.from_dict(ind_college_comp_data["" + str(x) + ""], orient='index').T.to_excel(writer, "" + str(x[0:30]) + "")

writer.save()

#open file
file = "output_linkedin_ivy_"+ str(datetime.date.today())+".xlsx"
os.startfile(file)


