from flask import Flask, jsonify
from storage import liked_articles, unliked_articles, all_articles
from content_filtering import get_recommendations
from demographic_filtering import output

app = Flask(__name__)
@app.route('/get-article')
def get_article():
    return jsonify({"article":all_articles[0], "status":"success"}), 200

@app.route('/liked-article', methods = ["POST"])
def liked_articles():
    article = all_articles[0]
    all_articles = all_articles[1:]
    liked_articles.append(article)
    return jsonify({"status":"success"})

@app.route('/unliked-article', methods = ["POST"])
def unliked_articles():
    article = all_articles[0]
    all_articles = all_articles[1:]
    unliked_articles.append(article)
    return jsonify({"status":"success"})

@app.route('/popular')
def popular_movies():
    article_data = []
    for article in output:
        i = {"link": article[0], 
             "title": article[1], 
             "language": article[2], 
             "events": article[3]}
        article_data.append(i)
    return jsonify({"data":article_data, "status":"success"})

@app.route('/content')
def content():
    rec_articles = []
    for liked_article in liked_articles:
        output = get_recommendations(liked_article[4])
        for article in output:
            rec_articles.append(article)
    import itertools 
    rec_articles.sort() 
    rec_articles = list(rec_articles for rec_articles,_ in itertools.groupby(rec_articles)) 
    article_data = [] 
    for recommended in rec_articles: 
        _d = { "link": recommended[0], "title": recommended[1], "language": recommended[2], "events": recommended[3]} 
        article_data.append(_d)
    return jsonify({"data":article_data, "status":"success"})

if(__name__=="__main__"):
    app.run()