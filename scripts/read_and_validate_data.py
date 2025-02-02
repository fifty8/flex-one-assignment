import json

# Open JSON file and load file content string as JSON object
with open("resources/account_data.json") as file:
	data = json.load(file)

print(json.dumps(data, indent = 2))
assert "assets" in data.keys()
assert "liabilities" in data.keys()
assert "equity" in data.keys()

"""
Raise an exception if:
- The account has no key `value`
- The account has subaccounts under key `items` but their values don't add up to 
  the account's value.
"""
def validateAccount(accountData, precision = 2):
	if "name" not in accountData:
		print(json.dumps(accountData, indent = 2))
		raise Exception("Account data is missing name. Full printout above.")
	
	accountName = accountData["name"]
	
	if "items" not in accountData.keys():
		print(f"[O] Account [{accountName}] has no child accounts")
		return
	
	subAccounts = accountData["items"]
	
	if len(subAccounts) == 0:
		print(f"[O] Account [{accountName}] has no child accounts")
		return
	
	if "value" not in accountData.keys():
		print(f"[X] Account [{accountName}] has no `value` key.")
		return
	
	accountValue = float(accountData["value"])
	
	subAccountTotal = 0.0
	for subAccountData in subAccounts:
		# Recursively validate the subaccount
		validateAccount(subAccountData)
		
		if "value" in subAccountData.keys():
			subAccountTotal += float(subAccountData["value"])
	
	subAccountTotal = round(subAccountTotal, precision)
	accountValue = round(accountValue, precision)
	
	if subAccountTotal != accountValue:
		print(f"[X] Account [{accountName}] has value {accountValue}, but {len(subAccounts)} child accounts have values that total {subAccountTotal}")
	else:
		print(f"[O] Account validated: [{accountName}] has value {accountValue} and {len(subAccounts)} child accounts")


def validateTopLevelAccounts(data, precision = 2):
	assetTotal = round(float(data["assets"]["value"]), precision)
	liabilitiesTotal = float(data["liabilities"]["value"])
	equityTotal = float(data["equity"]["value"])
	
	if assetTotal != round(liabilitiesTotal + equityTotal, precision):
		print(f"[X] Assets total {assetTotal} does not equal to liabilities and equity total {round(liabilitiesTotal + equityTotal, precision)}")
	else:
		print(f"[O] Assets total {assetTotal} match the sum of liabilities and equity")

def main():
	validateAccount(data["assets"])
	validateAccount(data["liabilities"])
	validateAccount(data["equity"])
	validateTopLevelAccounts(data)

if __name__ == "__main__":
	main()
