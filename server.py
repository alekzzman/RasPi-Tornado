import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.gen as gen
import tornado_mysql
import json 
import RasPi
import os
from subprocess import Popen, PIPE
class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("index.html")

class LoginHandler(tornado.web.RequestHandler):
	@gen.coroutine
	def post(self):
		login = self.get_argument('login', '')
		password = self.get_argument('password', '')
		response = {}
		try:
			conn = yield tornado_mysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123', db='raspberry', charset='utf8')
			cur = conn.cursor()
			yield cur.execute("SELECT count(*) FROM users WHERE login = %s AND password = %s", 
				(login, password))
			if cur.fetchone()[0]:
				response = {
					'error': False,
					'page': open("home.html", "r").read()
				}
			else:
				response = {
					'error': True,
				}
			cur.close()
			conn.close()
		finally:
			self.write(response)

class OnHandler(tornado.web.RequestHandler):
	@gen.coroutine
	def post(self):
		pin = self.get_argument('pin', '')

		RasPi.relay_on(pin)

		self.write({'pin': pin})

class OffHandler(tornado.web.RequestHandler):
	@gen.coroutine
	def post(self):
		pin = self.get_argument('pin', '')

		RasPi.relay_off(pin)

		self.write({'pin': pin})

class TempHumHandler(tornado.web.RequestHandler):
	@gen.coroutine
	def get(self):
		res = RasPi.climate()

		self.write({'temp': res['temp'], 'hum': res['hum']})

class CameraOnHandler(tornado.web.RequestHandler):
	@gen.coroutine
	def get(self):
		Popen("./start.sh", shell=True, stdout=PIPE, stderr=PIPE)

class CameraOffHandler(tornado.web.RequestHandler):
	@gen.coroutine
	def get(self):
		Popen("./stop.sh", shell=True, stdout=PIPE, stderr=PIPE)

prev = False
curr = False
class MonitorHandler(tornado.web.RequestHandler):
	@gen.coroutine
	def get(self):
		result = RasPi.motionauto(prev, curr)

		self.write({"info": result['info']})

prevSec = False
currSec = False
class SecureOnHandler(tornado.web.RequestHandler):
	@gen.coroutine
	def get(self):
		result = RasPi.secure_on(prevSec, currSec)

		self.write({"info": result['info']})

class SecureOffHandler(tornado.web.RequestHandler):
	@gen.coroutine
	def get(self):
		result = RasPi.secure_off()

		self.write({"info": result['info']})

application = tornado.web.Application([
	(r"/", MainHandler),
	(r"/on", OnHandler),
	(r"/off", OffHandler),
	(r"/temp_hum", TempHumHandler),
	(r"/camera_on", CameraOnHandler),
	(r"/camera_off", CameraOffHandler),
	(r"/monitor", MonitorHandler),
	(r"/secure_on", SecureOnHandler),
	(r"/secure_off", SecureOffHandler),
	(r"/login", LoginHandler)],
	debug = True
)

if __name__ == "__main__":
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(80)
	tornado.ioloop.IOLoop.instance().start()
