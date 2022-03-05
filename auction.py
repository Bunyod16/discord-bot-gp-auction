import messages
from utils import tz, now, INCREMENT_AMOUNT
from datetime import datetime
import api_firestore

def get_auction_info(nft_name):
    info = api_firestore.get_auction(nft_name)
    return (info)