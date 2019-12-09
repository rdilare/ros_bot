#!/usr/bin/env python2

from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit


from flask_video_streaming import app, socketApp
#from flask_video_streaming.camera import Camera
from flask_video_streaming.pi_camera import Camera
from velocity_publisher import vel_publisher
from image_publisher import img_publisher


import rospy

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
		frame, arrayFrame = camera.get_frame()
		img_publisher(arrayFrame)
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
	#socketApp.run(app,host="192.168.43.202", port="5000",debug=True)

if __name__=="__main__":
	try :
		rospy.init_node("webapp", anonymous=True)
		main()
		# rospy.spin()
		
	except rospy.ROSInterruptException:
		pass
