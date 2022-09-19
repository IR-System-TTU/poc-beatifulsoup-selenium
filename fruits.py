from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
import time
from constants import *

def get_free_proxies():
  url = 'https://free-proxy-list.net/'
  # request and grab content
  soup = bs(requests.get(url).content, 'html.parser')
  # to store proxies
  proxies = []
  for row in soup.find("table", class_='table table-striped table-bordered').find_all('tr')[1:]:
    tds = row.find_all('td')
    try:
      ip = tds[0].text.strip()
      port = tds[1].text.strip()
      proxies.append(str(ip) + ':' + str(port))
    except IndexError:
      continue

  return proxies

# url = 'http://httpbin.org/ip'
# proxies = get_free_proxies()

# for i in range(len(proxies)):
#   print("Request Number : " + str(i + 1))
#   proxy = proxies[i]

#   try:
#     response = requests.get(url, proxies= {'http': proxy, 'https': proxy})
#     print(response.json())
#   except:
#     # if the proxy Ip is pre occupied
#     print("Not available")

def find_products_fruits_walmart():
  #Find walmart products
  #Fruits

  print('WALMART\n\n')
  # print(get_free_proxies())

  option = webdriver.ChromeOptions() # see https://www.programmersought.com/article/30255594749/
  option.add_argument('disable-infobars')

  driver = webdriver.Chrome(chrome_options=option)
  driver.get("about:blank")
  driver.maximize_window()
  try:
    driver.get('https://www.walmart.com/browse/food/fresh-fruits/976759_976793_9756351?page=1')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(5)
    html = driver.execute_script("return document.body.innerHTML;")
    print("Scroll completed")
  except Exception as e:
      print(e)
  finally:
      driver.quit()   
      
  parsed_html = bs(html, "lxml")
  fruits_grid = parsed_html.find_all('div', class_='mb1 ph1 pa0-xl bb b--near-white w-25')

  # with open('result.html', 'w') as f: # use a helper html file to help you analyze the code and find what you are looking for 
  #   for fruit in fruits_grid:
  #     f.write(fruit.prettify())
  count = 0
  for fruit_card in fruits_grid:
    if (count == 0):
      try:
        count += 1
        product_detail_url = fruit_card.find('a')['href'].split("&")[-1] # get product url to append to base url
        product_detail_link = WALMART_BASE_URL + product_detail_url # get product detail url
        driver = webdriver.Chrome(chrome_options=option)
        driver.get("about:blank") #unica forma de obtener todo el html completo (comprobado)
        driver.maximize_window()
        try:
          driver.get(product_detail_link)
          driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
          time.sleep(5)
          html = driver.execute_script("return document.body.innerHTML;")
          print("Page displayed")
        except Exception as e:
            print(e)
        finally:
            driver.quit()   

        product_detail_html = bs(html, 'lxml')

        print('fetching data...')

        product_name = product_detail_html.find('h1', class_='f3 b lh-copy dark-gray mt1 mb2').text
        product_image = product_detail_html.find('img', class_='noselect db')['src']
        product_price_span = product_detail_html.find('span', attrs={'data-testid': 'price-wrap'})
        product_price_denomination = product_price_span.contents[0].text
        product_price = product_price_span.contents[1].text[1:] # just get the number not the denomination
        product_avg_price = product_detail_html.find('div', attrs={'data-testid': 'price-mobile'}).contents[2].text
        product_avg_price_desc = product_detail_html.find('div', attrs={'data-testid': 'price-mobile'}).contents[3].text

        product_details_block = product_detail_html.find_all('div', class_='dangerous-html mb3')
        product_details = product_details_block[0].p.text
        product_details_header = product_details_block[1].p.text
        product_details_header_body = product_details_block[1].ul

        product_specifications_block = product_detail_html.find_all('div', class_='expand-collapse-header')[1]
        # product_specifications_header = product_specifications_block

        print(product_name)
        print(product_image)
        print(product_price_denomination)
        print(product_price)
        print(product_avg_price)
        print(product_avg_price_desc)
        print(product_details)
        print(product_details_header)
        print(product_details_header_body)
        print(product_specifications_block)

        # with open('fruit_detail.html', 'w') as f:
        #   f.write(product_detail_html.prettify())
      except Exception as e:
        print(e)
      finally:
        print('done')

