from singleQuery import search_date, search_price, search_term
import datetime
import re


def main():
	full = False
	exit = False


	while not exit:
		search = input("Input Query: ").lower()

		if (search == "output=full"):
			full = True

			print("Output set to full")
			continue

		elif (search == "output=brief"):
			full = False

			print("Output set to brief")
			continue

		elif (search == "exit"):
			break

		search_words = search.split()
		num_words = len(search_words)
		valid_query = True
		current_word = 0
		data = None

		while current_word < num_words:
			# print(search_words[current_word])
			word = search_words[current_word]

			# check if query is date
			if (word == "date"):
				operator = search_words[current_word + 1]
				target = search_words[current_word + 2]

				if check_operator(operator):
					
					try: 
						year,month,day = target.split('/')
						datetime.datetime(int(year), int(month), int(day))

					except ValueError:
						valid_query = False
						break

					# search_query = word + " " + operator + " " + target
					search_query = word + operator + target
					data = search_date(search_query, data)
					current_word += 3	

				else:
					valid_query = False
					break

			# check if query is price
			elif (word == "price"):
				operator = search_words[current_word + 1]
				target = search_words[current_word + 2]

				if (check_operator(operator)):
					try:
						int(target)

					except ValueError:
						valid_query = False
						break

					search_query = word + operator + target
					data = search_price(search_query, data)
					current_word += 3

				else:
					valid_query = False
					break

			elif (word == "location" or word == "cat"):
				operator = search_words[current_word + 1]
				target = search_words[current_word + 2]

				if (check_operator(operator)):
					search_query = word + operator + target

					# data = search_location(search_query, data)
					current_word += 3

			# check if query is term
			elif (re.match(r'^[a-z0-9]+[%]?$', word) is not None):	#Fred assisted with RegEx understanding
				data = search_term(word, data)
				current_word += 1

			else:
				valid_query = False
				break
			
		if (valid_query):

			if full:
				for value in data:
					print(value[0] + " | " + value[1] + " | " + value[2] + " | " + value[3] + " | " + value[4] + " | " + value[5] + " | " + value[6])

			else:
				for value in data:
					print(value[0] + " | " + value[4])

		else:
			print("Invalid query syntax encountered")


def check_operator(operator):
	
	if (operator == "<" or  operator == ">" or operator == "<=" or operator == ">=" or operator == "="):
		return True

	else:
		return False

main()