#!/usr/bin/env python
# coding: utf-8

# In[3]:


import streamlit as st
from streamlit.components.v1 import html
import pika
import redis
from PIL import Image

image = Image.open('sample.png')

url = st.secrets["rabbitmq_url"]


            
st.title("Get a YouTube channel's Stats")
st.markdown("With this app you can get a Youtube channel stats (each videos likes,dislikes, views etc):")
st.markdown("Input a valid channel link, example: https://www.youtube.com/channel/UC7eF1vkUfzHAoku19ZXfLug/videos")
st.write('Validation is not complete but a little is in place')

label = 'Enter Youtube channel Link'
title = st.text_input(label, '')
email = st.text_input('Email', '')

def mailer(email):
    my_js = f"""
            alert('An email will be sent to {email} with data as attachement');
            """

    # Wrapt the javascript as html code
    my_html = f"<script>{my_js}</script>"

    html(my_html)
    
def process():
    print(title.startswith('https://www.youtube.com/'))
    print('.com' in email)
    print('@' in email)
    
    if title.startswith('https://www.youtube.com/') and '.com' in email and '@' in email:
        r = redis.Redis(
          host= st.secrets["redis_host"],
          port=19542,
          password= st.secrets["redis_password"])

        params = pika.URLParameters(url)
        
        connection = pika.BlockingConnection(params)
        channel = connection.channel() # start a channel
        #check if the key exists 
        value = r.get(title)
        #get data from s3 and send to email
        if False: #value:
            st.write('A request has been recently for this same channel, so the data will be sent to you. PS, it might be hours old')
            mailer(email)
        else:
            #set if it doesnt exist and send to queue
            #r.set(title,'s3 address')
        
       
        
            # channel.queue_declare(queue='youtube') # Declare a queue
            channel.basic_publish(exchange='',
                                  routing_key='newYoutube',
                                  body=f"[{title},{email}]")

            print(" Sent to queue")
            connection.close()
            # Define your javascript
            mailer(email)
    else:
        st.write('Input a youtube channel link, gboran')
        
    
    
but = st.button('Submit Request')

if but:
    process()


st.image(image, caption='Sample of the data you\'d be receiving')
