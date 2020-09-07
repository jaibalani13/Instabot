from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import random

class InstaBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome()
        self.photos_liked = 0

    def closeBrowser(self):
        self.driver.close()

    def login(self):
        driver = self.driver
        driver.get("https://www.instagram.com/")
        time.sleep(2)
        user_name_elem = driver.find_element_by_xpath("//input[@name='username']")
        user_name_elem.clear()
        user_name_elem.send_keys(self.username)
        passworword_elem = driver.find_element_by_xpath("//input[@name='password']")
        passworword_elem.clear()
        passworword_elem.send_keys(self.password)
        passworword_elem.send_keys(Keys.RETURN)
        time.sleep(5)


    def like_photos_of_hashtag(self, hashtag):
        driver = self.driver
        print("Hashtag: %s" % hashtag)
        driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        time.sleep(2)

        # gathering photos
        pic_hrefs = []
        for i in range(1, 10):
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                # get tags
                hrefs_in_view = driver.find_elements_by_tag_name('a')
                # finding relevant hrefs
                hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                                 if '.com/p/' in elem.get_attribute('href')]
                # building list of unique photos
                [pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]
                # print("Check: pic href length " + str(len(pic_hrefs)))
            except Exception:
                continue

        # Liking photos
        print(pic_hrefs)
        unique_photos = len(pic_hrefs)
        for pic_href in pic_hrefs:
            driver.get(pic_href)
            time.sleep(2)
            try:
                time.sleep(random.randint(2, 4))
                try:
                    driver.find_element_by_xpath("//*[@aria-label='Like']")
                    likes = driver.find_element_by_xpath(
                        '//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/section[2]/div/div/button/span')
                    if int(likes.text) > 10:
                        print(">10 likes")
                        continue
                except (NoSuchElementException, ValueError) as e:
                    print("Already liked")
                    continue
                driver.find_element_by_xpath("//*[@aria-label='Like']").click()
                self.photos_liked += 1
                if self.photos_liked % 50 == 0:
                    print("Sleeping")
                    time.sleep(60*30)
                print("liked: %s" % self.photos_liked)
                time.sleep(18)

            except Exception as e:
                print(e)
                time.sleep(2)
            unique_photos -= 1

if __name__ == "__main__":

    username = "USERNAME"
    password = "PASSWORD"

    ig = InstaBot(username, password)
    ig.login()

    hashtags = ['stockmarket',
                'trading', 'stockmarketnews', 'bse', 'stocks', 'banknifty', 'stockmarketindia', 'nifty', 'sensex', 'intraday', 'finance',
                'intradaytrading', 'indiansharemarket', 'money', 'investor', 'india', 'dalalstreet', 'niftyfifty',
                'warrenbuffet', 'sharemarkettips', 'bigprofits', 'billionaire', 'binaryoptions', 'bitcoin', 'bsesensex',
                'business', 'candlesticks', 'coronav', 'cryptocurrency', 'dalalstreet2020', 'daytrader', 'daytrading',
                'earnfromhome', 'economy', 'entrepreneur', 'entrepreneurship', 'equity', 'equitymarket', 'financeblogs',
                'financial', 'financialadvice', 'financialcourse', 'financialeducation', 'financialfreedom',
                'financiallearning', 'financialliteracy', 'financialmarket', 'financialmarketlearning',
                'financialmarkets', 'followbackinstantly', 'followers', 'followforfollowback', 'forex',
                'forexlifestyle', 'forexsignals', 'forextrader', 'forextrading', 'freedom', 'fundamentalanalysis',
                'futuresandoptions', 'indiafightscorona', 'indianstock', 'indianstockadvisor', 'indianstockexchange',
                'instagram', 'intradaytrader', 'invest', 'laptopincome', 'laptopmoney', 'learning', 'lifestyle',
                'makemoneyonline', 'market', 'marketcap', 'marketnews', 'markets', 'mcx', 'millionaire',
                'millionairebyage', 'motivation', 'nationalstockexchange', 'nifty50', 'niftygenius', 'ns10', 'nseindia',
                'nsemumbai', 'nyse', 'onlinejobsworkfromhome', 'options', 'optionstrading', 'optiontrader',
                'pricepatterns', 'profit', 'radhakishandamani', 'rakeshjhunjhunwala', 'rakeshjunjunwala', 'richest',
                'sanbun', 'sensexindia', 'sensextoday', 'share', 'stockanalytics', 'stockedge',
                'stockedgekarosmartinvestorbano', 'stockexchange', 'stockmarketeducation', 'StockMarketIndia',
                'stockmarketinvesting', 'stockmarketmemes', 'stockmarketquotes', 'stockmarkets', 'stockresearch',
                'stocktrader', 'success', 'swingtrading', 'technicalanalysis', 'trade', 'trader', 'traderslife📈📉',
                'tradingforex', 'tradingstocks', 'vijaykedia', 'wallstreet', 'warrenbuffett', 'wealth', 'work',
                'zerodha']

    for hashtag in hashtags:
        try:
            ig.like_photos_of_hashtag(hashtag)
            time.sleep(30 * 60)
        except Exception:
            ig.closeBrowser()
            time.sleep(30*60)
            ig = InstaBot(username, password)
            ig.login()
            ig.like_photos_of_hashtag(hashtag)
