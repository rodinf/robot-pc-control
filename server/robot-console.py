import serial, string, time, os, random, hashlib, logging, argparse
from flask import *
from flask_bootstrap import Bootstrap

ROBOT_VERSION = 'v1.1 Alpha'

app = Flask(__name__)
Bootstrap(app)

app.config['BOOTSTRAP_SERVE_LOCAL'] = True

parser = argparse.ArgumentParser()
parser.add_argument("serial_port", help="serial port address where robot is connected to", type=str)
parser.add_argument("serial_freq", help="serial port frequency", type=str)
args = parser.parse_args()

def token_generate(length):
    letters = string.ascii_lowercase+string.digits
    return ''.join(random.choice(letters) for i in range(length))
real_token = token_generate(128)
webuser_username = 'robot'
webuser_password = token_generate(8)
real_token_text = '\n-- PASSWORD:   '+webuser_password+'   --\n'

print('\n-- ROBOT VASILY SERVER '+ROBOT_VERSION+' -- \n '+real_token_text)

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

##def com_connect():
try:
    ##global ser, args
    ser = serial.Serial(args.serial_port, args.serial_freq)
    time.sleep(3)
    print('-- Successfully connected to <{0}> ! --\n'.format(args.serial_port))
except Exception:
    print('-- Error: Could not connect to <{0}> ! --\n'.format(args.serial_port))

def no_conn_exeption():
    print('-- Error: No device connected!')
    
def stop(event):
    try:
        ser.write(b's')
    except:
        no_conn_exeption()

def move_left(event):
    try:
        ser.write(b'l')
        print("-- Moving Left!")
    except:
        no_conn_exeption()

def move_right(event):
    try:
        ser.write(b'r')
        print("-- Moving Right!")
    except:
        no_conn_exeption()

def move_forward(event):
    try:
        ser.write(b'f')
        print("-- Moving Forward!")
    except:
        no_conn_exeption()

def move_backward(event):
    try:
        ser.write(b'b')
        print("-- Moving Backward!")
    except:
        no_conn_exeption()
		
def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combined_func

@app.route('/control', methods = ['GET'])
def moving():
    global real_token
    token = request.args.get('token')
    move = request.args.get('move')
    lights = request.args.get('lights')
    if(token == real_token):
        ## MOVE
        if(move == 'l'):
            try:
                ser.write(b'l')
                print('-- Moving left') 
                data = {'move' : 'left'}
            except:        
                print('-- Cannot move! Please check connection.')    
                data = {'error' : '2'}
        elif(move == 'r'):
            try:
                ser.write(b'r')
                print('-- Moving right') 
                data = {'move' : 'right'}
            except:        
                print('-- Cannot move! Please check connection.')    
                data = {'error' : '2'} 
        elif(move == 'f'):
            try:
                ser.write(b'f')
                print('-- Moving forward') 
                data = {'move' : 'forward'}
            except:        
                print('-- Cannot move! Please check connection.')    
                data = {'error' : '2'}
        elif(move == 'b'):
            try:
                ser.write(b'b')
                print('-- We`re going backwards, ignoring the realities...') 
                data = {'move' : 'back'}
            except:        
                print('-- Cannot move! Please check connection.')    
                data = {'error' : '2'}
        elif(move == 's'):
            try:
                ser.write(b's')
                print('-- Stopping') 
                data = {'move' : 'left'}
            except:        
                print('-- Cannot move! Please check connection.')    
                data = {'error' : '2'}  
        ## LIGHTS
        elif(lights == '1'):
            try:
                ser.write(b'e')
                print('-- Lights: ON') 
                data = {'lights' : '1'}
            except:        
                print('-- Cannot toggle lights! Please check connection.')    
                data = {'error' : '2'}  
        elif(lights == '0'):
            try:
                ser.write(b'r')
                print('-- Lights: OFF') 
                data = {'lights' : '0'}
            except:        
                print('-- Cannot toggle lights! Please check connection.')    
                data = {'error' : '2'} 
        else:
            data = {'error' : '1'}
    else:
        abort(404)

    js = json.dumps(data)
    resp = Response(js, status=200, mimetype='application/json')
    return resp

if __name__ == "__main__":
    app.run('0.0.0.0', port='8080')
