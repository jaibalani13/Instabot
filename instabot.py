from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time, datetime
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
        for i in range(1, 3):
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
            print("time: %s" % datetime.datetime.now())
            driver.get(pic_href)
            time.sleep(2)
            try:
                time.sleep(random.randint(2, 4))
                try:
                    driver.find_element_by_xpath("//*[@aria-label='Like']")
                except (NoSuchElementException, ValueError) as e:
                    print("Already liked")
                    continue
                try:
                    likes = driver.find_element_by_xpath(
                        '//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/section[2]/div/div/button/span')
                    if int(likes.text) > 20:
                        print(">20 likes")
                        continue
                except (NoSuchElementException, ValueError) as e:
                    print("Likes not found")
                    continue
                driver.find_element_by_xpath("//*[@aria-label='Like']").click()
                self.photos_liked += 1
                if self.photos_liked % 25 == 0:
                    print("Sleeping")
                    time.sleep(60*30)
                print("liked: %s" % self.photos_liked)
                time.sleep(20)

            except Exception as e:
                print(e)
                time.sleep(2)
            unique_photos -= 1

if __name__ == "__main__":

    username = "stocksadvisor"
    password = "Piyujai#1"

    ig = InstaBot(username, password)
    ig.login()

    hashtags = ['stockmarket',
                'trading', 'stockmarketnews', 'bse', 'stocks', 'banknifty', 'stockmarketindia', 'nifty', 'sensex', 'intraday', 'finance',
                'intradaytrading', 'indiansharemarket', 'investor', 'dalalstreet', 'niftyfifty',
                'warrenbuffet', 'sharemarkettips', 'bigprofits', 'billionaire', 'binaryoptions', 'bsesensex',
                'business', 'candlesticks', 'coronav', 'cryptocurrency', 'dalalstreet2020', 'daytrader', 'daytrading',
                'earnfromhome', 'economy', 'entrepreneur', 'entrepreneurship', 'equity', 'equitymarket', 'financeblogs',
                'financial', 'financialadvice', 'financialcourse', 'financialeducation', 'financialfreedom',
                'financiallearning', 'financialliteracy', 'financialmarket', 'financialmarketlearning',
                'financialmarkets', 'followbackinstantly', 'followers', 'followforfollowback', 'forex',
                'forexlifestyle', 'forexsignals', 'forextrader', 'forextrading', 'fundamentalanalysis',
                'futuresandoptions', 'indiafightscorona', 'indianstock', 'indianstockadvisor', 'indianstockexchange',
                'instagram', 'intradaytrader', 'invest', 'laptopincome', 'laptopmoney', 'learning', 'lifestyle',
                'makemoneyonline', 'marketcap', 'marketnews', 'mcx', 'millionaire',
                'millionairebyage', 'nationalstockexchange', 'nifty50', 'niftygenius', 'nseindia',
                'nsemumbai', 'nyse', 'onlinejobsworkfromhome', 'options', 'optionstrading', 'optiontrader',
                'pricepatterns', 'profit', 'radhakishandamani', 'rakeshjhunjhunwala', 'rakeshjunjunwala',
                'sanbun', 'sensexindia', 'sensextoday', 'stockanalytics', 'stockedge',
                'stockedgekarosmartinvestorbano', 'stockexchange', 'stockmarketeducation', 'StockMarketIndia',
                'stockmarketinvesting', 'stockmarketmemes', 'stockmarketquotes', 'stockmarkets', 'stockresearch',
                'stocktrader', 'swingtrading', 'technicalanalysis', 'trader', 'traderslife📈📉',
                'tradingforex', 'tradingstocks', 'vijaykedia', 'wallstreet', 'warrenbuffett',
                'zerodha']

    while True:
        hashtag = random.choice(hashtags)
        try:
            ig.like_photos_of_hashtag(hashtag)
            time.sleep(30 * 60)
        except Exception:
            ig.closeBrowser()
            time.sleep(30*60)
            ig = InstaBot(username, password)
            ig.login()
            ig.like_photos_of_hashtag(hashtag)
