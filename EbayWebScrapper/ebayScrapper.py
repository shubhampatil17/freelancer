from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection as Finding
from ebaysdk.trading import Connection as Trading
from bs4 import BeautifulSoup
from openpyxl import Workbook
import datetime


class Scrapper:
    can_call_finding_api = True
    can_call_trading_api = True
    listing_count = 0

    api_request = {
        'itemFilter': [],

        'outputSelector': [
            'SellerInfo',
            'StoreInfo',
            'UnitPriceInfo'
        ],

        'paginationInput': {
            'pageNumber': '1'
        }
    }

    xl_header = [
        'Sequence Number',
        'Seller',
        'Seller Rating',
        'Ebay Item Number',
        'Item Description',
        'Price',
        'Postage',
        'Condition',
        'Link',
        'Category',
        'Sold',
        'Available'
    ]

    column_width = [0 for x in range(len(xl_header))]

    workbook = Workbook()
    worksheet = workbook.active

    def __init__(self, keywords, seller):
        self.set_keywords(keywords)
        self.add_to_filter('Seller', seller)

    def set_keywords(self, keywords):
        try:
            if keywords != '':
                self.api_request['keywords'] = keywords
            else:
                raise Exception('WARNING : Either Keyword or Seller not set.')
        except Exception as e:
            print e.message

    def add_to_filter(self, filter_name, filter_value):
        try:
            if filter_name != '' and filter_value != '':
                self.api_request['itemFilter'].append({
                    'name': filter_name,
                    'value': filter_value
                })
            else:
                raise Exception('WARNING : Either Keyword or Seller not set.')
        except Exception as e:
            print e.message

    def start_scraping(self):
        api = Finding(config_file = 'ebay.yaml', siteid = 'EBAY-AU')
        print 'INFO : Scrapping started.'

        if self.can_call_finding_api:
            self.write_to_XL(self.xl_header)

            try:
                response = api.execute('findItemsAdvanced', self.api_request)
                total_pages = int(response.dict()['paginationOutput']['totalPages'])

                print 'INFO : Total Number of Pages :', total_pages
                print 'INFO : Scraping Page 1',

                self.parse_response(response)

                for page_number in range(2, total_pages + 1):
                    self.api_request['paginationInput']['pageNumber'] = str(page_number)
                    response = api.execute('findItemsAdvanced', self.api_request)
                    print 'INFO : Scraping Page', page_number,
                    self.parse_response(response)

            except ConnectionError as e:
                self.can_call_finding_api = False
                print 'ERROR :', e.response.dict()

            self.workbook.save('ebay_' + str(datetime.datetime.today()) + '.xlsx')


    def parse_response(self, response):

        soup = BeautifulSoup(response.content, 'lxml')
        api = Trading(config_file='ebay.yaml', siteid=15)

        if soup.searchresult is not None:
            for item in soup.searchresult.find_all('item'):
                if item.find('sellingstate').string == 'Active':
                    self.listing_count = self.listing_count + 1

                    listing = []
                    listing.append(str(self.listing_count))

                    seller_user_name = item.find('sellerusername')
                    if seller_user_name is not None:
                        seller_user_name = seller_user_name.string

                    listing.append(unicode(seller_user_name))

                    feedback_score = item.find('feedbackscore')
                    if feedback_score is not None:
                        feedback_score = feedback_score.string

                    listing.append(unicode(feedback_score))

                    item_id = item.find('itemid')
                    if item_id is not None:
                        item_id = item_id.string

                    listing.append(unicode(item_id))

                    title = item.find('title')
                    if title is not None:
                        title = title.string

                    listing.append(unicode(title))

                    current_price = item.find('currentprice')
                    if current_price is not None:
                        current_price = current_price.get('currencyid') + ' ' + current_price.string

                    listing.append(unicode(current_price))

                    shipping_cost = item.find('shippingservicecost')
                    if shipping_cost is not None:
                        shipping_cost = shipping_cost.get('currencyid') + ' ' + shipping_cost.string

                    listing.append(unicode(shipping_cost))

                    condition = item.find('conditiondisplayname')
                    if condition is not None:
                        condition = condition.string

                    listing.append(unicode(condition))

                    item_url = item.find('viewitemurl')
                    if item_url is not None:
                        item_url = item_url.string

                    listing.append(unicode(item_url))

                    category_name = item.find('categoryname')
                    if category_name is not None:
                        category_name = category_name.string

                    listing.append(unicode(category_name))

                    if self.can_call_trading_api:
                        try:
                            trading_api_response = api.execute('GetItem', {
                                'ItemID': item.find('itemid').string,
                                'IncludeWatchCount': True,
                                'OutputSelector': [
                                    'SellingStatus',
                                    'QuantityAvailableHint',
                                    'QuantityThreshold'
                                ]
                            })

                            trading_soup = BeautifulSoup(trading_api_response.content, 'lxml')

                            quantity_sold = trading_soup.find('quantitysold')
                            if quantity_sold is not None:
                                quantity_sold = quantity_sold.string

                            listing.append(unicode(quantity_sold))

                            quanity_available = trading_soup.find('quantityavailablehint')
                            if quanity_available is not None:
                                quanity_available = quanity_available.string

                            threshold = trading_soup.find('quantitythreshold')
                            if threshold is not None:
                                threshold = threshold.string
                                quanity_available = unicode(quanity_available) + unicode(threshold)

                            listing.append(quanity_available)

                        except ConnectionError as e:
                            self.can_call_trading_api = False
                            print e.response.dict()

                    self.write_to_XL(listing)
            print '(Done)'

        else:
            print '(Not allowed)'

    def write_to_XL(self, listing):
        self.worksheet.append(listing)

        for item in listing:
            index = listing.index(item)
            if item is not None:
                if len(item) >  self.column_width[index]:
                    self.column_width[index] = len(item)
                    self.worksheet.column_dimensions[str(list(self.worksheet.columns)[index][0].column)].width = len(item) + 10

    def dump(self, api):
        if api.warnings():
            print "WARNINGS : ", api.warnings()

        print "Response code: ",api.response_code()


def print_usage():
    print 'Usage:'
    print 'KEYWORDS EXAMPLES'
    print 'baseball card    :   Returns Items with both the words "baseball" and "card".'
    print 'baseball,card    :   Returns Items with the exact phrase "baseball card" in the title. This is equivalent to specifying the keywords, separated by spaces, in order within quotation marks (e.g., "baseball card").'
    print '(baseball,card)  :   Returns Items with either the word "baseball" or the word "card" in the title.'
    print '"baseball card"  :   Returns Items with the exact phrase "baseball card" in the title.'
    print 'baseball -autograph  :   Returns Items that have the word "baseball" but not "autograph".'
    print 'baseball -(autograph,card,star)  :   Returns Items with the word "baseball" but not "autograph," "card," or "star".'
    print '@1 baseball autograph card   : Returns Items with two of the three words "baseball," "autograph," and "card". For a "3 out of 4" search, use @2 and a list of four words.'
    print '@1 baseball autograph card +star :   Returns Items with any two of the three words "baseball," "autograph," or "card" in the title plus the word "star".'

if __name__ == "__main__":
    print_usage()
    keywords = raw_input("Enter KEYWORDS :")
    seller = raw_input("Enter SELLER :")
    Scrapper(keywords, seller).start_scraping()
