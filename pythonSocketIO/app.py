import socketio

sio = socketio.Server('http://192.168.1.47')
app = socketio.WSGIApp(sio, static_files={
   '/': '/home/pi/vue3-doorbell-receiver/public/'
})

@sio.event
def connect(sid, environ):
   print(sid, 'connect')
   
@sio.event
def disconnect(sid):
   print(sid, 'disconnected')
