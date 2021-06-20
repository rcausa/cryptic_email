import requests
from bs4 import BeautifulSoup 
import sqlite3

"""
Scrape all clues and store in a json file.
Be able to retrieve from the json file.

New script:
go to all puzzles page, get puzzle id, check if exists in json. 
If not, add to json.

New script:
Take all emails from URL of an email list/database, then retrieve some clues and answers.
Create an HTML body, and send email via protonmail/gmail to each address.
"""

# storage_dict = {}


def create_table():
    """
    Create database table.
    """
    conn = sqlite3.connect('cryptic_clues_and_answers.db')
    print('Database created...')
    try:
        conn.execute(
            """
            CREATE TABLE CRYPTIC_CLUES_AND_ANSWERS
            ( ID INTEGER PRIMARY KEY,
            PUZZLE_ID INT NOT NULL,
            CLUE TEXT NOT NULL,
            ANSWER TEXT NOT NULL );
            """
        )
        print('Table format successful...')
    except Exception as e:
        print(e,'\n')
    conn.close()

# Create database    
create_table()

def insert_table(connection,puzzle,clue,answer):
    text = f"""
    INSERT INTO CRYPTIC_CLUES_AND_ANSWERS (PUZZLE_ID, CLUE, ANSWER)
    VALUES (?, ?, ?)
    """
    connection.execute(text, (puzzle,clue,answer))

def string_replace(string):
    string = string.replace("'","_APOST").replace(",","_COMMA").replace(".","_PERIOD").replace("?","_QUES").replace(":","_COL").replace(";","_SEMICOL").replace("!","_EXCL").replace("%","_PERC").replace("(","_LBRAC").replace(")","_RBRAC")
    return string

def inv_string_replace(string):
    string = string.replace("_APOST","'").replace("_COMMA",",").replace("_PERIOD",".").replace("_QUES","?").replace("_COL",":").replace("_SEMICOL",";").replace("_EXCL","!").replace("_PERC","%").replace("_LBRAC","(").replace("_RBRAC",")")
    return string 

more_pages = True
page = 1

while more_pages:
    try:
        print(f'Page: {page}')
        # Each page with 5 puzzles
        all_puzzles_url = f'https://www.theguardiancrosswordanswers.com/category/the-guardian-cryptic-crossword/page/{page}/'
        puzzle_soup = BeautifulSoup(requests.get(all_puzzles_url).content, 'html.parser')
        puzzles = puzzle_soup.find_all('article') # 5 results / page

        for p in puzzles:
            # Open DB connection once per puzzle
            connection = sqlite3.connect('cryptic_clues_and_answers.db')
            
            # Get id number and url for each puzzle
            puzzle_title = p.find('a')['title']
            puzzle_id = int(puzzle_title.split(' ')[-2])
            puzzle_href = p.find('a')['href']
            print(f'Puzzle: {puzzle_id}')

            # Get clues and answers - 2 lists ACROSS, DOWN, w separate urls per answer
            clues_soup = BeautifulSoup(requests.get(puzzle_href).content, 'html.parser')
            across_down_lists = clues_soup.find('body').find('div',class_='single clear').find('div',class_='content').find('article',class_='article').find_all('ul')[:2]
            
            # Finally navigate to clues and their answers
            for lists in across_down_lists:
                clues_list = lists.find_all('li')
                for clue in clues_list:
                    question = clue.find('a').text[:]
                    answer_url = clue.find('a')['href']
                    answer_soup = BeautifulSoup(requests.get(answer_url).content,'html.parser')
                    answer = answer_soup.find('body').find('div',class_='main-container clear').find('div',class_='single clear').find('div',class_='content').find('article',class_='article').find('div',class_='solutions').text[8:]
                    # print(question, answer) # original string literal
                    question = string_replace(question)
                    answer = answer.replace("'","`").replace(","," ")
                    print(question, answer)

                    # Add each clue individually
                    insert_table(connection,puzzle_id, question, answer)
                    connection.commit()
            
            # Close DB connection once per puzzle        
            connection.close()
            print('-----') # after each puzzle
        print('\n') # after each page
        page += 1

    except: # If cannot resolve page URL, i.e. no more pages
        break
    
