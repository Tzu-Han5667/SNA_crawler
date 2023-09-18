from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
from datetime import datetime
import os
from random import randrange
import requests

class login_process:
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def open_incognito_driver(self):
        opts = Options()
        opts.add_argument("--incognito")
        driver = webdriver.Chrome(options=opts)
        driver.minimize_window()
        return driver
    
    def login(self, driver):
        driver.get('https://www.instagram.com/')
        time.sleep(3)
        driver.find_element_by_xpath("//input[@name='username'][@type='text']").send_keys(self.username) #input_account
        driver.find_element_by_xpath("//input[@name='password'][@type='password']").send_keys(self.password) #input_password
        driver.find_element_by_xpath("//button[@type='submit']").click() #login_buttom
        time.sleep(5)
        notnow = driver.find_element_by_xpath("//button[contains(text(),'Not Now')]")
        notnow.click()
            
    def main(self):
        driver = self.open_incognito_driver()
        self.login(driver)
        return driver

class get_post_info:
    def __init__(self, topic, posts):
        self.topic = topic
        self.posts = posts

    def get_content(self, driver):
        name = driver.find_element_by_xpath("//div[@class='e1e1d']").text
        container = driver.find_element_by_xpath("//div[@class='C4VMK']").text.replace(name+'\n','')
        period = container.split('\n')
        period = period[len(period)-1]
        content = container.split('#')[0]
        hashtags = [i.replace('\n','').replace(period,'').replace(' ','') for i in container.split('#')[1:]]
        date = driver.find_element_by_xpath('//time').get_attribute('title')
        date = datetime.strptime(date, '%b %d, %Y').date()
        return [name, content, hashtags, date]
    
    def save_images(self, name, driver):
        link = driver.find_element_by_xpath('//img[@class="_6q-tv"]').get_attribute('src')
        img = requests.get(link) 
        directory = "images_"+self.topic
        if directory not in os.listdir():
            os.mkdir(directory)
        else:
            pass
        with open("images_"+self.topic+"\\" + name + ".jpg", "wb") as file: 
            file.write(img.content) 
    
    def get_data(self, driver):
        data_arr= []
        for p in self.posts:
            driver.get(p)
            time.sleep(3)
            try:
                res = self.get_content(driver)
                data_arr.append(res)
                self.save_images(res[0], driver)
            except:
                pass
        data_df = pd.DataFrame([data_arr], columns=['name', 'content', 'hashtags', 'date'])
        return data_df
    
    def main(self, driver):
        data_df = self.get_data(driver)
        driver.quit()
        return data_df

class tag_search:
    def __init__(self, tag, page_count):
        self.tag = tag
        self.page_count = page_count
            
    def get_url(self, driver):
        driver.get('https://www.instagram.com/explore/tags/'+self.tag+'/')
        posts = []
        for n in range(self.page_count):
            links = driver.find_elements_by_xpath('//a')
            posts.extend([link.get_attribute('href') for link in links if '/p/' in link.get_attribute('href')])
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            time.sleep(randrange(5))
        posts = list(dict.fromkeys(posts))
        return posts
        
    def main(self, username, password):
        driver = login_process(username, password).main()
        posts = self.get_url(driver)
        data_df = get_post_info(self.tag, posts).main(driver)
        return data_df
    
