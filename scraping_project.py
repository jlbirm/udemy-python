# http://quotes.toscrape.com
import requests
from bs4 import BeautifulSoup as bs
import random
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

page_url = 'http://quotes.toscrape.com'
quotes_list = []

while True:
	response = requests.get(page_url, verify = False)
	soup = bs(response.text, "html.parser")

	quotes = soup.find_all(class_="quote")

	for quote in quotes:
		text = quote.find(class_= "text").get_text()
		name = quote.find(class_= "author").get_text()
		url = quote.find("a")["href"]
		quote_dict = {"text" : text, "name" : name, "url" : url}
		quotes_list.append(quote_dict)

	if soup.find(class_= "next"):
		page_url = f'https://quotes.toscrape.com{soup.find(class_= "next").find("a")["href"]}'
	else:
		break

# Guessing Game

def hint(rem_guesses, cur_quote, answer):
	response = requests.get(f"https://quotes.toscrape.com{cur_quote['url']}", verify = False)
	soup = bs(response.text, "html.parser")
	name_split = cur_quote["name"].split()

	if rem_guesses == 3:
		born_date = soup.find(class_="author-born-date").get_text()
		born_loc = soup.find(class_="author-born-location").get_text()

		return f'The author was born on {born_date} {born_loc}.'

	elif rem_guesses == 2:
		first_name = name_split[0]
		first_initial = first_name[0]
		return f"The author's first initial is {first_initial}"

	elif rem_guesses == 1:
		last_name = name_split[1]
		last_initial = last_name[0]
		return f"The author's last initial is {last_initial}"
	else:
		return f"Sorry, you've run out of guesses. The answer was {answer}"


def play_again():
	while True:
		play_again = input('Would you like to play again (y/n)? ')

		if play_again == 'y':
			print('Great! Here we go again...')
			return True

		elif play_again == 'n':
			print("Okay! Thank's for playing!")
			return False

		else:
			print("I'm sorry, that was not an option")
			continue

def game():
	i = random.randrange(len(quotes_list))
	cur_quote = quotes_list[i]
	print(f'Here is a quote: {cur_quote["text"]}')

	rem_guesses = 4
	answer = cur_quote["name"]

	while rem_guesses > 0:
		guess = input(f"Who said this? Guesses remaining: {rem_guesses} ")

		if guess == answer:
			print("You're right!")
			break
		else:
			rem_guesses -= 1
			print(hint(rem_guesses, cur_quote, answer))

keep_playing = True

while keep_playing == True:
	game()
	keep_playing = play_again()