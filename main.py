import time
from fruits import *

if __name__ == '__main__':
  while True:
    print('scraping for fruits')
    find_products_fruits_walmart()
    time_wait = 1440
    print(f'Waiting {time_wait} minutes...')
    time.sleep(time_wait * 60) #run program every day\