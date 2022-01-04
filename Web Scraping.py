import bs4 as bs
import urllib.request
import re

# Create a source for our soup
matches_url = "https://www.uefa.com/uefachampionsleague/news/026c-131a0f45d056-813415b1929d-1000--all-the-2021-22-champions-league-fixtures-and-results/"
source = urllib.request.urlopen(matches_url).read()

# Our soup
soup = bs.BeautifulSoup(source, 'lxml')

# Isolate divs involving the content of the article
divs = soup.find_all('div', class_='article_content')

# Extract the text from the first div
div_text = divs[0].text

# Create a list of lines for each bit of text seperated by a new line
lines = [line for line in div_text.split('\n') if line != '']

# We only want the group stage results
lines = lines[3:]

# First few characters are just highlights, each line represents a different Matchday
# We can split on every day and on "Group", this should be enough for now
days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
splitting = ''
for day in days:
    splitting += '{} |'.format(day)
splitting += 'Group'

# All lines start with a Tuesday so we look for this to do our splitting
# Initialise our dictionary and current date
date_match = {}
digits = [str(i) for i in range(1,10)]
current_date = None

for line in lines:
    new_line = line[line.find('Tuesday'):]
    new_lines = re.split(splitting, new_line)[1:]

    # Iterate through these split lines and group matches by the date
    for item in new_lines:
        if item[0] in digits and item not in date_match.keys():
            date_match[item] = []
            current_date = item
        else:
            date_match[current_date].append(item)

print(date_match)