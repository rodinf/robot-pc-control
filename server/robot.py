from tkinter import *
from tkinter import ttk
import serial
import string
import time
import os
import threading
import random
import hashlib
from flask import *
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

app.config['BOOTSTRAP_SERVE_LOCAL'] = True

def token_generate(length):
    letters = string.ascii_lowercase+string.digits
    return ''.join(random.choice(letters) for i in range(length))
real_token = token_generate(128)
webuser_username = 'robot'
webuser_password = token_generate(8)
real_token_text = 'password:   '+webuser_password

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
@app.errorhandler(403)
def access_forbidden(e):
    return render_template('403.html'), 403
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/')
@app.route('/index')
def index():
    
    if request.authorization and request.authorization.username == webuser_username and request.authorization.password == webuser_password: 
        token = {'token': real_token } 
        return render_template("index.html", token=token)
    return make_response('403 Forbidden', 401, {'WWW-Authenticate' : 'Basic realm="Login Required!"'})

def com_connect():
    try:
        global ser
        ser = serial.Serial(com.get(), var.get())
        time.sleep(3)
        print('Successfully connected to <{0}> !'.format(com.get()))
        bottom_label.config(text='Successfully connected to {0}!'.format(com.get()))
    except Exception:
        print('Error: Could not connect to <{0}> !'.format(com.get()))
        bottom_label.config(text='Could not connect to <{0}> !'.format(com.get()))

root = Tk()
root.title("Robot server")
root.geometry('360x100')
root.resizable(False, False)
imgicon = PhotoImage(file=os.path.join(os.path.realpath('icon.gif')))
root.tk.call('wm', 'iconphoto', root._w, imgicon)
'''
except Exception:
    print('Error: No device connected!')
    bottom_label.config(text='No device connected!')
'''
def no_conn_exeption():
    print('Error: No device connected!')
    bottom_label.config(text='No device connected!')

def stop(event):
    try:
        ser.write(b's')
    except:
        no_conn_exeption()

def move_left(event):
    try:
        ser.write(b'l')
        print("Moving Left!")
    except:
        no_conn_exeption()

def move_right(event):
    try:
        ser.write(b'r')
        print("Moving Right!")
    except:
        no_conn_exeption()

def move_forward(event):
    try:
        ser.write(b'f')
        print("Moving Forward!")
    except:
        no_conn_exeption()

def move_backward(event):
    try:
        ser.write(b'b')
        print("Moving Backward!")
    except:
        no_conn_exeption()

def about():
    top = Toplevel()
    top.title("About")
    top.geometry('300x150')
    msg = Message(top, text="«Robot Vasily server» v1.0 Beta by @badfedor, 2018. \n\n Use keys W, A, D, X \n to move forward, left, right, backward \n and key S to stop. \n\n Don't forget to check you're using english keymap! ", width=300)
    msg.pack()

def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combined_func

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="About", command=about)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)
imgicon_about = PhotoImage(file=os.path.join(os.path.realpath('icon.gif')))
menubar.tk.call('wm', 'iconphoto', menubar._w, imgicon_about)
root.config(menu=menubar)

frame_com = Frame(root, bd=0)
com = ttk.Entry(frame_com, width=20)
com.pack(side=LEFT)
var = StringVar(root)
option = ttk.OptionMenu(frame_com, var, 300, 1200, 2400, 4800, 9600, 19200, 38400, 57600, 74880, 115200, 230400, 250000, 500000, 1000000, 2000000)
var.set(9600)
option.config(width=6)
option.pack(side=LEFT)
com_button = ttk.Button(frame_com, text="Connect", command=com_connect, width=10)
com_button.pack(side=TOP)

bottom_label = Label(root, text="", bd=5)
bottom_token = Label(root, text=real_token_text, bd=5)
frame_com.pack(side=TOP)
bottom_token.pack()
bottom_label.pack(side=LEFT)

root.bind("<w>", move_forward)
root.bind("<a>", move_left)
root.bind("<d>", move_right)
root.bind("<x>", move_backward)
root.bind("<s>", stop)

@app.route('/control', methods = ['GET'])
def moving():
    global real_token
    token = request.args.get('token')
    move = request.args.get('move')
    if(token == real_token):
        if(move == 'l'):
            try:
                ser.write(b'l')
                print('Moving left') 
                data = {'move' : 'left'}
            except:        
                print('Cannot move! Please check connection.')    
                data = {'error' : '2'}
        elif(move == 'r'):
            try:
                ser.write(b'r')
                print('Moving right') 
                data = {'move' : 'right'}
            except:        
                print('Cannot move! Please check connection.')    
                data = {'error' : '2'} 
        elif(move == 'f'):
            try:
                ser.write(b'f')
                print('Moving forward') 
                data = {'move' : 'forward'}
            except:        
                print('Cannot move! Please check connection.')    
                data = {'error' : '2'}
        elif(move == 'b'):
            try:
                ser.write(b'b')
                print('We`re going backwards, ignoring the realities...') 
                data = {'move' : 'back'}
            except:        
                print('Cannot move! Please check connection.')    
                data = {'error' : '2'}
        elif(move == 's'):
            try:
                ser.write(b's')
                print('Stopping') 
                data = {'move' : 'left'}
            except:        
                print('Cannot move! Please check connection.')    
                data = {'error' : '2'}  
        else:
            data = {'error' : '1'}
    else:
        abort(404)

    js = json.dumps(data)
    resp = Response(js, status=200, mimetype='application/json')
    return resp

def flask_start():
    app.run('0.0.0.0', port='8080')

def tkinter_start():
    root.mainloop()

if __name__ == "__main__":
    flt = threading.Thread(target=flask_start)
    flt.daemon = True
    flt.start() 
    tkinter_start() 

"""
execfile('robot.py')
def toggle_entry():
    global hidden
    if hidden:
        e.grid()
    else:
        e.grid_remove()
    hidden = not hidden

hidden = False
root = Tk()
e = Entry(root)
e.grid(row=0, column=1)
Button(root, text='Toggle entry', command=toggle_entry).grid(row=0, column=0)
root.mainloop()

"""
