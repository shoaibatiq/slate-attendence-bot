#Final
from selenium import webdriver
import datetime
from time import sleep
import  calendar
from datetime import timedelta
from selenium.webdriver.common.keys import Keys
import pause
from credentials import email,Password
import sys

if(Password is None or email is None):
    input('Please input your slate email and password using "ChangeCredentials.exe" to use this program.')
    sys.exit(0)
options = webdriver.ChromeOptions()
options.add_argument('--headless')



def DayClick(i):
    try:
        sleep(2)
        day=driver.find_element_by_xpath(f'//table[@class="minicalendar calendartable"]//a[contains(text(),"{datetime.datetime.today().day}")]')
        day.click()
    except:
        if(i!=0):
            DayClick((i-1))
    

def convert24(str1): 
      
  
    if str1[-2:] == "AM" and str1[:2] == "12": 
        return "00" + str1[2:-2] 
          
    elif str1[-2:] == "AM": 
        return str1[:-2] 
      
    elif str1[-2:] == "PM" and str1[:2] == "12": 
        return str1[:-2] 
          
    else: 
          
        return str(int(str1[:2]) + 12) + str1[2:8] 
    
def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end
    
    
year=datetime.date.today().year
month=datetime.date.today().month
daTe=datetime.date.today().day

schedule={
 'Tuesday':   [
                (datetime.datetime(year, month, daTe, 10, 30, 2, 0),datetime.datetime(year, month, daTe, 11, 0, 0, 0)),
                (datetime.datetime(year, month, daTe, 13, 30, 2, 0), datetime.datetime(year, month, daTe, 14, 0, 0, 0)),
                (datetime.datetime(year, month, daTe, 16, 30, 2, 0), datetime.datetime(year, month, daTe, 17, 0, 0, 0))],

 'Wednesday': [
                (datetime.datetime(year, month, daTe, 9, 0, 2, 0),datetime.datetime(year, month, daTe, 9, 30, 0, 0)),
                (datetime.datetime(year, month, daTe, 10, 30, 2, 0),datetime.datetime(year, month, daTe, 11, 0, 0, 0)),
                (datetime.datetime(year, month, daTe, 12, 0, 2, 0), datetime.datetime(year, month, daTe, 12, 30, 0, 0)),
                (datetime.datetime(year, month, daTe, 16, 30, 2, 0), datetime.datetime(year, month, daTe, 17, 0, 0, 0))],

 'Thursday':  [
                (datetime.datetime(year, month, daTe, 10, 30, 2, 0),datetime.datetime(year, month, daTe, 11, 0, 0, 0)),
                (datetime.datetime(year, month, daTe, 13, 30, 2, 0), datetime.datetime(year, month, daTe, 14, 0, 0, 0))],

 'Friday':    [
                (datetime.datetime(year, month, daTe, 10, 30, 2, 0),datetime.datetime(year, month, daTe, 11, 0, 0, 0)),
                (datetime.datetime(year, month, daTe, 12, 0, 2, 0), datetime.datetime(year, month, daTe, 12, 30, 0, 0))],

 'Saturday':  [
                (datetime.datetime(year, month, daTe, 9, 0, 2, 0),datetime.datetime(year, month, daTe, 9, 30, 0, 0)),
                (datetime.datetime(year, month, daTe, 10, 30, 2, 0),datetime.datetime(year, month, daTe, 11, 0, 0, 0)),
                (datetime.datetime(year, month, daTe, 13, 30, 2, 0), datetime.datetime(year, month, daTe, 14, 0, 0, 0))]
}

toDay=calendar.day_name[calendar.weekday(datetime.datetime.today().year, datetime.datetime.today().month, datetime.datetime.today().day)]
Tschedule=schedule[toDay]

for lec in Tschedule:
    try:
        pause.until(lec[0])
        sleep(10)
        if datetime.datetime.today() > lec[0]  and datetime.datetime.today() < lec[1]:
            try:
                print("Attempting to Submit Attendence.")
                driver=webdriver.Chrome("chromedriver.exe",options=options)
                driver.get("https://slate.uol.edu.pk")
                driver.find_element_by_xpath("//a[@title='Google']").click()
                driver.find_element_by_xpath("//input[@type='email']").send_keys(email)
                driver.find_element_by_xpath("//input[@type='email']").send_keys(Keys.RETURN)
                sleep(6)
                driver.find_element_by_xpath("//input[@type='password']").send_keys(Password)
                driver.find_element_by_xpath("//input[@type='password']").send_keys(Keys.RETURN)
                try:
                    driver.find_element_by_xpath('//a[@title="Google"]').click()
                except:
                    pass 
            except:
                driver.quit()
                input("Error in login. Make sure you have a working internet connection and input your correct credentials using ChangeCredentials.exe. ")
                sys.exit(0)

            sleep(12)
            DayClick(3)
            att_elements=driver.find_elements_by_xpath('//div[@data-type="event" and @data-event-title="Attendance"]')
            for a in att_elements:
                copy_text=a.text.split("\n")[1]

                start,end=a.text.split("\n")[1].replace("Today, ","").replace(" ","").split('»')
                start=start.replace(start[-2:],f":00 {start[-2:]}")
                start= '0'+start if int(start.split(":")[0]) <10 else start
                start=convert24(start).split(":")
                start=datetime.time(int(start[0]),int(start[1]),int(start[2]))

                end=end.replace(end[-2:],f":00 {end[-2:]}")
                end= '0'+end if int(end.split(":")[0]) <10 else end
                end=convert24(end).split(":")
                end=datetime.time(int(end[0]),int(end[1]),int(end[2]))

                now=datetime.datetime.now()
                now=datetime.time(now.hour,now.minute,now.second)
                if(time_in_range(start, end, now)):
                    attendence=a

            subjectName=attendence.text.split('\n')[-2]
            attendence.find_element_by_partial_link_text("Go to activity").click()
            driver.get(driver.find_element_by_xpath("//a[contains(text(),'Submit attendance')]").get_attribute('href'))
            driver.find_element_by_xpath('//span[contains(text(),"Present")]/parent::*').click()
            driver.find_element_by_id("id_submitbutton").click()
            sleep(3)
            driver.quit()
            print(subjectName,"attendece submitted.")
    except:
        driver.quit()
        print("Error!")

input("\n\nPress any key to close.")