#LED that is connected to RPi breadboard, switch accessible via LAN

# make_server is used to create this simple python webserver
from wsgiref.simple_server import make_server

# import Raspberry Pi gpio support into python
import RPi.GPIO as GPIO
# import a sleep function from time module
from time import sleep

led = 18  # gpio number where the led is connected

# Tell the GPIO module to use gpio numbering used by cpu
GPIO.setmode(GPIO.BCM)
# Set gpio nr 18 to output mode
GPIO.setup(led, GPIO.OUT)
led_state = 0

# Function that is ran when a http request comes in
def simple_app(env, start_response):
    global led_state
    # set some http headers that are sent to the browser
    status = '200 OK'
    headers = [('Content-type', 'text/html')] 
    start_response(status, headers)

    # What did the user ask for?
    if env["PATH_INFO"] == "/on":
        print("GPIO.output(led, False")
        return "got on"
	GPIO.output(led, False)

    elif env["PATH_INFO"] == "/off":
        print("user asked for /off")
        return "got off"
	GPIO.output(led, True)

    elif env["PATH_INFO"] == "/switch":
	if led_state == 0:
		GPIO.output(led, True)
		led_state = 1
	else:
		GPIO.output(led, False)
		led_state = 0
	return "<a href='/switch'>ON / OFF</a>"
    else:
        print("user asked for something else")
        return "<a href='/switch'>ON / OFF</a>"

# Create a small python server
httpd = make_server("", 8000, simple_app)
print "Serving on port 8000..."
print "You can open this in the browser http://192.168.1.154:8000"
httpd.serve_forever()
