from singleQuery import query
import datetime
import re


def main():

	search = input("Input Query: ").lower()
	search_words = search.split()
	num_words = len(search_words)
	valid_query = True
	current_word = 0

	while current_word < num_words:
		# print(search_words[current_word])
		word = search_words[current_word]
		
		# check if query is camera
		if ("camera" in word):
			if (word == "camera" or word == "camera%"):
				query(word)
				current_word += 1
			else:
				valid_query = False
				break

		# check if query is date
		elif (word == "date"):
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
				# print(search_query)
				query(search_query)
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
				query(search_query)
				current_word += 3

			else:
				valid_query = False
				break

		else:
			valid_query = False
			break
		
	if (valid_query):
		print("Valid Query")

		# TODO: Print query output

	else:
		print("Invalid query syntax encountered")

	# query()


def check_operator(operator):
	
	if (operator == "<" or  operator == ">" or operator == "<=" or operator == ">=" or operator == "="):
		return True

	else:
		return False

main()