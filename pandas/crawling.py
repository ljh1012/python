import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

ref_info = []
headers = {'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}
start_url = f'https://www.mdpi.com/2079-7737/1/1'
r_start_url = requests.get(start_url, headers=headers)
volume_list = BeautifulSoup(r_start_url.text,'html.parser')
volumes = volume_list.find('div', class_='journal-browser-volumes')
volumes = volumes.find_all('li', class_='side-menu-li')
print()
count = 14
for volume in volumes:
    count -= 1
    if count <8:
        break
    print(count)
    # if count < 8:        
    #     cur_vol_url = f'https://www.mdpi.com'+ volume.find('a')['href'] #volume_page
    #     r_cur_vol_url = requests.get(cur_vol_url, headers=headers)
    #     cur_vol_issues = BeautifulSoup(r_cur_vol_url.text,'html.parser')
    #     issues = cur_vol_issues.find_all('div', class_='ul-spaced')
    #     print(issues)
    #     # issues = issues.find_all('li')
    #     for issue in issues:
    #         cur_issue_url = f'https://www.mdpi.com'+ issue.find('a')['href'] #issue_page
    #         r_cur_issue_url = requests.get(cur_issue_url, headers=headers)
    #         cur_issue = BeautifulSoup(r_cur_issue_url.text,'html.parser')    
    #         articles = cur_issue.find_all('div', class_='article-content')
    #         for article in articles:
    #             article_url = f'https://www.mdpi.com'+ article.find('a', class_='title-link')['href'] #article_page
    #             r2 = requests.get(article_url, headers=headers)
    #             article_full = BeautifulSoup(r2.text,'html.parser')
    #             article_ref = article_full.find('ol', class_=['html-xxx', 'html-xx', 'html-x'])
    #             article_ref2 = article_ref.find_all('li')
    #             for ref in article_ref2:
    #                 ref_info.append(ref.text)
    if count >=8:
        cur_vol_url = f'https://www.mdpi.com'+ volume.find('a')['href'] 
        r_cur_vol_url = requests.get(cur_vol_url, headers=headers)
        cur_vol_issues = BeautifulSoup(r_cur_vol_url.text,'html.parser')
        issues = cur_vol_issues.find('div', id_='middle-column')
        print(issues)
        issues = issues.find_all('div', class_='issue_cover')    
        
        for issue in issues:
            cur_issue_url = f'https://www.mdpi.com'+ issue.find('a')['href'] 
            r_cur_issue_url = requests.get(cur_issue_url, headers=headers)
            cur_issue = BeautifulSoup(r_cur_issue_url.text,'html.parser')    
            articles = cur_issue.find_all('div', class_='article-content')
            for article in articles:
                article_url = f'https://www.mdpi.com'+ article.find('a', class_='title-link')['href'] 
                r2 = requests.get(article_url, headers=headers)
                article_full = BeautifulSoup(r2.text,'html.parser')
                article_ref = article_full.find('ol', class_=['html-xxx', 'html-xx', 'html-x'])
                article_ref2 = article_ref.find_all('li')
                
                for ref in article_ref2:
                    ref_info.append(ref.text)
