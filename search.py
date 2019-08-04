import pandas as pd
import difflib
import json
from flask import Flask, request, render_template

app = Flask(__name__, template_folder='./templates')
@app.route("/search", methods=['GET'])
def fuzzySearch():
    search_word = request.args.get('word') #read query string from here
    tp_df = pd.DataFrame()
    df = pd.read_csv("word_search.tsv", sep='\t', names=["word", "count"]) #Read .tsv file through pandas function
    df["word"] = df["word"].apply(lambda x: str(x)) #Here I converted word list to string
    searched_df = difflib.get_close_matches(search_word, df["word"], n=25) #Searched close matches of given word and resolved constraint 1 and 2(a, b)
    tp_df["word"] = searched_df
    tp_df["count"] = [df["count"][searched_df.index(item)] for item in searched_df]
    tp_df = tp_df.sort_values(["count"], ascending = False)
    return tp_df['word'].to_json(orient='records') #Final json result of top 25 word

@app.route("/", methods=['GET'])
def home_page():
    return render_template('srch.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000)
