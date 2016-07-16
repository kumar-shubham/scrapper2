from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import json, operator,sys,time

categories = ["Consumer Electronics", "Jewelry", "Watches", "Health & Beauty"]
driver = webdriver.Firefox()
product = {}


def login():
    driver.get("https://login.aliexpress.com/buyer.htm")

    elem = driver.find_element_by_xpath("//a[contains(@href, 'http://thirdparty.aliexpress.com/login.htm?type=gg&tracelog=ws_gg_mainlogin')]")
    elem.click()

    driver.switch_to_window(driver.window_handles[-1])

    elem = driver.find_element_by_id("Email")
    elem.send_keys("kb4shubhamtest1")

    submit = driver.find_element_by_id("next")
    submit.click()

    time.sleep(2)
    elem = driver.find_element_by_id("Passwd")
    elem.send_keys("plmnkoijb")

    submit = driver.find_element_by_id("signIn")
    submit.click()
    time.sleep(10)
    driver.switch_to_window(driver.window_handles[0])


def execute():
    prod_limit = 100
    sub_cat_limit = 5
    count=-1
    for cat in categories:
        count += 1
        driver.get("http://www.aliexpress.com/")
        time.sleep(2)
        elem = None
        try:
            elem = driver.find_element_by_id("search-key")
            elem.send_keys("Hope You are enjoying the scraping :P  ..... ")
        except:
            time.sleep(2)
        try:
            elem = driver.find_element_by_xpath("//a[contains(text(),'" + categories[count] + "')]")
        except NoSuchElementException:
            print "sleeping for three seconds"
            time.sleep(2)
            elem = driver.find_element_by_xpath("//a[contains(text(),'" + categories[count] + "')]")
        elem.click()
        time.sleep(1)
        sub_links = []
        #print "count : " + str(count) 
        if count == 0:
            sub_links = driver.find_elements_by_xpath("//h2[@class='bc-big-row-title bc-nowrap-ellipsis']/a")
        elif count == 1 or count == 2:
            sub_links = driver.find_elements_by_xpath("//div[@class='bc-row-wrap']/a")
        elif count == 3:
            sub_links = driver.find_elements_by_xpath("//p[@class='bc-main-name bc-nowrap-ellipsis']/a")
        sub_link_dict = {}
        sub_link = []
        for link in sub_links:
            temp = link.get_attribute("href")
            if "http:" not in temp:
                temp = "http:" + temp
            sub_link.append(temp)

        sub_link_dict[categories[count]] = sub_link
        #print len(sub_link)
        c = 0
        prod_link_dict = {}
        prod_link = []
        sub_count = 0
        for link in sub_link:
            sub_count += 1
            c += 1
            if( c>sub_cat_limit):
                break
            driver.get(link)
            time.sleep(2)
            prod_elem = driver.find_elements_by_xpath("//a[@class=' product ' or @class='product ']")
            for plink in prod_elem:
                temp = plink.get_attribute("href")
                if "http:" not in temp:
                    temp = "http:" + temp
                prod_link.append(temp)
            prod_link_dict[categories[count]] = prod_link
            ctr = 0
            prod = {}
            size = prod_limit
            update_value = size*1.0/100
            divider = int(update_value+1)
            timer = 0
            for prod1 in prod_link:
                if timer % int(divider) == 0:
                    #print "s : " + str(size) + " uv : " + str(update_value) + " t/uv : " + str(int(timer/update_value)) + " :: " + str(count)
                    num = int(timer/(update_value*4*sub_cat_limit)) + 25*(sub_count-1)/sub_cat_limit +25*count
                    #print "a : " + str(int(timer/(update_value*4*sub_cat_limit))) + " b : " + str(25*(sub_count-1)/sub_cat_limit) + " c : " + str(25*count)
                    update_progress_bar(num)
                ctr += 1
                if ctr>prod_limit:
                    break
                driver.get(prod1)
                time.sleep(2)
                product_name = driver.find_element_by_xpath("//h1[@class='product-name']")
                if product_name is not None:
                    product_name = product_name.text
                rating = driver.find_element_by_xpath("//span[@class='percent-num']")
                if rating is not None:
                    rating = rating.text
                image = driver.find_element_by_xpath("//div[@class='ui-image-viewer-thumb-wrap']/a/img")
                if image is not None:
                    image = image.get_attribute('src')

                try:
                    price = driver.find_element_by_xpath("//span[@itemprop='lowPrice']" )
                except NoSuchElementException:
                    try:
                        price = driver.find_element_by_id("j-sku-discount-price")
                    except NoSuchElementException:
                        try:
                            price = driver.find_element_by_id("j-sku-price")
                        except NoSuchElementException:
                            price = None
                    
                if price is not None:
                    price  = price.text

                try:
                    desc = driver.find_element_by_css_selector("#j-product-description > div.ui-box-body > div > p:nth-child(2)")
                except NoSuchElementException:
                    desc = None
                if desc is not None:
                    desc = desc[0].text
                if desc is None or len(desc) < 30:
                    try:
                        desc = driver.find_element_by_css_selector("#j-product-description > div.ui-box-body > div > p:nth-child(3)")
                    except NoSuchElementException:
                        desc = None
                if desc is not None:
                    desc = desc.text

                try:
                    cat = driver.find_element_by_xpath("//a[contains(text(),'All Categories')]//following-sibling::a//following-sibling::a")
                    cat = cat.text
                except NoSuchElementException:
                    cat = None

                
                feedback_block = driver.find_element_by_css_selector("#feedback iframe")
                feedback_url = None
                if feedback_block is not None:
                    feedback_url = feedback_block.get_attribute("thesrc")
                feedbacks = []
                if feedback_url is not None and "http:" not in feedback_url:
                    feedback_url = "http:" + feedback_url
                    f = driver.get(feedback_url)
                    feedbacks = driver.find_elements_by_xpath("//div[@class='feedback-item clearfix']")
                feedback = []
                #print feedbacks
                for fb in feedbacks:
                    feed = {}
                    try:
                        user_name = fb.find_element_by_xpath(".//span[@class='user-name']")
                    except NoSuchElementException:
                        user_name = None
                    if user_name is not None:
                        user_name = user_name.text
                    try:
                        comment = fb.find_element_by_xpath(".//dt[@class='buyer-feedback']//following-sibling::span")
                    except NoSuchElementException:
                        comment = None
                    if comment is not None:
                        comment = comment.text
                    try:
                        times = fb.find_element_by_xpath(".//dd[@class='r-time']")
                    except NoSuchElementException:
                        times = None
                    if times is not None:
                        times = times.text
                    feed['user_name'] = user_name
                    feed['comment'] = comment
                    feed['time'] = times
                    feedback.append(feed)

                #print "  description   :: " + str(desc)
                #print "  prodduct name :: " + str(product_name)
                #print "  category      :: " + str(cat)
                #print "  rating        :: " + str(rating)
                #print "  price         :: " + str(price)
                #print "  image         :: " + str(image)
                prod['product_name'] = product_name
                prod['category'] = cat
                prod['image'] = image
                prod['price'] = price
                prod['rating'] = rating
                prod['description'] = desc
                prod['link'] = prod1
                prod['reviews'] = feedback

                if categories[count] not in product:
                    product[categories[count]] = [prod]
                else:
                    product[categories[count]].append(prod)
                timer += 1
    update_progress_bar(100)

def close():
    driver.close()

def update_progress_bar(num):
    percent = float(num) / 100
    bar_length = 50
    hashes = '#' * int(round(percent * bar_length))
    spaces = ' ' * (bar_length - len(hashes))
    sys.stdout.write("\rPercent Scraped: [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))))
    sys.stdout.flush()


if __name__ == "__main__":
    
    update_progress_bar(0)
    login()
    try:
        execute()
    except:
        close()
    for dicts in product:
        product[dicts] = sorted(product[dicts], key=operator.itemgetter('price'), reverse=True)    
    result = json.dumps(product)
    with open("product.json", "w+") as json_file:
        json_file.write(result)

    print ' Done!'
    print result


