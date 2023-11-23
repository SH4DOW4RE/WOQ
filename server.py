from flask import Flask, render_template, request
import socket
from random import randint
import json
import os
import math


app = Flask(__name__)

IP = socket.gethostbyname(socket.gethostname())
PORT = 5000
global correct
correct = ''


def monstersAlive():
    with open('static/stats.json', 'r') as f:
        data = json.load(f)
    goblin = data['goblin']['curr-health']
    orc1 = data['orc1']['curr-health']
    orc2 = data['orc2']['curr-health']
    dragon = data['dragon']['curr-health']
    if goblin <= 0 and orc1 <= 0 and orc2 <= 0 and dragon <= 0:
        return False
    else:
        return True


@app.route('/')
def index():
    os.remove('static/stats.json')
    with open('static/stats_reset.json', 'r') as p:
        with open('static/stats.json', 'w+') as f:
            p.seek(0)
            f.seek(0)
            data = p.read()
            f.write(data)
    return render_template('index.html')

@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/rules')
def rules():
    return render_template('rules.html')

@app.route('/game/player')
def play(question_=False, answer_=False, killed=False, encounter=False,
        topic='', difficulty=0, attacker='', attacked = '',
        question='', die_val=0, correct='', answer='',
        answer1='', answer2='', answer3='', answer4='',
        question_index="-1", battle_=False, roll=0):
    return render_template('play.html',
        question_=question_, answer_=answer_, attacker=attacker, attacked = attacked,
        topic=topic, difficulty=difficulty, answer=answer, killed=killed,
        question=question, die_val=die_val, correct=correct, encounter=encounter,
        answer1=answer1, answer2=answer2, answer3=answer3, answer4=answer4,
        question_index=question_index, battle_=battle_, roll=roll)

@app.route('/game/player', methods=['POST'])
def playing(skip = False, args=[]):
    global correct
    if not skip:
        try: player = request.form['player'] if request.form['player'] != "0" else None
        except: player = None
        try: question = request.form['question'] if request.form['question'] != "" else None
        except: question = None
        try: topic = request.form['topic'] if request.form['topic'] != "" else None
        except: topic = None
        try: answer = request.form['answer'] if request.form['answer'] != "-1" else None
        except: answer = None
        try: attacker = request.form['attacker'] if request.form['attacker'] != "-1" else None
        except: attacker = None
        try: attacked = request.form['attacked'] if request.form['attacked'] != "-1" else None
        except: attacked = None
    else:
        player = args[0]
        question = args[1]
        answer = args[2]
        topic = args[3]
        attacker = args[4]
        attacked = args[5]
    if player == None and question == None and answer == None and topic == "-1":
        # Error
        raise Exception
    
    # Player 1
    elif (player == "1" and question == "-5" and answer == None and topic == "-1") or \
         (player == "1" and question == "-5" and answer == None and topic == None):
        # Ask if encounter
        return play(battle_ = True)
    elif (player == "1" and question == None and answer == None and topic == "-1") or \
         (player == "1" and question == None and answer == None and topic == None):
        # Roll the dice
        roll = randint(1, 5)
        return play(roll = roll, die_val = roll)
    elif (player == "1" and question == "-1" and answer == None and topic == "-1") or \
         (player == "1" and question == "-1" and answer == None and topic == None):
        # Ask wich monster
        return play(encounter = True)
    elif (player == "1" and question == "-3" and answer == None and topic == "-1") or \
         (player == "1" and question == "-3" and answer == None and topic == None):
        # Ask a question
        cont = True
        while cont:
            topic = 'HTML' if randint(0, 1) == 1 else 'CSS'
            difficulty = randint(1, 10)
            with open(f'static/questions/{topic.lower()}.json') as f:
                data = json.load(f)
            qs = []
            questions = []
            for i in range(20):
                qs.append(data[f'questions{i+1}'])
            for i in range(len(qs)):
                if qs[i]['difficulty'] == difficulty:
                    questions.append(qs[i])
            cont = False
            try: question_index = randint(1, len(questions)) - 1
            except: cont = True
        question = questions[question_index]['question']
        answer1 = questions[question_index]['possibilities'][0]
        answer2 = questions[question_index]['possibilities'][1]
        answer3 = questions[question_index]['possibilities'][2]
        answer4 = questions[question_index]['possibilities'][3]
        for i in range(len(qs)):
            if qs[i]['question'] == question:
                qi = i + 1
        if attacker == '':
            attacker = 'player'
        else:
            attacker = attacker
        return play(question_=True, topic=topic, difficulty=difficulty,
                    question=question, question_index=str(qi),
                    answer1=answer1, answer2=answer2,
                    answer3=answer3, answer4=answer4, attacker=attacker, attacked=attacked)
    elif (player == "1" and question == "-2" and answer == None and topic == "-1") or \
         (player == "1" and question == "-2" and answer == None and topic == None):
        # No battle
        return play()
    elif player == "1" and question != None and answer == "-2" and topic != "-1":
        # Continue battle
        if attacker == 'player':
            atk = attacker + player
        else:
            atk = attacker
        if attacked == 'player':
            atd = attacked + player
        else:
            atd = attacked
        with open('static/stats.json', 'r') as f:
            data = json.load(f)
        cah = data[atk]['curr-health']
        cdh = data[atd]['curr-health']
        d_ = attacker if attacker != 'player' else attacked
        difficulty = int(topic)
        
        killed = False
        if attacker == 'player':
            cdh -= difficulty
        else:
            if question == "-10":
                if difficulty == 1:
                    difficulty = 0
                else:
                    difficulty = math.floor(difficulty * .8)
                    if difficulty < 1:
                        difficulty = 1
            cdh -= difficulty
        with open('static/stats.json', 'r') as f:
            data = json.load(f)
        data['player1']['curr-health'] = cah
        data[atd]['curr-health'] = cdh
        os.remove('static/stats.json')
        with open('static/stats.json', 'w+') as f:
            json.dump(data, f)
        if data[f'player{player}']['curr-health'] <= 0:
            return render_template('game_over.html')
        if data[d_]['curr-health'] <= 0:
            killed = True
        tmp = attacker
        attacker = attacked
        attacked = tmp
        print(monstersAlive())
        if not monstersAlive():
            return render_template('winner.html')
        print(killed)
        if killed:
            with open('static/stats.json', 'r') as f:
                data = json.load(f)
            data['player1']['curr-health'] = 20 if data['player1']['curr-health'] < 20 else data['player1']['curr-health']
            os.remove('static/stats.json')
            with open('static/stats.json', 'w+') as f:
                json.dump(data, f)
            return play(killed = True)
        player = "1"
        question = "-3"
        answer = None
        topic = "-1"
        args = [player, question, answer, topic, attacker, attacked]
        return playing(skip = True, args = args)
    elif player == "1" and question != None and answer != None and topic != "-1":
        # Show answer
        topic = 'HTML' if topic == "1" else 'CSS'
        with open(f'static/questions/{topic.lower()}.json') as f:
                data = json.load(f)
        ai = data[f'questions{question}']['answer']
        correct = 'Correct' if int(answer) == ai else 'Wrong'
        difficulty = data[f'questions{question}']['difficulty']
        answer = data[f'questions{question}']['possibilities'][ai]
        return play(answer_=True, topic='ANSWER', difficulty=difficulty,
                    answer=answer, correct=correct, attacker=attacker, attacked=attacked)
    
    # Player 2
    elif (player == "2" and question == "-5" and answer == None and topic == "-1") or \
         (player == "2" and question == "-5" and answer == None and topic == None):
        # Ask if encounter
        return play(battle_ = True)
    elif (player == "2" and question == None and answer == None and topic == "-1") or \
         (player == "2" and question == None and answer == None and topic == None):
        # Roll the dice
        roll = randint(1, 5)
        return play(roll = roll, die_val = roll)
    elif (player == "2" and question == "-1" and answer == None and topic == "-1") or \
         (player == "2" and question == "-1" and answer == None and topic == None):
        # Ask wich monster
        return play(encounter = True)
    elif (player == "2" and question == "-3" and answer == None and topic == "-1") or \
         (player == "2" and question == "-3" and answer == None and topic == None):
        # Ask a question
        cont = True
        while cont:
            topic = 'HTML' if randint(0, 1) == 1 else 'CSS'
            difficulty = randint(1, 10)
            with open(f'static/questions/{topic.lower()}.json') as f:
                data = json.load(f)
            qs = []
            questions = []
            for i in range(20):
                qs.append(data[f'questions{i+1}'])
            for i in range(len(qs)):
                if qs[i]['difficulty'] == difficulty:
                    questions.append(qs[i])
            cont = False
            try: question_index = randint(1, len(questions)) - 1
            except: cont = True
        question = questions[question_index]['question']
        answer1 = questions[question_index]['possibilities'][0]
        answer2 = questions[question_index]['possibilities'][1]
        answer3 = questions[question_index]['possibilities'][2]
        answer4 = questions[question_index]['possibilities'][3]
        for i in range(len(qs)):
            if qs[i]['question'] == question:
                qi = i + 1
        if attacker == '':
            attacker = 'player'
        else:
            attacker = attacker
        return play(question_=True, topic=topic, difficulty=difficulty,
                    question=question, question_index=str(qi),
                    answer1=answer1, answer2=answer2,
                    answer3=answer3, answer4=answer4, attacker=attacker, attacked=attacked)
    elif (player == "2" and question == "-2" and answer == None and topic == "-1") or \
         (player == "2" and question == "-2" and answer == None and topic == None):
        # No battle
        return play()
    elif player == "2" and question != None and answer == "-2" and topic != "-1":
        # Continue battle
        if attacker == 'player':
            atk = attacker + player
        else:
            atk = attacker
        if attacked == 'player':
            atd = attacked + player
        else:
            atd = attacked
        with open('static/stats.json', 'r') as f:
            data = json.load(f)
        cah = data[atk]['curr-health']
        cdh = data[atd]['curr-health']
        d_ = attacker if attacker != 'player' else attacked
        difficulty = int(topic)
        
        killed = False
        if attacker == 'player':
            cdh -= difficulty
        else:
            if question == "-10":
                if difficulty == 1:
                    difficulty = 0
                else:
                    difficulty = math.floor(difficulty * .8)
                    if difficulty < 1:
                        difficulty = 1
            cdh -= difficulty
        with open('static/stats.json', 'r') as f:
            data = json.load(f)
        data['player1']['curr-health'] = cah
        data[atd]['curr-health'] = cdh
        os.remove('static/stats.json')
        with open('static/stats.json', 'w+') as f:
            json.dump(data, f)
        if data[f'player{player}']['curr-health'] <= 0:
            return render_template('game_over.html')
        if data[d_]['curr-health'] <= 0:
            killed = True
        tmp = attacker
        attacker = attacked
        attacked = tmp
        print(monstersAlive())
        if not monstersAlive():
            return render_template('winner.html')
        print(killed)
        if killed:
            return play(killed = True)
        player = "2"
        question = "-3"
        answer = None
        topic = "-1"
        args = [player, question, answer, topic, attacker, attacked]
        return playing(skip = True, args = args)
    elif player == "2" and question != None and answer != None and topic != "-1":
        # Show answer
        topic = 'HTML' if topic == "1" else 'CSS'
        with open(f'static/questions/{topic.lower()}.json') as f:
                data = json.load(f)
        ai = data[f'questions{question}']['answer']
        correct = 'Correct' if int(answer) == ai else 'Wrong'
        difficulty = data[f'questions{question}']['difficulty']
        answer = data[f'questions{question}']['possibilities'][ai]
        return play(answer_=True, topic='ANSWER', difficulty=difficulty,
                    answer=answer, correct=correct, attacker=attacker, attacked=attacked)
    
    print(player)
    print(question)
    print(answer)
    print(topic)
    return rules()


if __name__ == '__main__':
    app.run(debug=True, host=IP, port=PORT)
