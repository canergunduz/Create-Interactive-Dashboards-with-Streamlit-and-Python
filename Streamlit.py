import streamlit as st
import pandas as pd
import numpy as np
import plotly_express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

st.title("Sentiment Analysis of Tweets about Airlines")
st.sidebar.title("bidibidi")

st.markdown("First dashboard")
st.sidebar.markdown("bidibidi")


DATA_URL = ("/home/rhyme/Desktop/Project/Tweets.csv")
@st.cache(persist=True)
def load_data():
    data = pd.read_csv(DATA_URL)
    data['tweet_created'] = pd.to_datetime(data['tweet_created'])
    return data

data = load_data()

st.sidebar.subheader("random")
random_tweet = st.sidebar.radio('Sentiment', ('positive','negative','neutral'))
st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[["text"]].sample(n=1).iat[0,0])


select = st.sidebar.selectbox('Viz type', ['Histogram', 'Pie chart'], key ='1')
sentiment_count = data['airline_sentiment'].value_counts()
sentiment_count = pd.DataFrame({'Sentiment': sentiment_count.index, 'Tweets': sentiment_count.values})

if not st.sidebar.checkbox("Hide", True):
    st.markdown('###number of tw')
    if select == "Histogram":
        fig = px.bar(sentiment_count, x= 'Sentiment', y = 'Tweets', color='Tweets', height=500)
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count, names= 'Sentiment', values = 'Tweets', height=500)
        st.plotly_chart(fig)


st.sidebar.subheader("When and Where tweets from")
hour = st.sidebar.slider("Hour", min_value = 1, max_value = 24)
modified_data = data[data['tweet_created'].dt.hour == hour]
if not st.sidebar.checkbox("Close", True, key = '1'):
    st.markdown("locations based on time")
    st.markdown("%i tweets between %i:00 and %i:00" % (len(modified_data), hour, hour+1))
    st.map(modified_data)
    if st.sidebar.checkbox("Show raw data", False):
        st.write(modified_data)

st.sidebar.subheader("Breakdown")
choice = st.sidebar.multiselect('Pick Airlines', ('US Airways', 'United', 'American','Soutwest','Delta'), key='0')

if len(choice) >0:
    choice_data = data[data.airline.    isin(choice)]
    fig_choice = px.histogram(choice_data, x = 'airline', y='airline_sentiment',
    histfunc='count', color = 'airline_sentiment', facet_col ='airline_sentiment')
    st.plotly_chart(fig_choice)

st.sidebar.header("Word Cloud")
word_sentiment = st.sidebar.radio('Display for sentiment',('positive','negative','neutral'))

if not st.sidebar.checkbox('Close', True, key='3'):
    st.header('Word cloud for %s sentiment' % (word_sentiment))
    df = data[data['airline_sentiment']== word_sentiment]
    words = ' '.join(df['text'])
    processed_words = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', height = 640, width = 800).generate(processed_words)
    plt.imshow(wordcloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot()