from firebase_admin import firestore
from utils import sanitise

COLLECTION = "auctions"
db = firestore.Client()

def add_auction(NFT_NAME, PRICE, HIGHEST_BIDDER, START_DATE, START_TIME, END_DATE, END_TIME, IMAGE_LINK):
    NFT_NAME = sanitise(NFT_NAME)
    try:
        db = firestore.Client()
        doc_ref = db.collection(COLLECTION).document(NFT_NAME)
        doc_ref.set({
            "nft_name" : NFT_NAME,
            "price": PRICE,
            "highest_bidder": HIGHEST_BIDDER,
            "start_date": START_DATE,
            "start_time": START_TIME,
            "end_date": END_DATE,
            "end_time": END_TIME,
            "image_link": IMAGE_LINK,
            "started": 0
            })
    except:
        return (0)
    return (1)

def get_auction(NFT_NAME):
    doc_ref = db.collection(COLLECTION).document(NFT_NAME)
    doc = doc_ref.get()
    if doc.exists:
        return(doc.to_dict())
    else:
        return (0)

def get_all_auctions():
    docs = db.collection(COLLECTION).stream()
    return (docs)

def update_auction_start(NFT_NAME, STARTED):
    try:
        auction_ref = db.collection(COLLECTION).document(NFT_NAME)
        auction_ref.update({'started': STARTED})
    except Exception as err:
        print(err)
        return (0)
    return (1)

def update_auction(NFT_NAME, PRICE, HIGHEST_BIDDER):
    try:
        auction_ref = db.collection(COLLECTION).document(NFT_NAME)
        auction_ref.update({'price': PRICE,
                                        'highest_bidder': HIGHEST_BIDDER,})
    except Exception as err:
        print(err)
        return (0)
    return (1)

def delete_auction(NFT_NAME):
    db.collection(COLLECTION).document(NFT_NAME).delete()
    return (1)