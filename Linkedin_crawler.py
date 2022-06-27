from os import name
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time
import getpass
from datetime import datetime
from insert_data import database


class Crawler:
    
    #log into LinkedIn
    def Login(self):
        userid = str(input("Enter email address or number with country code: "))
        password = getpass.getpass('Enter your password:')
        self.driver = webdriver.Chrome("C:\\Users\\F.Mahmoudi\\Downloads\\chromedriver.exe")
        self.driver.get("https://linkedin.com/uas/login")
        # waiting for the page to load
        time.sleep(5)
        self.username = self.driver.find_element(By.ID,"username")
        self.pword = self.driver.find_element(By.ID,"password")
        self.username.send_keys(userid)
       
        #Enter Your Password
        self.pword.send_keys(password)		
      
        # Clicking on the log in button
    
        self.driver.find_element(By.XPATH,"//button[@type='submit']").click()


    def Conn_Crawling(self):
        # Now using beautiful soup
        connections_url = "https://www.linkedin.com/mynetwork/invite-connect/connections/"
        self.driver.get(connections_url)
        start = time.time()

        # will be used in the while loop
        initialScroll = 0
        finalScroll = 1000

        while True:
            self.driver.execute_script(f"window.scrollTo({initialScroll},{finalScroll})")
            # this command scrolls the window starting from the pixel value stored in the initialScroll
            # variable to the pixel value stored at the finalScroll variable
            initialScroll = finalScroll
            finalScroll += 1000

            # we will stop the script for 3 seconds so that the data can load
            time.sleep(3)
            end = time.time()

            # We will scroll for 20 seconds.
            if round(end - start) > 20:
                break
        self.src = self.driver.page_source
        self.soup = BeautifulSoup(self.src, 'lxml')
        self.intro = self.soup.find_all('a', {'class': 'ember-view mn-connection-card__link'},href=True)
        self.l =[]
        for i in self.intro:
            connection_url = f"https://www.linkedin.com/{i['href']}"
            name,location,about = self.Crawling(connection_url)
        
            self.l.append({"Name": name, "Location":location,"about": about})
            
        return self.l

    def Crawling(self,url):
        self.driver.get(url)
        self.src = self.driver.page_source
        self.soup = BeautifulSoup(self.src, 'lxml')
        self.intro = self.soup.find('div', {'class': 'pv-text-details__left-panel'})
        self.name_loc = self.intro.find("h1")

        # Extracting the Name
        self.name = self.name_loc.get_text().strip()
        # strip() is used to remove any extra blank spaces

        self.works_at_loc = self.intro.find("div", {'class': 'text-body-medium'})

        # this gives us the HTML of the tag in which the Company Name or university is present
        self.works_at = self.works_at_loc.get_text().strip()

        self.intro2 = self.soup.find('div', {'class': 'pb2 pv-text-details__left-panel'})
        self.location_loc = self.intro2.find_all("span", {'class': 'text-body-small'})

        # Ectracting the Location
        self.location = self.location_loc[0].get_text().strip()
        database().connection()
        database().insert(self.name,self.location,self.works_at)
        return self.name,self.location,self.works_at


    def log(self,name,location,about,list):

        with open(r'C:\Users\F.Mahmoudi\Dropbox\My PC (F-MAHMOUDI)\Desktop\linkedinlog.log', 'a') as fp:
            input = {"Name": name, "Location":location,"about": about,"time":datetime.now()}
            fp.write(f"{input}\n")
            for item in list:
                # write each item on a new line
                item.update({"time":datetime.now()})
                fp.write("%s\n" % item)
            print('Done')
        fp.close()

    def my_page(self):
        self.src = self.driver.page_source
        self.soup = BeautifulSoup(self.src, 'lxml')
        self.intro = self.soup.find('div', {'feed-identity-module__actor-meta break-words'})
        self.name_loc = self.intro.find("a")
        x = str(self.intro).split('=')
        for i in x:
            if "/in/" in i:
                i=i[1:-4]
                url = i
                break
        mypage_url = f"https://www.linkedin.com/{url}"
        return self.Crawling(mypage_url)

if __name__ == "__main__":
    crawler_obj = Crawler()
    crawler_obj.Login()
    name,location,about = crawler_obj.my_page()
    list = crawler_obj.Conn_Crawling()
    crawler_obj.log(name,location,about,list)
    crawler_obj.driver.close()

