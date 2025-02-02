# README

## Question 1: ERD on the account data

Please find the ERD in `account_data_erd.jpeg` in the root directory.

With the information given to me, I think it's a sensible approach to have an _Account_ entity, and an implied _Entity_ entity (a company, a user, a coporation, etc.). Both entities should become a respective table in a relational database world. They shall have these relationships:

- Each _Entity_ has 3 root _Accounts_: assets, liabilities, and equity. In the assignment, I was provided data for only one _Entity_.

- Each _Account_:
	- Has a UUID-4 string as the primary key
	- Has a name
	- Has a value
	- Optionally has a `parentAccountID` that is the ID of another _Account_.

I noticed that some accounts don't have a valid Account ID in the data. It may be due to how the system was setup before, or just indications of data quality issues. If given more context I'll be able to adjust the graph.

## Question 2: Validate account data

The validation is done in Python 3, serializing the JSON file and recursively check if any account has issue:

- All accounts must have a name
- All accounts must have a value that can convert into a number, under the `value` key
- For accounts with children under the key `items`, the immediate children's values should add up to the value of the parent

The validation also quickly checks if assets = liabilities + equity.

To execute the script:

1. Make sure you are at the repository's root directory

2. Check that the directory `dest` exists (I used an empty file `.gitkeep` so it should be there automatically upon Git clone)

3. Run this command (assuming the executable is `python3`):

	```sh
	python3 scripts/read_and_validate_data.py > dest/validation.log
	```

4. Check the log in `dest/validation.log`. Lines that begin with `[X]` in indicate an error. 
	
	During my execution, there are 2 errors:
	
	- Assets total is not the same as Liabilities + Equity. (This may be expected from outstanding revenue/expenses in the current fiscal year, but I'm calling it out here nonetheless.)
	
	- "Current Liabilities" has value 1,014,525.75, but its 2 child accounts add up to a total of 937,527.65.

There may be better ways to call out validation errors, by raising exceptions, for example. But I think it's a decision better made if given more specific requirements and backgrounds on the entire data systems.

## Other comments

Regarding consumption or ETL of the data:

I am not sure if the next step of the data is to load it in a relational database, where we can manipulate data in SQL.

There may be more considerations before we can load the data in the database:

- Some accounts have missing Account ID. This may be expected as it only seems to happen to accounts with fixed names ("ASSETS", "Current Liabilities", etc.)

- Some accounts have an Account ID that doesn't follow UUID-4 format. For example, "Settle Loans Payable" has ID `220`. Again, this may be expected given certain business context.
