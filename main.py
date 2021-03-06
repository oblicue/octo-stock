import threading
import numpy as np
from matplotlib import pyplot as plt
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import requests
import json
import time
from PyInquirer import *
import pandas as pd
# TO DO
# -- add graphs using PIL or something

location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) # dont understand this but it works 🤷

# gets results from json file
with open(os.path.join(location, 'watchlist.json'), 'r') as f:
    analyse = json.loads(f.read())

#getting your api token from the .env file
load_dotenv()
TOKEN = os.getenv('TOKEN')

#you can also add your own custom date instead of yesterdays date
date = (datetime.now() - timedelta(1)).strftime("%Y-%m-%d")

#json or formatted
formatted = True

def show_analyse_list():
    for i in analyse:
        r = requests.get(f'https://api.polygon.io/v1/open-close/{i}/{date}?unadjusted=true&apiKey={TOKEN}').json()
        # remove some of these values if you dont want em, if you use the formatted version, remove them from the print too lol
        try:
            result = {
                'symbol': r['symbol'],
                'open': r['open'],
                'high': r['high'],
                'low': r['low'],
                'close': r['close'],
                'afterhours': r['afterHours'],
                'date': r['from']
            }
        except:
            if formatted:
                print(f"Error! Here it is: {r['error']}")
                break
            else:
                print(f"Error! {r}")
                break
        if formatted:
            print(f'''
            Symbol: {result["symbol"]},
            Opening: {result["open"]},
            High: {result["high"]},
            Low: {result["low"]},
            Closing: {result["close"]},
            After Hours: {result["afterhours"]},
            Date: {result["date"]}
            ''')
        else:
            print(result)

def display_graph(item): # not yet implemented because i dont understand matplotlib and i dont think there's enough data to create a graph anyway. too bad.
    r = requests.get(f'https://api.polygon.io/v1/open-close/{item}/{date}?unadjusted=true&apiKey={TOKEN}').json()
    try:
        result = {
            'symbol': r['symbol'],
            'open': r['open'],
            'high': r['high'],
            'low': r['low'],
            'close': r['close'],
            'afterhours': r['afterHours'],
            'date': r['from']
        }
    except:
            print(f"Error! {r}")
            return
    dev_y = [result["open"], result["close"]]

    dev_x = [0, 24]

    plt.plot(dev_x, dev_y)
    plt.show()
def add_to_watchlist(item):
    print("Remember - the polygon api free version has a 5 requests per minute limit")
    with open(os.path.join(location, 'watchlist.json'), 'w') as f:
        analyse.append(item)
        json.dump(analyse, f, ensure_ascii=False, indent=4)
def remove_from_watchlist(item):
    with open(os.path.join(location, 'watchlist.json'), 'r', encoding='utf-8') as f:
        toiletdance = json.load(f) # load
    if item == 'everything':
        toiletdance = []
    else:
        toiletdance.remove(item) # actually do something
    with open(os.path.join(location, 'watchlist.json'), 'w', encoding='utf-8') as f:
            json.dump(toiletdance, f, ensure_ascii=False, indent=4) # save

def run():
    #show_analyse_list() # hardcoded in for easy testing
    #add_to_watchlist('SBUX') # hardcoded in for easy testing
    style = style_from_dict({
        Token.Separator: '#cc5454',
        Token.QuestionMark: '#673ab7 bold',
        Token.Selected: '#cc5454',  # default
        Token.Pointer: '#673ab7 bold',
        Token.Instruction: '',  # default
        Token.Answer: '#f44336 bold',
        Token.Question: '',
    })

    questions = [
        {
            'type': 'list',
            'message': 'Select action',
            'name': 'Actions',
            'choices': [
                {
                    'name': 'showwatchlist'
                },
                {
                    'name': 'addtowatchlist'
                },
                {
                    'name': 'removefromwatchlist'
                }
            ],
            'validate': lambda answer: 'You need to pick an action.' \
                if len(answer) == 0 else True
        }
    ]

    answers = prompt(questions, style=style)
    if answers['Actions'] == 'showwatchlist':
        show_analyse_list()
    elif answers['Actions'] == 'addtowatchlist':
        question = [
            {
                'type': 'input',
                'name': 'whattoadd',
                'message': 'What do you want to add?'
            }
        ]
        time.sleep(0.5)
        answer = prompt(question, style=style)
        add_to_watchlist(answer['whattoadd'])
        print(f"Done! Added {answer['whattoadd']} to your watchlist!")
    elif answers['Actions'] == 'removefromwatchlist':
        questionpoo = [
            {
                'type': 'input',
                'name': 'whattoremove',
                'message': 'What do you want to remove?'
            }
        ]
        time.sleep(0.5)
        answerwacky = prompt(questionpoo, style=style)
        remove_from_watchlist(answerwacky['whattoremove'])
        print(f"Successfully removed {answerwacky['whattoremove']} from your watchlist!")
    question2 = [
        {
            'type': 'list',
            'message': 'Select action',
            'name': 'Actions',
            'choices': [
                {
                    'name': 'continue'
                },
                {
                    'name': 'quit'
                }
            ],
            'validate': lambda answer: 'You need to pick an action.' \
                if len(answer) == 0 else True
        }
    ]
    answer2 = prompt(question2, style=style)
    if answer2['Actions'] == 'continue':
        run()
    else:
        print("Okay. Quitting...")
        quit()
if __name__ == '__main__':
    run()
    # display_graph("HD") # debugging
