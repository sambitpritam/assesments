import sys
import requests
from bs4 import BeautifulSoup

url_kw = 'http://www.shopping.com/products?KW=<keyword>'
url_pnkw = 'http://www.shopping.com/products~PG-<number>?KW=<keyword>"'

def get_result(keyword):
    new_url = url_kw.replace('<keyword>', keyword)
    required_no = 0
    str_no = ''
    req = requests.get(new_url)
    source_code = BeautifulSoup(req.content, 'html.parser')

    #   Getting data from the numTotalResult section that will display the number of results being displayed in the current page out of total result.
    try:
        links = source_code.find_all('span', {'class': 'numTotalResults'})
        if links:
            for eachLink in links:
                str_no = eachLink.text

            str_list = str_no.split(' ')
            final_no = str_list[len(str_list) - 1].replace('\n', '')

            if '+' in final_no:
                required_no = int(final_no.replace('+', ''))
            else:
                required_no = int(final_no)

        else:
            required_no = 0

    except:
        print('Error: Error while retriving the data')

    return required_no

def get_result_on_page(keyword, page_no):
    url_tmp = url_pnkw.replace('<number>', page_no)
    url = url_tmp.replace('<keyword>', keyword)

    new_req = requests.get(url)
    soup2 = BeautifulSoup(new_req.content, 'html.parser')

    #   Find the total number of product displayed in the result for the search keyword and page number... If either of them is wrong, the result will be zero.
    list_of_items = soup2.find_all('a', {'class': 'productName'})

    return len(list_of_items)

if __name__ == '__main__':
    args = list()

    if len(sys.argv) == 2:
        for i in range(len(sys.argv)):
            args.append(sys.argv[i])
        print(get_result(args[1]))
    elif len(sys.argv) == 3:
        for i in range(len(sys.argv)):
            args.append(sys.argv[i])
        try:
            print(get_result_on_page(args[2], args[1]))
        except:
            print('Error: invalid args')

#
# # To read a keyword from the entire web site
# def read_all(keyword, soup):
#     count = 0
#     word_list = list()
#
#     # get all the links from the home page
#
#     return count
#
#
# # Reading the cmd line arguments
# args = []
# url = ''
# keyword = ''
# page_no = 0
# for eachArg in sys.argv:
#     args.append(eachArg)
#
# if len(sys.argv) == 2:
#     # read from the entire website
#     keyword = args[1]
# elif len(sys.argv) == 3:
#     url = args[1]
#     page_no = args[2]
# else:
#     print('Error: atleast a keyword or a Keyword and a page number is expected')
#     break
#
#
# url = 'http://www.shopping.com/car-audio-and-video-accessories/car-audio-and-video/products~PG-2?KW=car+audio+and+video'
#
# r = requests.get(url)
# soup = BeautifulSoup(r.content)
#
# links = soup.find_all('span', {'class': 'newMerchantName'})
#
# for link in links:
#     print(link.text)
# print(links['value'])
#
#
#
#
