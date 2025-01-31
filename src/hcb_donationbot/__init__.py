#################
# SETUP/IMPORTS #
#################

__version__ = "1.0.0"

import asyncio  # noqa
import datetime

import requests


############
# DEFAULTS #
############
DEFAULT_HOURS = 24
DEFAULT_ORG = "hq"

#################
# API ENDPOINTS #
#################
DONATION_API_URL = "https://hcb.hackclub.com/api/v3/organizations/{org_id}/donations"
NAME_API_URL = "https://hcb.hackclub.com/api/v3/organizations/{org_id}"

#####################
# MESSAGE TEMPLATES #
#####################
AMOUNT_MESSAGE = "There were {amount} donations to {name} in the last {hours} hours {emoji}"
THANKS_MESSAGE = """Many thanks to **{name}** for donating **${amount_dollars:.2f}(USD)** to **{org_name}** {emoji}
(*donated on {date} at {time}*)"""


#############
# FUNCTIONS #
#############
async def check_donations(ctx, org_id: str = DEFAULT_ORG, hours: int = DEFAULT_HOURS):
	check_period = datetime.datetime.now() - datetime.timedelta(hours=hours)
	# Fetch donation data from the HCB API
	response = requests.get(DONATION_API_URL.format(org_id=org_id))
	org_name = await get_org_name(org_id)
	transactions = response.json()

	filtered_transactions = []

	for transaction in transactions:
		transaction["date"] = datetime.datetime.strptime(transaction['date'], "%Y-%m-%dT%H:%M:%SZ")
		if transaction["date"] > check_period:
			filtered_transactions.append(transaction)

	filtered_transactions = sorted(filtered_transactions, key=lambda x: x["date"])

	# Send the filtered transactions to the channel

	await ctx.send(
		AMOUNT_MESSAGE.format(
			amount=len(filtered_transactions),
			name=org_name,
			hours=hours,
			emoji=":tada:" if len(filtered_transactions) > 0 else ":sob:"
		)
	)

	for transaction in filtered_transactions:
		await ctx.send(
			THANKS_MESSAGE.format(
				name=d["name"] if not (d := transaction["donor"])["anonymous"] else "Anonymous Donor",
				amount_dollars=transaction["amount_cents"] / 100,
				org_name=org_name,
				date=transaction["date"].strftime("%Y-%m-%d"),
				time=transaction["date"].strftime("%H:%M:%S"),
				emoji=":tada:"
			)
		)


async def get_org_name(org_id):
	res = requests.get(NAME_API_URL.format(org_id=org_id))
	res.raise_for_status()
	return res.json()["name"]
