import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import pickle
from wordcloud import WordCloud
from nltk.corpus import stopwords
import string
from nltk.stem.wordnet import WordNetLemmatizer




st.set_page_config(layout = 'wide')

st.markdown("""
    <style>
    .big-font {
        font-size:80px !important;
        text-align:center;
    }
    </style>
""", unsafe_allow_html=True)
st.markdown('<p class="big-font">Final Notebook</p>', unsafe_allow_html=True)

option = st.selectbox(
     'Select the map you want to see:',
     #('Daily Confirmed Cases', 'Daily Deaths', 'Aggregated Confirmed Cases', 'Aggregated Deaths'))
     ('Correlation, comparisons, and trends', 'Distributions and part-to-whole', 'Geospatial', 'Concepts and qualitative'))

if (option == 'Correlation, comparisons, and trends'):
    # Take input from the excel file and load it to a dataframe
    df = pd.read_excel('Assignment_Files/Data/forestfires.xlsx')
    
    # Convert the month column from string to int
    df["month"].replace({"jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6, "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12}, inplace=True)
    df["month"] = df["month"].astype(int)
    
    
    var = st.multiselect(
     "Select variable(s):",
     ['FFMC', 'DMC', 'DC', 'ISI', 'temp', 'RH', 'wind', 'rain', 'area'],
     ['FFMC', 'DMC', 'DC', 'ISI', 'temp', 'RH', 'wind', 'rain', 'area'])
    
    if(len(var)==0):
        st.write('Select variable(s) to proceed!')
    else:
        preVar = ['X', 'Y', 'month', 'day']
        df = df[preVar+var]

        # Plot a pair plot color-coded by months to see if they show any relation
        fig = px.parallel_coordinates(df, color="month",
                                     color_continuous_scale=px.colors.diverging.Tealrose,
                                     color_continuous_midpoint=6, width=1500, height=800,
                                      title="Relations between weather/dryness variables while grouping them by month")
        st.plotly_chart(fig)
        
elif (option == 'Distributions and part-to-whole'):
    df = pd.read_excel('Assignment_Files/Data/forestfires.xlsx')
    df_sum = df.groupby(['month']).sum()
    
    bar = st.checkbox('Bar Plot', value=True)
    pie = st.checkbox('Pie Plot', value=True)
     

    c1, c2 = st.columns(2)
    if(bar):
        with c1:
            # Plot the aggregated area for each month to identify how devasting each month was?
            # Set the size of the plot for a high-resolution plot and setup the fonts for ticks, legend, and title.
            df_area = df_sum[['area']]
            months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
            df_bar_plot = df_area.loc[months]
            x = df_bar_plot.index.tolist()
            y = df_bar_plot['area'].tolist()
            x_pos = np.arange(len(x))
            print(x_pos)
            plt.figure(figsize=(20, 20), dpi=500)
            
            plt.bar(x_pos, y, color=['lightcoral','lightskyblue','yellow','yellowgreen','grey','pink','blue','darkgreen','cyan','magenta','violet','gold'])
            plt.xticks(x_pos, x)
            plt.xticks(fontsize=18)
            plt.yticks(fontsize=18)
            #plt.legend(fontsize=18)
            plt.xlabel('\nMonth',fontsize=18)
            plt.ylabel('Burnt Area (HA)\n',fontsize=18)
            plt.title('Burnt Forest Area by Month\n',fontsize=35)
            plt.legend('',frameon=False)
            st.pyplot(plt)
    if(bar and pie):
        with c2:
            df_pie_plot = df_sum[['wind', 'area']]
            months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
            df_pie_plot = df_pie_plot.loc[months]
            x = df_pie_plot.index.tolist()
            y = df_pie_plot['area'].tolist()
            percent = [100*ey / sum(y) for ey in y]
            colors = ['lightcoral','lightskyblue','yellow','yellowgreen','grey','pink','blue','darkgreen','cyan','magenta','violet','gold']
            fig, ax = plt.subplots(figsize=(20,20))
            patches, texts = ax.pie(y, colors = colors, counterclock=False, startangle=-270, radius=1)
            labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(x, percent)]
            plt.title('Part-to-whole Distribution of\nForest Fire', loc='center',fontsize=35)
            
            plt.legend(patches, labels, title = 'Month', loc='center', bbox_to_anchor=(0,1),
                       fontsize=20, title_fontsize=25)
            st.pyplot(fig)
    if(not bar and pie):
        with c1:
            df_pie_plot = df_sum[['wind', 'area']]
            months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
            df_pie_plot = df_pie_plot.loc[months]
            x = df_pie_plot.index.tolist()
            y = df_pie_plot['area'].tolist()
            percent = [100*ey / sum(y) for ey in y]
            colors = ['lightcoral','lightskyblue','yellow','yellowgreen','grey','pink','blue','darkgreen','cyan','magenta','violet','gold']
            fig, ax = plt.subplots(figsize=(20,20))
            patches, texts = ax.pie(y, colors = colors, counterclock=False, startangle=-270, radius=1)
            labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(x, percent)]
            plt.title('Part-to-whole Distribution of\nForest Fire', loc='center',fontsize=35)
            
            plt.legend(patches, labels, title = 'Month', loc='center', bbox_to_anchor=(0,1),
                       fontsize=20, title_fontsize=25)
            st.pyplot(fig)
elif (option == 'Geospatial'):
    # import relevant data
    data=pd.read_csv("Assignment_Files/Data/zipcode_wise_tweet_count_IN.csv")
    # load the selected subset of the US map (shapefile) containin IN only.
    # I am using a backup of the partial shapefile.
    # If you want to learn more on how I selected the subset and did a backup, you may
    # want to go over this file: 'Assignments/Assignment5_6_8_9_10_11_12/ISLAM_SAMIUL.ipynb' on
    # my git hub repo.
    with open('Assignment_Files/Data/us_map.pickle', 'rb') as handle:
        us_map = pickle.load(handle)
    # merge them based on ZCTA5CE10 which is zip-code
    map_data = us_map.merge(data, on="ZCTA5CE10")
    map_data['log2_t_count'] = np.log2(map_data['t_count'])
    
    c1, c2, c3 = st.columns(3)
    with c2:
        log = st.radio(
            "Do you want to consider logrithmic value of number of tweets?",
            ('No', 'Yes'))
        
        var = 't_count'
        
        if(log=='No'):
            var = 't_count'
        else:
            var = 'log2_t_count'
        
        fig, ax = plt.subplots(1, figsize=(10, 10))
        fig.patch.set_facecolor('white')
        plt.xticks(rotation=90)
        plt.yticks(fontsize=50)
        map_data.plot(column=var, cmap="Reds", linewidth=1, ax=ax, edgecolor="0")
        plt.title('\n\nDistribution of Tweets Made from Indiana during 2014\nMap is Sub-divided into Zip Codes', fontdict = {'fontsize' : 17.5})
        bar_info = plt.cm.ScalarMappable(cmap="Reds", norm=plt.Normalize(vmin=0, vmax= max(map_data[var])))
        bar_info._A = []
        cbar = fig.colorbar(bar_info)
        cbar.ax.tick_params(labelsize=12.5)
        cbar.ax.set_ylabel('\n# of tweets\n', rotation=90, fontsize = 12.5)
        ax.axis("off")
        st.pyplot(fig)
    
elif (option == 'Concepts and qualitative'):
    # read tweets
    # IL has more than 20 million tweets. Working with those will require
    # a lot of time. To minimize that, I am using first 20,000 of those tweets here.
    # you may want to go over this file: 'Assignments/Assignment5_6_8_9_10_11_12/ISLAM_SAMIUL.ipynb' on
    # my git hub repo to use a larger set.
    df_tweets_il = pd.read_csv('Assignment_Files/Data/tweets_il_20k.csv')
    
    c1, c2, c3 = st.columns(3)
    with c2:
        nTweets = st.slider('Select number of tweets to use:', 100, 20000, 1000)
    df_tweets_il = df_tweets_il[0:nTweets]
    # clean the data
    stop = set(stopwords.words('english'))
    exclude = set(string.punctuation)
    lemma = WordNetLemmatizer()
    
    def clean(text):
        stop_free = ' '.join([word for word in str(text).lower().split() if word not in stop])
        punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
        normalized = ' '.join([lemma.lemmatize(word) for word in punc_free.split()])
        return normalized
    
    df_tweets_il['text_clean']=df_tweets_il['text'].apply(clean)
    
    # aggregate the cleaned tweeted text
    agg_tweets_il = df_tweets_il['text_clean'].str.cat(sep=' ')    
    
    
    with c2:    
        # generate wordcloud
        wordcloud = WordCloud(width=1920, height=1080).generate(agg_tweets_il)
        plt.figure(figsize=(12, 9), dpi=1200).patch.set_facecolor('xkcd:white')
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.title('Wordcloud of the tweets made from IL during 2014', fontsize = 20) # Instead of selecting 20 mil tweets,
                                                                # I am using first 20,000 of those to reduce runtime.
        st.pyplot(plt)
        #plt.show()    


















































