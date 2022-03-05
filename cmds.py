from discord.ext import commands
import messages
from utils import get_authorised_users, now, tz, AUCTION_ROLES, INCREMENT_AMOUNT
from datetime import datetime
import database
import api_firestore

def is_authorised_channel(message):
	if (message.channel.name.startswith("auction-")):
		return (1)
	return (0)

def is_authorised_user(message):
  roles = message.author.roles
  for role in roles:
    if role.id in AUCTION_ROLES:
      return (1)
  return (0)

def is_exception_channel(message):
  if ("goat" in message.channel.name):
    return (1)
  return (0)

def error_check_create(message, *args):
	args = args[0]
	if (str(message.author) not in get_authorised_users()):
		return ("Unathorised User")
	if (len(args) != 7):
		return ("Wrong number of arguements")
	nft_name = args[0]
	auction_price = args[1]
	auction_st_date = args[2]
	auction_st_time = args[3]
	auction_end_date = args[4]
	auction_end_time = args[5]
	auction_image = args[6]
	#checking price
	try :
		auction_price = int(auction_price)
	except :
		return ("Initial price is not a number")

#checking dates
	try :
		start_date = f"{auction_st_date} {auction_st_time}"
		start_date_obj = datetime.strptime(start_date, "%d/%m/%y %H:%M").replace(tzinfo=tz)
	except :
		return ("Error setting start date")
	try :
		end_date = f"{auction_end_date} {auction_end_time}"
		end_date_obj = datetime.strptime(end_date, "%d/%m/%y %H:%M").replace(tzinfo=tz)
	except :
		return ("Error setting end date")
	if (start_date_obj > end_date_obj):
		return ("Start date and time must be before end date")
	if (now() > start_date_obj):
		return (f"Start date and time must be at least 1 minute later than current time. Timezone {tz}")

	status = api_firestore.get_auction(nft_name)
	if (status != 0):
			return (f"Invalid nft_name, auction already on going")
	
	return ({"nft_name":nft_name, "starting_price":auction_price, "start_date":auction_st_date, "start_time":auction_st_time, "end_date":auction_end_date, "end_time":auction_end_time, "image":auction_image})

def auction_ended(auction):
  time = str(messages.get_remaining_time(auction))
  if time.startswith("-"):
    return (1)
  return (0)
  

class general_commands(commands.Cog):
  @commands.command()
  async def create(self, message, *args):
    if (str(message.author) not in get_authorised_users()):
      await message.reply("Only admins may use this command!")
      return
    result = error_check_create(message, args)
    if (type(result) == dict):
      database.create_auction(result["nft_name"], result["starting_price"], "",result["start_date"], result["start_time"], result["end_date"], result["end_time"], result["image"])
      await (message.channel.send(embed=messages.create_new(result)))
    else:
      await message.send(result)
      await message.send(embed=messages.create_usage_example())

  @commands.command()
  async def cancel(self, message, *args):
    if (str(message.author) not in get_authorised_users()):
      await message.reply("Only admins may use this command!")
      return
    if (len(args) < 1):
      await message.channel.send("No auction name given to cancel")
      return
    nft_name = args[0]
    status = api_firestore.delete_auction(nft_name)
    await message.channel.send(f"Auction for {nft_name} has been cancelled")

  @commands.command()
  async def bid(self, message, *args):
    if (is_authorised_channel(message) == 0):
      await message.reply("Please use me in the `#auctions` channel")
      return
    if (is_authorised_user(message) == 0 and not is_exception_channel(message)):
      await message.reply("You need to have a holder role in order to bet!")
      return
    nft_name = message.channel.name.replace("auction-","")
    auction = api_firestore.get_auction(nft_name)
    if (auction_ended(auction)):
      await message.reply("Sorry, no more bids, auction has ended!")
      return
    if (auction["highest_bidder"] == ""):
      status = api_firestore.update_auction(auction["nft_name"], int(auction["price"]), message.author.name)
    else:
      status = api_firestore.update_auction(auction["nft_name"], int(auction["price"]) + INCREMENT_AMOUNT, message.author.name)
    if (status == 1):
      await message.channel.send(embed=messages.success_bet(message, auction["nft_name"], int(auction["price"]) + INCREMENT_AMOUNT))
    else:
      await message.channel.send("My oh my, something went wrong when placing the bet!")

  @commands.command()
  async def show(self, message, *args):
    auctions = api_firestore.get_all_auctions()
    count = 0
    for auction in auctions:
      await message.channel.send(f"{auction.to_dict()['nft_name']}")
      count += 1
    if (count == 0):
      await message.channel.send(f"No current auctions!")

