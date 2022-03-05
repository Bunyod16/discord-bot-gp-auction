import api_firestore

def sanitise(string):
    return (str(string).replace(";",""))

def create_auction(NFT_NAME, PRICE, HIGHEST_BIDDER, START_DATE, START_TIME, END_DATE, END_TIME, IMAGE_LINK):
    NFT_NAME = sanitise(NFT_NAME)
    PRICE = sanitise(PRICE)
    HIGHEST_BIDDER = sanitise(HIGHEST_BIDDER)
    START_DATE = sanitise(START_DATE)
    START_TIME = sanitise(START_TIME)
    END_DATE = sanitise(END_DATE)
    END_TIME = sanitise(END_TIME)
    IMAGE_LINK = sanitise(IMAGE_LINK)
    status = api_firestore.add_auction(NFT_NAME, PRICE, HIGHEST_BIDDER, START_DATE, START_TIME, END_DATE, END_TIME, IMAGE_LINK)
    return (status)

def update_auction_price(NFT_NAME, PRICE, HIGHEST_BIDDER):
    NFT_NAME= sanitise(NFT_NAME)
    PRICE= sanitise(PRICE)
    HIGHEST_BIDDER= sanitise(HIGHEST_BIDDER)
    status = api_firestore.update(NFT_NAME, PRICE, HIGHEST_BIDDER)
    return (status)