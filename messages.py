import discord
from utils import INCREMENT_AMOUNT, tzstr, now, tz, PR, POPULAR_LAB_ICON_URL
import auction
import api_firestore
from datetime import datetime

def get_help_message():
	title = "Ugly Bargainer's abilities"
	description = ""
	fields = [
		{"name":f"{PR}show", "description":"Shows information about current auctions."},
		{"name":f"{PR}bid", "description":f"Bid for an NFT, {INCREMENT_AMOUNT} ADA higher than the previous bidder."},
		{"name":f"{PR}create <nft_name> <initial_price> <start_date> <start_time> <end_date> <end_time> <image_link>", "description":"Creates a new auction."},
		{"name":f"{PR}cancel <nft_name>", "description":"Cancel an auction."},
		{"name":f"{PR}help", "description":"Sends a list of commands."}
	]
	message_help = discord.Embed(title=title, description=description, color=0x00ff00)
	for field in fields:
		message_help.add_field(name=field["name"], value=field["description"], inline=False)
	return (message_help)

def create_usage_example():
	title = "Example of !create"
	description = f"""{PR}create <nft_name> <initial_price> <start_date> <start_time> <end_date> <end_time> <image_link>
	{PR}create new_ugly 1000 24/01/22 10:00 24/01/22 14:00 https://media1.tenor.com/images/5d8f1a60f3e5e0e66b2079f312a9ee32/tenor.gif?itemid=24630514"""
	message_help = discord.Embed(title=title, description=description, color=0x00ff00)
	return (message_help)

def get_auction_info(nft_name):
	title = nft_name
	auction = api_firestore.get_auction(nft_name)
	if (auction == 0):
		return (discord.Embed(title="What?", description="I dont remember having such auctions", color=0x00ff00))
	if (auction != 0):
		fields = [{"name":"Highest Bid", "description": f"**{auction['price']} ADA** by **{auction['highest_bidder']}**"},
						{"name":"Start date", "description":f"{auction['start_date']}, {auction['start_time']}, {tzstr}"},
						{"name":"End date", "description":f"{auction['end_date']}, {auction['end_time']}, {tzstr}"}
						]
	message = discord.Embed(title=title, description="", color=0x00ff00)
	message.set_image(url=auction["image_link"])
	for field in fields:
		message.add_field(name=field["name"], value=field["description"], inline=False)
	return (message)

def fail_bet(message, nft_name, bet_amount):
	title = "I refuse your offer"
	description = f"Your bid for **{nft_name}** failed"
	message = discord.Embed(title=title, description=description, color=0x00ff00)
	return (message)

def get_remaining_time(info):
	current_time = now()
	auction_time = datetime.strptime(
			f"{info['end_date']} {info['end_time']}",
			"%d/%m/%y %H:%M").replace(tzinfo=tz)
	time_left = str(auction_time - current_time)
	time_left = time_left.replace("days,", "d, ", 1)
	time_left = time_left.replace(":", "h, ", 1)
	time_left = time_left.replace(":", "m, ", 1)
	time_left = time_left[:-7]
	time_left = time_left + "s."
	return (time_left)

def success_bet(message, nft_name, bet_amount):
	title = f"New bid leader for **{nft_name}**!"
	info = api_firestore.get_auction(nft_name)
	time_left = get_remaining_time(info)
	fields = [{"name":"Bid Leader", "description": f"{message.author}"},
				  {"name":"Top Bid", "description": f"{info['price']} ADA"},
				  {"name":"Time remaining", "description": f"{time_left}"}]
	message = discord.Embed(title=title, description="", color=0x00ff00)
	img_link = auction.get_auction_info(nft_name)["image_link"]
	message.set_image(url=img_link)
	for field in fields:
		message.add_field(name=field["name"], value=field["description"], inline=True)
	return (message)

def create_new(result):
	title = "A new auction has been created"
	fields = [{"name":"NFT name", "description": result['nft_name']},
						{"name":"Starting bid", "description":f"{result['starting_price']} ADA"},
						{"name":"Begins on", "description":f"{result['start_date']}, {result['start_time']}, {tzstr}"},
						{"name":"Ends on", "description":f"{result['end_date']}, {result['end_time']}, {tzstr}"}
						]
	message = discord.Embed(title=title, description="", color=0x00ff00)
	message.set_image(url=result["image"])
	for field in fields:
		message.add_field(name=field["name"], value=field["description"], inline=False)
	return (message)

def auction_start(info):
	title = f"Attention! Auction Started!"
	time_left = get_remaining_time(info)
	fields = [{"name":"NFT", "description": f"**{info['nft_name'].upper()}**"},
				  {"name":"Starting Price", "description": f"`{info['price']}` ADA"},
				  {"name":"Increment", "description": f"`{INCREMENT_AMOUNT}` ADA"},
				  {"name":"Ends in", "description": f"{time_left}"},
				  {"name":"Command", "description": f"`{PR}bid`"}]
	message = discord.Embed(title=title, description="", color=0x00ff00)
	message.set_image(url=info["image_link"])
	for field in fields:
		message.add_field(name=field["name"], value=field["description"], inline=True)
	message.set_author(name = "Powered by Popular Lab", icon_url=POPULAR_LAB_ICON_URL)
	return (message)

def auction_end(info):
	title = f"Congratulations! Auction Ended!"
	time_left = get_remaining_time(info)
	fields = [{"name":"NFT", "description": f"**{info['nft_name'].upper()}**"},
				  {"name":"New Owner", "description": f"{info['highest_bidder']}"},
				  {"name":"Price", "description": f"{info['price']} ADA"}]
	if (info["highest_bidder"] == ""):
		title = f"Nobody has placed bids on **{info['nft_name']}**!"
		fields = [{"name":f"Today I admit defeat but I'll be back with an offer. you cant refuse!",
		"description":f"Now {info['nft_name']} remains mine for eternity!"}]
	message = discord.Embed(title=title, description="", color=0x00ff00)
	message.set_image(url=info["image_link"])
	for field in fields:
		message.add_field(name=field["name"], value=field["description"], inline=False)
	message.set_author(name = "Powered by Popular Lab", icon_url=POPULAR_LAB_ICON_URL)
	return (message)