# Insights-project

此project用於爬取網站，資料來源包含Dcard及Instagram

## 所需套件/其他檔案
- Packages:
selenium
pandas
datetime
requests
- Files:
chromedriver.exe (需與目前電腦所使用的版本相同，並放置於同一層)

## Dcard

此部分有兩個腳本, 分別為"Dcard.py"及"Dcard_sample.py". 前者為已經寫好並包成class的完整腳本, 後者則為用於展示如何使用Dcard.py

### Steps

1. 給定"topic"及"page_count" (page_count為想要搜索的頁面數)
2. 取得在Dcard討論特定主題中前n頁的貼文網址
3. 進入每個貼文並取得貼文相關資料
4. 將貼文資料存成兩個表格, 分別為overview及comment


### Classes 

|class_name|function|desc.|
|---|---|---|
|get_urls|open_incognito_driver|用webdriver開啟一個無痕視窗並縮小|
|get_urls|search_topic|搜尋給定之主題並下滑指定頁數|
|get_urls|get_url|抓取目前頁面上的所有url, 並篩選出文章的url|
|get_contents|find_title|抓取文章標題|
|get_contents|comment_extend|把留言都按出來|
|get_contents|find_time_like_comment_count|爬取發文日期, 愛心數及留言數|
|get_contents|find_content|爬取文章內容|
|get_contents|find_comment_and_likes|爬取文章中所有留言及各留言讚數|
|get_contents|get_content|整合所有爬取內容|
|get_contents|get_final_df|將爬取內容整理成兩個DataFrame並給每篇文章一個postid|


## Instagram

此部分有兩個腳本, 分別為"Instagram.py"及"Instagram_sample.py". 前者為已經寫好並包成class的完整腳本, 後者則為用於展示如何使用Instagram.py

### Steps

1. 給定"topic"(為欲搜索之hashtag), "page_count"(page_count為想要搜索的頁面數), username(optional), password(optional)
2. 登入Instagram主頁
3. 取得在Instagram使用特定標籤的公開貼文前n頁的貼文網址
4. 進入每個貼文並取得貼文相關資料
5. 將貼文資料存成表格, 並將發文者的頭貼存檔

### Classes

|class_name|function|desc.|
|---|---|---|
|login_process|open_incognito_driver|用webdriver開啟一個無痕視窗並縮小|
|login_process|login|登入Instagram主頁, 並點選記住密碼視窗中的Not Now|
|get_post_info|get_content|取得單篇貼文中的貼文資訊, 含發文者, 內容, 標籤及發文日期|
|get_post_info|save_images|將發文者的頭貼存入一個以搜尋標籤命名的文件夾|
|get_post_info|get_data|整合所有爬取行為|
|tag_search|get_url|使用標籤進行搜尋, 並產出相關公開貼文的網址|
