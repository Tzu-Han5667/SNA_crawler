from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import uuid
from datetime import datetime
from selenium.webdriver.common.keys import Keys
import pandas as pd

class get_urls:
    def __init__(self, topic, page_count):
        self.topic = topic
        self.page_count = page_count
    
    def open_incognito_driver(self):
        opts = Options()
        opts.add_argument("--incognito")
        driver = webdriver.Chrome(options=opts)
        driver.minimize_window()
        return driver
    
    def search_topic(self, driver):
        driver.get('https://tw.observer/') #開啟深卡
        search_bar = driver.find_element_by_xpath('//input[@placeholder="搜尋線上文章"]')
        search_bar.send_keys('#%s'%self.topic) #搜尋主題
        search_button = driver.find_element_by_xpath('//span[@class="search-button"]')
        search_button.click()
        
        for i in range(self.page_count): #下滑指定頁數
            driver.execute_script("return document.body.scrollHeight")
            time.sleep(1)
            driver.find_element_by_tag_name('body').send_keys(Keys.END)
    
    def get_url(self, driver):
        url = []
        for i in driver.find_elements_by_xpath('//a'):
            if '/tw.observer/p/' in i.get_attribute('href'):
                url.append(i.get_attribute('href'))
        return url
    
    def main(self):
        driver = self.open_incognito_driver()
        self.search_topic(driver)
        url = self.get_url(driver)
        driver.quit()
        return url

class get_contents:
    def __init__(self, url):
        self.url = url
    
    def find_title(slef, driver):
        title = driver.find_element_by_xpath('//article/h1/span').text
        return title
        
    def comment_extend(self, driver):
        for i in driver.find_elements_by_xpath('//div[@class="comment unextend"]'):
            i.click()
            time.sleep(1)
        
    def find_time_like_comment_count(self, driver):
        ele = driver.find_element_by_xpath('//article').text.split('\n')[4]
        like_count = ele.split('favorite_border')[1].split(' ')[0]
        comment_count = ele.split('toc')[1].split(' ')[0]
        times = datetime.strptime('2021/'+ele.split('favorite_border')[0].strip(), "%Y/%m/%d %H:%M")
        return like_count, comment_count, times
    
    def find_content(self, driver, like_count, comment_count):
        ele = driver.find_element_by_xpath('//div[@class="body"]').text.split('\nfavorite_border'+like_count+' toc'+comment_count+'\n')
        ele = ele[len(ele)-1].split('\n')
        content = driver.find_element_by_xpath('//div[@class="body"]').text.split('\nfavorite_border'+like_count+' toc'+comment_count+'\n')[0]
        return content
    
    def find_comment_and_likes(self, driver, like_count, comment_count):
        ele = driver.find_element_by_xpath('//div[@class="body"]').text.split('\nfavorite_border'+like_count+' toc'+comment_count+'\n')[1]
        comment = []
        comment_like = []
        for i in ele.split('\nB'):
            i = i.split(':')
            c = i[len(i)-1].replace('\n',' ')
            comment.append(c)
            if 'favorite' in i[0]:
                txt = i[0].split(' / ')[2].replace('favorite_border','')
                cl = [int(s) for s in txt.split() if s.isdigit()][0]
                comment_like.append(cl)
            else:
                comment_like.append(cl)
        comment = [i.replace(' ','') for i in comment]
        comment_dict = dict(zip(comment, comment_like))
        return comment_dict
    
    def get_content(self, driver):
        title = self.find_title(driver)
        time.sleep(2)
        self.comment_extend(driver)
        like_count, comment_count, times = self.find_time_like_comment_count(driver)
        time.sleep(2)
        content = self.find_content(driver, like_count, comment_count)
        comment_dict = self.find_comment_and_likes(driver, like_count, comment_count)
        overview = [title, content, like_count, comment_count, times]
        comment = [list(comment_dict.keys()), list(comment_dict.values())]
        return overview, comment

    def get_final_df(self, overview, comment):
        overview_df = pd.DataFrame(dict(zip(['title', 'content', 'like_count', 'comment_count', 'times'], overview)), index=[0])
        comment_df = pd.DataFrame(dict(zip(['comments', 'comment_like'], comment)))
        uid = str(uuid.uuid4())[0:8]
        overview_df['postId'] = comment_df['postId'] = uid
        return overview_df, comment_df
    
    def main(self):
        fin_overview = fin_comment = pd.DataFrame()
        for u in self.url:
            driver = get_urls(0, 0).open_incognito_driver()
            driver.get(u)
            overview, comment = self.get_content(driver)
            overview_df, comment_df = self.get_final_df(overview, comment)
            fin_overview = pd.concat([fin_overview, overview_df], axis=0).reset_index(drop=True)
            fin_comment = pd.concat([fin_comment, comment_df], axis=0).reset_index(drop=True)
            driver.quit()
        return fin_overview, fin_comment
