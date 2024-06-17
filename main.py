
from flask import Flask, render_template, request, redirect, url_for, make_response
import random
import json
from keras.models import load_model
import numpy as np
import pickle
import nltk
import os
from nltk.stem import WordNetLemmatizer
app = Flask(__name__)
app.secret_key = 'dsfowqdeqwkjdqwdqdjqwwq'


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('dashboard.html')


lemmatizer = WordNetLemmatizer()
model = load_model(os.path.join(app.static_folder, 'data', 'chatbot_model.h5'))
intents = json.loads(
    open(os.path.join(app.static_folder, 'data', 'intents.json')).read())
words = pickle.load(
    open(os.path.join(app.static_folder, 'data', 'words.pkl'), 'rb'))
classes = pickle.load(
    open(os.path.join(app.static_folder, 'data', 'classes.pkl'), 'rb'))


def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(
        word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence


def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return(np.array(bag))


def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list


def getResponse(ints, intents_json):
    if(len(ints) == 0):
        return 'Sorry I dont understand'
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag'] == tag):
            result = random.choice(i['responses'])
            break
    return result


def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res


# Creating GUI with tkinter
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         conn = connectDB()
#         mycursor = conn.cursor()
#         sql = 'SELECT * FROM users WHERE username = %s AND password = %s'
#         val = (username, password)
#         mycursor.execute(sql, val)
#         myresult = mycursor.fetchall()
#         if len(myresult) > 0 and myresult[0][1] == username and myresult[0][2] == password:
#             ressp = make_response(redirect(url_for('home')))
#             ressp.set_cookie('username', username)
#             return ressp
#         else:
#             session['login_error'] = 'Invalid Credentials'
#             return redirect(url_for('login'))
#     else:
#         return render_template('index.html')


# @app.route('/register', methods=['GET', "POST"])
# def register():
#     if request.method == "POST":
#         username = request.form['username']
#         password = request.form['password']
#         conn = connectDB()
#         sql = 'INSERT INTO users (username,password) VALUES (%s,%s)'
#         val = (username, password)
#         mycursor = conn.cursor()
#         mycursor.execute(sql, val)
#         # return mycursor.rowcount
#         conn.commit()
#         ressp = make_response(redirect(url_for('home')))
#         ressp.set_cookie('username', username)
#         return ressp
#     else:
#         return render_template('register.html')

@app.route('/api/chatresponse', methods=["POST"])
def response():
    if request.method == "POST":
        res = chatbot_response(request.json['msg'])
        return res


@app.route("/logout", methods=["POST"])
def logout():
    ressp = make_response(redirect(url_for('login')))
    ressp.set_cookie('username', '')
    return ressp


if __name__ == '__main__':
    app.run(debug=True)
