from flask import Flask, send_from_directory, render_template, request, redirect, url_for
from waitress import serve
from src.models.predictor import get_model
import pandas as pd

app = Flask(__name__, static_url_path="/static")

#input article options into this dataframe with same column names as how it started
options_df = pd.read_csv('app_test_df.csv')
print(options_df['article'])

OUTPUTS = ["POLITICS", "Thousands of children from Central America are apprehended at the U.S.-Mexico border each year . Donald Trump’s administration is following a blanket policy of referring for prosecution all people who cross illegally . The change means that authorities send parents to jails and their children to the same agency ."]

#Based off of just headline of dropdown, it returns the full data for that article in pandas df to be sent to "run_model" function
def article_data_from_headline(headline, options_df):
    data = options_df[options_df['headline']==headline]
    return data

@app.route("/")
def index():
    """Return the main page."""
    return send_from_directory("static", "index.html")

@app.route("/run_model", methods=["POST"])
def run_model():
    """ Use the ML model to make a prediction using the form inputs. """

    # Convert the data into just a list of values to be sent to the model
    headline = request.form.get("article_headline")
    
    #get the whole row of just the headline you want and put it in data variable
    data = article_data_from_headline(headline, options_df)
#     feature_values = extract_feature_values(data)
    print(data["article"]) # Remove this when you're done debugging

    # Send the values to the model to get a prediction
#     outputs = get_model(data)
    outputs = OUTPUTS
    print("within run_model:")
    print(outputs[0])
    print(outputs[1])
    print(data["authors"][0])
    print(data["date"][0])
    print(type(data["date"][0]))
    print(str(data["date"][0]))

    # Tell the browser to fetch the results page, passing along the prediction
    return redirect(url_for("show_results", topic = outputs[0], summary=outputs[1], article=data["article"][0], headline=data["headline"][0], publish_date=data['date'][0], authors=data["authors"][0]))

@app.route("/show_results")
def show_results():
    """ Display the results page with the provided prediction """
    
    # Extract the prediction from the URL params
    topic = request.args.get("topic")
    summary = request.args.get("summary")
    article = request.args.get("article")
    headline = request.args.get("headline")
    authors = request.args.get("authors")
    publish_date = request.args.get("publish_date")
    
    print("within show_results:")
    print(topic)
    print(summary)
    print(headline)
    print(authors)
    print(publish_date)
#     print(publish_date)
    print(article[:30])
    

    # Return the results pge
    return render_template("results.html", topic=topic, summary=summary, article=article, headline=headline, publish_date=publish_date, authors=authors)


if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=5000)
