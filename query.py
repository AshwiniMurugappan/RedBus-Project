import streamlit as st
import pandas as pd
import mysql.connector as db

db_connection = db.connect(
    host = "localhost",
    user = "root",
    password = "Pink@2213",
    database = "redbusproject"
)
curr = db_connection.cursor()


def view_data():
    curr.execute('select * from bus_details')
    data = curr.fetchall()
    return data

def link():
    curr.execute('select * from routes')
    data = curr.fetchall()
    return data

def get_popular_cities():
    curr.execute("""
        SELECT route_name , COUNT(*) AS route_name_count
        FROM bus_details
        GROUP BY route_name
        ORDER BY route_name_count DESC;
    """)
    data = curr.fetchall()
    return data

def users(name, email, origincity, destcity, bustype):
    sql = "insert into users(name, email, origincity, destcity, bustype) values(%s, %s, %s, %s, %s)"
    val = (name, email, origincity, destcity, bustype)
    curr.execute(sql,val)
    db_connection.commit()

def update():
    curr.execute('select * from users')
    data = curr.fetchall()
    return data

def store_feedback(rating):
    sql = "INSERT INTO feedback (rating) VALUES (%s)"
    val = (rating,)
    curr.execute(sql, val)
    db_connection.commit()
    