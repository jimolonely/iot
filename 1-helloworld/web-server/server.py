#-*-coding:utf-8-*-

from bottle import run,route

@route('/')
def index():
    return 'Hello World'

run(host='127.0.0.1',port=8080)
