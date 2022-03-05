import os
from discord.ext import commands, tasks
from cmds import general_commands
import auction
from utils import AUCTION_CATEGORY_ID, GUILD_ID, now, tz, sanitise, PR
import api_firestore
import messages
from datetime import datetime

PREFIX = (PR)
bot = commands.Bot(command_prefix=PREFIX, description='Hi', help_command=None)
task_running = 0

def get_token():
  token = os.getenv("TOKEN")
  return (token)

@bot.event
async def on_ready():
	print(bot.user.name, "is online")
	print(bot.user.id)
	global task_running
	if (task_running == 0):
		timed_checker.start()
		task_running = 1


@tasks.loop(seconds=60)
async def timed_checker():
  await check_auction_start()
  await check_auction_end()

def get_auction_category(categories):
	for category in categories:
		if (category.id == AUCTION_CATEGORY_ID):
			return (category)

def get_created_channel(nft_name):
	nft_name = sanitise(nft_name.lower())
	guild = bot.get_guild(GUILD_ID)
	category = get_auction_category(guild.categories)
	channels = list(category.channels)
	for channel in channels:
		if (channel.name == f"auction-{nft_name}"):
			return (channel)

async def init_auction(nft_name):
	guild = bot.get_guild(GUILD_ID)
	name = sanitise(f"auction-{nft_name}")
	category = get_auction_category(guild.categories)
	if (not category):
		print("I CANT FIND THE AUCTION CATEGORY")
		return
	else:
		print("channel created")
		await guild.create_text_channel(name = name, category = category)
		channel = get_created_channel(nft_name)
		if (channel != None):
			api_firestore.update_auction_start(nft_name, 1)
	return (channel)

async def check_auction_start():
	auctions = api_firestore.get_all_auctions()
	for auction in auctions:
		auction = auction.to_dict()
		if (len(auction) == 0):
			break
		info = api_firestore.get_auction(auction["nft_name"])
		current_time = now()
		auction_time = datetime.strptime(
			f"{info['start_date']} {info['start_time']}",
			"%d/%m/%y %H:%M").replace(tzinfo=tz)
		if (((current_time.date() == auction_time.date()
			and current_time.time().hour == auction_time.time().hour
			and current_time.time().minute >= auction_time.time().minute) or 
			(current_time.date() >= auction_time.date()
			or current_time.time().hour >= auction_time.time().hour))
				and info["started"] == 0):
			print("auction started")
			channel = await init_auction(info["nft_name"])
			await channel.send(embed=messages.auction_start(info))

async def check_auction_end():
	auctions = api_firestore.get_all_auctions()
	for auction in auctions:
		auction = auction.to_dict()
		if (len(auction) == 0):
			break
		info = api_firestore.get_auction(auction["nft_name"])
		current_time = now()
		auction_time = datetime.strptime(
			f"{info['end_date']} {info['end_time']}",
			"%d/%m/%y %H:%M").replace(tzinfo=tz)
		if ((current_time.date() == auction_time.date()
				and current_time.time().hour == auction_time.time().hour
				and current_time.time().minute >= auction_time.time().minute) or 
				(current_time.date() >= auction_time.date()
				and current_time.time().hour > auction_time.time().hour)):
			print("auction ended")
			api_firestore.delete_auction(info["nft_name"])
			channel = get_created_channel(info["nft_name"])
			await channel.send(embed=messages.auction_end(info))
			guild = bot.get_guild(GUILD_ID)
			await channel.set_permissions(guild.default_role, send_messages=False)

	
bot.add_cog(general_commands())
bot.run(get_token())