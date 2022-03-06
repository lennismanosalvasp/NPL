import streamlit as st
import tweepy
from textblob import TextBlob
from wordcloud import WordCloud
import pandas as pd
import preprocessor as p
import nltk
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
from PIL import Image
import re
import plotly.express as px
from user import df_tweet
from datetime import date
from datetime import datetime
import streamlit.components.v1 as components


#from pysentimiento import create_analyzer
#analyzer = create_analyzer(task="sentiment", lang="es")

nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('stopwords')

#Removing stopwords
stop = nltk.corpus.stopwords.words('spanish')
plt.style.use('fivethirtyeight')

consumer_key = 'UjYQZT9P9vdYq6OzEFPsqSLQB'
consumer_secret = 'LWKnd023OSmb6kfTbDd5zPjo4P0LcQodvg1wRf7LynWCgOH8Nb'
access_token = '384431766-SdZnMYaETCYPiI6NyogMtZSEZq95dAYqZyDNkWhU'
access_token_secret = '5GD2CpP3Bt3ZvsCjiMV0LvkNnh5oBiJiEeJNW9lzdQ38o'

st.set_option('deprecation.showPyplotGlobalUse', False)
p.set_options(p.OPT.URL, p.OPT.RESERVED,p.OPT.NUMBER)

#Create the authentication object
authenticate = tweepy.OAuthHandler(consumer_key, consumer_secret) 
    
# Set the access token and access token secret
authenticate.set_access_token(access_token, access_token_secret) 
    
# Creating the API object while passing in auth information
api = tweepy.API(authenticate, wait_on_rate_limit = True)

n = 350
    
def app():
    st.title("Tu año en Twitter 🔥")
    st.info('Estoy todavía en fase beta, trátame bonito y con cariño')
    st.subheader("Veamos como fueron tus tweets durante el 2021")
    raw_text = st.text_area("Escribe tu nombre de usuario (sin la @)")
    
    if st.button("Analizar"):
        texto = "Analizando los últimos " +  str(n) +" tweets del 2021"
        st.success(texto)
        
        def datos_usuario(raw_text):
            try:
                datos = api.get_user(raw_text) 
                st.write("Nombre: ",datos.name)
                st.write("Descripción: ",datos.description)    
                col1, col2 = st.columns(2)
                col1.metric("Leen tus tweets:", datos.followers_count)
                col2.metric("Lees tweets de tantos usuarios:", datos.friends_count)
                
                fecha = datos.created_at.year
                print(fecha)
                fecha = date.today().year - fecha
                print(fecha)
                html_str = f"""Llevas escribiendo <div style="color:red;font-size:35px;">{ fecha * 12 } meses</div> que obvio es lo mismo que <div style="color:red;font-size:35px;">{fecha} años</div>"""
                st.markdown(html_str, unsafe_allow_html=True)
            except:
                pass   
        def Show_Recent_Tweets(raw_text):
            # Extract 3200 tweets from the twitter user 
            with st.spinner('Metiendo todo la info en una licuadora...'):
                posts = tweepy.Cursor(api.user_timeline, screen_name = raw_text, include_rts = False,tweet_mode="extended").items(n)
                usuario = df_tweet(posts)        
            return usuario   

        df = Show_Recent_Tweets(raw_text)
                
        df["fecha"] =df['created_at'].dt.strftime('%m/%d/%Y')
        df["anio"] = df['created_at'].dt.strftime('%Y')
        df["mesnombre"] = df['created_at'].dt.strftime('%b')
        df["mes"] = df['created_at'].dt.strftime('%m')
        
        df = df[df["anio"].astype(int)>=2021].copy()
        st.success("¡LISTO!")
        
        st.subheader("Estos son tus datos")
        datos_usuario(raw_text)
        
        st.subheader("Palabras más usadas")
        
        def gen_wordcloud():
			# word cloud visualization
            allWords = ' '.join([twts for twts in df['Tweets']])
            allWords = p.clean(allWords)
            wordCloud = WordCloud(width=700, height=500, random_state=21, max_font_size=110,stopwords=stop).generate(allWords)
            plt.imshow(wordCloud, interpolation="bilinear")
            plt.axis('off')
            plt.savefig('WC.jpg')
            img= Image.open("WC.jpg") 
            return img
        
        try:
            img=gen_wordcloud()
            st.image(img,width=700)
        except:
            st.write("Parece que el trabajo te ha tenido ocupado y no tenemos tweets !!")
        
        
        st.subheader("Hashtag más utilizados")
        
        try:
            hashtags = df['Tweets'].apply(lambda x: pd.value_counts(re.findall('(#\w+)', x.lower() )))\
                .sum(axis=0).to_frame().reset_index().sort_values(by=0,ascending=False)
            hashtags.columns = ['hashtag','occurences']
            fig = px.bar(hashtags, x='hashtag', y='occurences')
            st.plotly_chart(fig) 
        except:
            st.write("No has escrito mucho que digamos este año")
        
        
        st.subheader("Con quién hablé más")
        
        try:
            usuarios = df['Tweets'].apply(lambda x: pd.value_counts(re.findall('(@\w+)', x.lower() )))\
            .sum(axis=0)\
            .to_frame()\
            .reset_index()\
            .sort_values(by=0,ascending=False)
            usuarios.columns = ["usuarios","interacciones"]
            usuarios["interacciones"] = usuarios["interacciones"].astype(int)
        
            col1, col2= st.columns(2)
            col1.metric(label="El total de personas que conversé ", value=usuarios.shape[0])
            col2.metric("Interacciones que tuve con mi mejor amigo en twitter", int(usuarios["interacciones"][:1].values))    
     
            html_str = f"""<br>No paré de conversar con <div style="color:red;font-size:35px;">{usuarios.iloc[0].iat[0]}</div>"""
            st.markdown(html_str, unsafe_allow_html=True)
        
            usuario = usuarios.iloc[0].iat[0]
            texto = "<a href=""https://twitter.com/" +usuario+ "?ref_src=twsrc%5Etfw"" class=""twitter-follow-button"" data-lang=""es"" data-show-count=""false"">Follow " +usuario+"</a><script async src=""https://platform.twitter.com/widgets.js"" charset=""utf-8""></script>"

            components.html(texto,height= 100)
            st.subheader("Mi top ten de conversones")
        
            st.table(usuarios.set_index("usuarios").head(10))
        
            #Actividad
            st.subheader("¿ Qué tan activo estuviste este año 2021?")
            df.sort_values("mes",ascending=False, inplace=True)
            usuario = df.groupby("mes")["Tweets"].count()
            fig = px.line(usuario, x=usuario.index, y='Tweets')
            st.plotly_chart(fig)
        
            #Popularidad
            st.subheader("¿ Cuál fue tu tweet más compartido ?")
        
            maximo = df["retweet_count"].max() 
            tweet_id = df[df["retweet_count"]==maximo].head(1)
            tweet_id = tweet_id["status_id"].values
            st.metric("Cantidad de RT's",int(maximo))
            result = api.get_oembed(int(tweet_id)) # , omit_script=True
            html = result['html'].strip()
        
            components.html(html,height= 1000)
        except:
            st.write("Te han faltado amigos, porque no empiezas a seguir más personas y hablar más")
        
        
        st.caption("Powered by Masapp")
        st.image("https://pbs.twimg.com/profile_images/1299512515802656768/Pg9L4yt8_400x400.jpg")
        link = '[Ir a la web](http://www.masappec.com)'
        st.markdown(link, unsafe_allow_html=True)
        
if __name__ == "__main__":
	app()