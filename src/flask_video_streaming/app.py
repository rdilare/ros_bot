#!/usr/bin/env python2


from flask import Flask, render_template, Response
from pi_camera import Camera
from flask_socketio import SocketIO, emit
from velocity_publisher import vel_publisher

import rospy

app = Flask(__name__)
socketApp=SocketIO(app)


data={'vel':0, 'omega':0}


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


    
@app.route("/")
def index():
	return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')




@socketApp.on('connect')
def test_connect():
    print("got a message on connect")
    emit('after_connect', {'data':"Lets Dance!!!"})


@socketApp.on('value changed')
def changed(message):
    global data
    if message==0:
        data = {"vel":0,"omega":0}
    else :
        data['vel'] += float(message['vel'])
        data['omega'] += float(message['omega'])  
    
    data['vel']=max(-10,min(data['vel'],10))
    data['omega']=max(-10,min(data['omega'],10))
    vel_publisher(data['vel'],data['omega'])
    emit('update value', data, broadcast=True)





def main():
	socketApp.run(app,host="192.168.43.150", port="5000",debug=True)

if __name__=="__main__":
	rospy.init_node("webapp", anonymous=True)
	main()
	#rospy.spin()
