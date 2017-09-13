#-*-coding:utf-8-*-

from bottle import run,route

@route('/')
def index():
    return 'Hello World'

cmd = 0

@route('/writecmd/<command>')
def write_cmd(command):
    global cmd
    cmd = command
    return str(cmd)

@route('/getcmd')
def get_cmd():
    return str(cmd)

if __name__=='__main__':
    run(host='127.0.0.1',port=8080)

