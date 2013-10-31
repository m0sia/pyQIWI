# -*- coding: utf-8 -*-
import sys, httplib
import xml.dom.minidom
import time

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

class Transaction(object):
	def __init__(self, xml):
		if xml.getAttribute("d")== "+":
			self.income = True
		else:
			self.income = False

		self.time = time.strptime(xml.getAttribute("t").encode("utf-8"), '%d.%m.%Y %H:%M:%S')
		self.amount = float(xml.getAttribute("s").encode("utf-8"))
		self.comment = xml.getAttribute("cmnt").encode("utf-8")
		self.id = int(xml.getAttribute("id").encode("utf-8"))

class QIWI(object):
	def __init__(self,user,token,udid):
		self.user = user
		self.token = token
		self.udid = udid
		
	def GetBalance(self):
		XML_REQUEST =  """<?xml version="1.0" encoding="utf-8"?>
		<request>
		<request-type>3</request-type>
		<extra name="client-software">Android v1.15.2 QIW</extra>
		<terminal-id>%s</terminal-id>
		<extra name="token">%s</extra>
		<extra name="udid">%s</extra>
		</request>
		""" % (self.user,self.token,self.udid)
		res = self.SendXML(XML_REQUEST)
		dom = xml.dom.minidom.parseString(res)
		balance = dom.getElementsByTagName("bal")[0].childNodes
		return getText(balance)

	def GetIncome(self,period="today"):
		XML_REQUEST =  """<?xml version="1.0" encoding="utf-8"?>
		<request>
		<request-type>54</request-type>
		<extra name="client-software">Android v1.15.2 QIW</extra>
		<terminal-id>%s</terminal-id>
		<extra name="token">%s</extra>
		<extra name="udid">%s</extra>
		<period>%s</period>
		<full>1</full>
		</request>
		""" % (self.user,self.token,self.udid,period)
		res = self.SendXML(XML_REQUEST)
		dom = xml.dom.minidom.parseString(res)
		transactions = dom.getElementsByTagName("p")
		result = []
		for node in transactions:
			result.append(Transaction(node))
		return result

	def SendXML(self,xml):
		webservice = httplib.HTTPS("www.mobw.ru")
		webservice.putrequest("POST", "/term2/xmlutf.jsp")
		webservice.putheader("Content-type", "text/xml; charset=\"UTF-8\"")
		webservice.putheader("Content-length", "%d" % len(xml))
		webservice.endheaders()
		webservice.send(xml)

		statuscode, statusmessage, header = webservice.getreply()
		res = webservice.getfile().read()
		return res
		
