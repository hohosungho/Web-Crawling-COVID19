from CovidDataManager import CovidDataManager as DBManager
import pymysql as mysql
import pandas as pd
import platform 
import folium
import matplotlib.pyplot as plt
from selenium import webdriver
from matplotlib import font_manager, rc
from bs4 import BeautifulSoup

manager = DBManager()

manager.cleanTables()

driver = webdriver.Chrome('C:/ProgramData/Anaconda/envs/playdata/crawling/chromedriver.exe')
url = 'https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EC%BD%94%EB%A1%9C%EB%82%98+%ED%98%84%ED%99%A9&oquery=%EC%BD%94%EB%A1%9C%EB%82%98+%ED%98%84%ED%99%A9&tqi=hfkY0wp0Jy0ssiQ97E8ssssstiR-146897'

driver.get( url )

html = driver.page_source

soup = BeautifulSoup(html, 'html.parser')
# data_chart = soup.select('#target2 .column')

for idx in range(1, 7):
    data_bar = driver.find_element_by_xpath('//*[@id="target2"]/dl/div[{}]/dd[1]'.format(idx))
    data_bar.click()
    date_raw = driver.find_element_by_class_name('_x_value').text.split('.')
    date = '2021-{}-{}'.format(
                        date_raw[0].zfill(2), 
                        date_raw[1].zfill(2))
    domestic = driver.find_element_by_class_name('_y_first_value').text
    international = driver.find_element_by_class_name('_y_second_value').text
    
    manager.insertIntoDailyData([date,domestic,international]) 

res = manager.fetchDailyData()

daily_covid_dates  = []
daily_covid_cnfmed_domestic = []
daily_covid_cnfmed_international = []

for row in res:
    daily_covid_dates.append( '{}.{}'.format(row[0].month, 
                                             row[0].day))  # date
    daily_covid_cnfmed_domestic.append(row[1])             # domestic count
    daily_covid_cnfmed_international.append(row[2])        # international count


daily_df = pd.DataFrame({'Date':daily_covid_dates,
                         'International':daily_covid_cnfmed_international,
                         'Domestic':daily_covid_cnfmed_domestic
                        }).set_index( 'Date' )

total_cases_button = driver.find_element_by_xpath( '*//span[@class="menu" and text()="지역별 표"]')
total_cases_button.click()

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

total_confirmed_cases = []
total_data = soup.select( '.type_basic > .table' )
total_pages = 3

for page in range( total_pages ):
    data  =  total_data[ page ].select( 'tbody tr td' )
    for idx in range( 0, len( data ), 3 ):
        city  = data[idx].select( '.text' )[0].text.strip()
        count = data[idx + 1].select( '.text' )[0].text
        total_confirmed_cases.append( [ city, count ] )
        
manager.insertIntoTotalData( total_confirmed_cases )

res = manager.fetchTotalData()

total_covid_dates = []
total_covid_cnfmed = []

for row in res:
    total_covid_dates.append( row[ 0 ] )  # city
    total_covid_cnfmed.append( row[ 1 ] ) # count


total_df = pd.DataFrame( {'City'  : total_covid_dates,
                          'Count' : total_covid_cnfmed } ).set_index( 'City' )

daily_df.plot(
    kind='bar', 
    title='일별 신규 확진자 수',
    rot=0,
    ylabel='확진자 수',
    stacked=True,
    color={"Domestic": "#ff3150", "International": "#1e1e23"}
)

plt.show()

location_df = pd.read_csv('./files/도시별_경위도.csv' )

total_df_no_index = total_df.reset_index()
location_count_df = pd.merge(location_df, total_df_no_index, on='City', how='inner')

center = ['36.12790033349445', '127.82658973039062'] 
m = folium.Map(location=center, zoom_start=6)

for i in range( len(location_count_df ) ):
    data = location_count_df.iloc[i]
    name = data['City']
    long = float(data['Longitute'])
    lat = float(data['Latitude'])
    size = int(data['Count']) // 1000
    folium.CircleMarker((long,lat), radius = size, color='#957DAD', tooltip=name, fill=True).add_to(m)

m.save('./files/covid19_total_confirmed_cases.html')

manager.closeConnection()