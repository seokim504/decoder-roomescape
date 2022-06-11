# -*- coding: utf-8 -*-

from selenium import webdriver
import time
from datetime import datetime
from unittest import result
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import re
import telegram


today = str(datetime.today().year)+'-'+('0'+str(datetime.today().month))[-2:]+'-'+('0'+str(datetime.today().day))[-2:]

# Selenium Driver 위치지정
driver = webdriver.Chrome('/Users/INDIGO/Downloads/chromedriver')
url = "http://decoder.kr/book-rubato/"
all_time = ['10:00', '11:30', ' 1:00', ' 2:30', ' 4:00', ' 5:30', ' 7:00', ' 8:30', '10:00']
x_path_nextMonth = '/html/body/div[2]/div/div[2]/section/div/div/div[2]/div[4]/div/div/div[3]/span/div/div/div/div/div/div/div[4]'
result = []

# on Saturday
def scrollSat():
    driver.get(url)
    time.sleep(1)

    for num_month in range(1,13):
        for num_week in range(1,5):
            x_path = '/html/body/div[2]/div/div[2]/section/div/div/div[2]/div[4]/div/div/div[3]/span/div/div/div/div/div/table/tbody/tr[' + str(num_week)+ ']/td[7]/div' # tempo rubato
            # x_path = '/html/body/div[2]/div/div[2]/section/div/div/div[2]/div[3]/div/div/div[3]/span/div/div/div/div/div/table/tbody/tr[' + str(num_week)+ ']/td[7]/div' # room2
            calendar = driver.find_element_by_xpath(x_path)
            # Selenium 버튼클릭
            calendar.click()

            time.sleep(1)
            #-------------------------------- Beautiful Soup Analysis -------------------------------#
            html = driver.page_source
            bsObject = BeautifulSoup(html, 'html.parser')
            search_result = bsObject.select_one('div.ab-booking-form').find_all('button',{"class":"booked"})
            bookedDate_search_result = str(search_result)[str(search_result).find('data-group')+12:str(search_result).find('data-group')+22]
            result_temp = [str(search_result)[m.start()-6:m.start()-1] for m in re.finditer( 'am', str(search_result))]+[str(search_result)[m.start()-6:m.start()-1] for m in re.finditer( 'pm', str(search_result))]
            result_temp.insert(0,bookedDate_search_result)

            if (result_temp[0] != today) & (all_time != result_temp[1:]):
                result.append(result_temp)
                print(result_temp)

        calendar = driver.find_element_by_xpath(x_path_nextMonth)
        # Selenium 버튼클릭
        calendar.click()

# on Sunday
def scrollSun():
    driver.get(url)
    time.sleep(1)
    for num_month in range(1,13):
        for num_week in range(2,6):
            x_path = '/html/body/div[2]/div/div[2]/section/div/div/div[2]/div[4]/div/div/div[3]/span/div/div/div/div/div/table/tbody/tr[' + str(num_week)+ ']/td[1]/div' # tempo rubato
            calendar = driver.find_element_by_xpath(x_path)
            # Selenium 버튼클릭
            calendar.click()

            time.sleep(1)
            #-------------------------------- Beautiful Soup Analysis -------------------------------#
            html = driver.page_source
            bsObject = BeautifulSoup(html, 'html.parser')
            search_result = bsObject.select_one('div.ab-booking-form').find_all('button',{"class":"booked"})
            bookedDate_search_result = str(search_result)[str(search_result).find('data-group')+12:str(search_result).find('data-group')+22]
            result_temp = [str(search_result)[m.start()-6:m.start()-1] for m in re.finditer( 'am', str(search_result))]+[str(search_result)[m.start()-6:m.start()-1] for m in re.finditer( 'pm', str(search_result))]
            result_temp.insert(0,bookedDate_search_result)

            if (result_temp[0] != today) & (all_time != result_temp[1:]):
                result.append(result_temp)
                print(result_temp)

        calendar = driver.find_element_by_xpath(x_path_nextMonth)
        # Selenium 버튼클릭
        calendar.click()



def sendMsg():
    bot = telegram.Bot(token='5489946700:AAGjGrRq10iuw3fBEdAPtZiaSH0CrpxkLpU')
    chat_id = 1656535070

    if result == [] :
        result.append('There is no time for available')
    bot.sendMessage(chat_id=chat_id, text=result)


#------------------------------------ Main ------------------------------------#
scrollSat()
scrollSun()

sendMsg()
driver.quit()
