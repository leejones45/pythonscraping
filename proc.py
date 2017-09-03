import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import datetime
import sqlite3
import os

os.chdir('/home/pi/Documents/StudentData')
url= "http://www.chesterstudentstamp.co.uk/SearchResults/Print/All"
r = requests.get(url)
source = r.text
t = datetime.datetime.now().date()
soup = BeautifulSoup(source,"html5lib")

row_marker = 0
column_marker = 0
row_count = 0
#Determine size of dataframe
for header in soup.find_all("div", attrs={'class':'innerListing'}):
    title = header.find("h2")
    row_count +=1

new_table = pd.DataFrame(columns = ["Title", "TotalBedrooms", "BedroomsAvailable", "Area","PropertyType","Date"], index = range(0,row_count))

#Process Title
for header in soup.find_all("div", attrs={'class':'innerListing'}):
    title = header.find("h2")
    new_table.iat[row_marker,column_marker] = title.text.strip()
    row_marker +=1

column_marker = 1
row_marker = 0

#Process Bedrooms
for layout in soup.find_all("div", attrs={'class':'layout'}):
    for info in layout.find_all("span", attrs={'class':'info',"id":True}):
        if "Bedrooms" in info["id"]:
            new_table.iat[row_marker,column_marker] = info.text.strip()
            column_marker += 1
    row_marker +=1
    column_marker =1

column_marker = 3
row_marker = 0

#Process Area
for layout in soup.find_all("div", attrs={'class':'layout'}):
    for info in layout.find_all("span", attrs={'class':'info',"id":True}):
        if "PropertyArea" in info["id"]:
            new_table.iat[row_marker,column_marker] = info.text.strip()
            row_marker +=1
    

column_marker = 4
row_marker = 0

#Process PropertyType and Date of execution
for layout in soup.find_all("div", attrs={'class':'layout'}):
    for info in layout.find_all("span", attrs={'class':'info',"id":True}):
        if "PropertyType" in info["id"]:
            new_table.iat[row_marker,column_marker] = info.text.strip()
            new_table.iat[row_marker,column_marker+1] = t
            row_marker +=1
   

conn = sqlite3.connect("student_data.db")
new_table.to_sql("student_data", conn,if_exists='append')
new_table.to_csv(r'/archive/stats_%s%s%s.txt' % (t.day, t.month, t.year), index=None, sep=';', mode='a')

