import time
import streamlit as st
import requests
import pymysql
import pymysql.cursors
from flask import Flask, jsonify, render_template
from datetime import datetime

################################################### STREAMLIT ###################################################


st.set_page_config(page_title="장재혁 AI", 
               page_icon=":robot_face:",
               layout="wide",
               initial_sidebar_state="expanded"
               )

# MySQL 데이터베이스 연결 설정
mydb = pymysql.connect(host="localhost",
                       user="root",
                       password="1234",
                       database="mydatabase")
mycursor = mydb.cursor(pymysql.cursors.DictCursor)

def p_title(title):
    st.markdown(f'<h3 style="text-align: left; color:#F63366; font-size:28px;">{title}</h3>', unsafe_allow_html=True)

def s_title(title):
    st.markdown(f'<h4 style="text-align: left; color:#F63366; font-size:15px;">{title}</h4>', unsafe_allow_html=True)

def p_title_blue(title):
    st.markdown(f'<h3 style="text-align: left; color:#2E2EFE; font-size:28px;">{title}</h3>', unsafe_allow_html=True)    

def insert_data(temperature, humidity, current_time, mach_cd):
    sql = "INSERT INTO test_table (temperature, humidity, date_time, device_num) VALUES (%s, %s, %s, %s)"
    val = (temperature, humidity, current_time, mach_cd)
    mycursor.execute(sql, val)
    mydb.commit()

def fetch_data():
    try:
        temperature_response = requests.get('http://192.168.0.106:5000/api/temperature')
        humidity_response = requests.get('http://192.168.0.106:5000/api/humidity')
        current_time_response = requests.get('http://192.168.0.106:5000/api/current_time')

        temperature = temperature_response.json().get('temperature')
        humidity = humidity_response.json().get('humidity')
        current_time = current_time_response.json().get('current_time')

        # Streamlit에 데이터 표시
        st.write(f"온도: {temperature} °C")
        st.write(f"습도: {humidity} %")
        st.write(f"현재시간: {current_time}")

        insert_data(temperature, humidity, current_time, 'test01')
    
    except Exception as e:
        st.error(f"오류 발생: {e}")

########
# SIDEBAR
########

st.sidebar.header('My AI Service :crystal_ball:')
st.sidebar.header('IOT 활용 온/습도 감지 및 조절')

nav = st.sidebar.radio('',['idea','온/습도 현황', '온/습도 추이'])
st.sidebar.write('')
st.sidebar.write('')

if nav == 'idea':
    st.markdown("<h4 style='text-align: center; color:grey;'>streamlit 소스 코드 제공 restAPI &#129302;</h4>", unsafe_allow_html=True)
    st.text('')
    p_title_blue('아이디어 설명')
    image_path = "C:/Users/KDP-010/GSW/실무/idea1.png"  # 이미지 파일 경로를 여기에 입력하세요.

    # 이미지 삽입
    st.image(image_path, caption="", use_column_width=True)
    st.markdown('___')

if nav == '온/습도 현황':
    st.markdown("<h4 style='text-align: center; color:grey;'>streamlit 소스 코드 제공 restAPI &#129302;</h4>", unsafe_allow_html=True)
    st.text('')
    p_title_blue('온도, 습도 현황')

    st.markdown('___')

    # 데이터 가져오기 버튼 추가
    if st.button('데이터 가져오기'):
        fetch_data()

    st.markdown('___')