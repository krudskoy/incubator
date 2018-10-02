from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import os, subprocess
import hashlib
from io import BytesIO
import cgi
import psutil

process = psutil.Process(os.getpid())
cred = "99adc231b045331e514a516b4b7680f588e3823213abe901738bc3ad67b2f6fcb3c64efb93d18002588d3ccc1a49efbae1ce20cb43df36b38651f11fa75678e8"

pid = open("server_pid", "w+")
pid.write(str(process.pid))
pid.close()

PORT_NUMBER = 80


def get_headline():

    mem = str(process.memory_info().rss)
    cpu = str(process.cpu_percent())
    git_commit = subprocess.Popen(["git rev-parse HEAD"], stdout=subprocess.PIPE, shell=True)
    (commit_out, commit_err) = git_commit.communicate()

    headline = "<html><center><b>Memory:</b> " + mem + "<b> CPU:</b> " + cpu + "<br><b> Commit:</b>" + str(commit_out) + "</center></html>"

    return headline
#test
#This class will handles any incoming request from
#the browser
class myHandler(BaseHTTPRequestHandler):

	#Handler for the GET requests
	def do_GET(self):
		if self.path=="/":
                    self.path="/index.html"


		try:
			#Check the file extension required and
			#set the right mime type

			sendReply = False
			if self.path.endswith(".html"):
				mimetype='text/html'
				sendReply = True
			if self.path.endswith(".jpg"):
				mimetype='image/jpg'
				sendReply = True
			if self.path.endswith(".gif"):
				mimetype='image/gif'
				sendReply = True
			if self.path.endswith(".js"):
				mimetype='application/javascript'
				sendReply = True
			if self.path.endswith(".css"):
				mimetype='text/css'
				sendReply = True

			if sendReply == True:
			    #Open the static file requested and send it
                                f = open(os.curdir + os.sep + self.path)
				self.send_response(200)
				self.send_header('Content-type',mimetype)
				self.end_headers()
                                self.wfile.write(get_headline())
				self.wfile.write(f.read())
				f.close()
			return

		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)

	#Handler for the POST requests

	def do_POST(self):
		if self.path=="/send":
			form = cgi.FieldStorage(
				fp=self.rfile,
			        headers=self.headers,
				environ={'REQUEST_METHOD':'POST',
		                 'CONTENT_TYPE':self.headers['Content-Type'],
			})

                try:


                        if hashlib.sha512(form["username"].value).hexdigest() == cred and hashlib.sha512(form["password"].value).hexdigest() == cred:
                            self.send_response(200)
                            self.end_headers()
                            self.wfile.write('<html><br><center><h1>Congratulations!</h1></center></html>')

                        else:
                            f = open(os.curdir + os.sep + 'index.html')
                            self.send_response(400)
                            self.end_headers()
                            response = BytesIO()
                            response.write(b'<html><font color="red"><center><h2>Login or password is incorrect</h2></center></font></html>')
                            response.write(get_headline())
                            self.wfile.write(response.getvalue())
                            self.wfile.write(f.read())
                            f.close()



                except:
                            f = open(os.curdir + os.sep + 'index.html')
                            self.send_response(400)
                            self.end_headers()
                            response = BytesIO()
                            response.write(b'<html><font color="red"><center><h2>Login or password is incorrect</h2></center></font></html>')
                            response.write(get_headline())
                            self.wfile.write(response.getvalue())
                            self.wfile.write(f.read())
                            f.close()



		return
try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER

	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()
