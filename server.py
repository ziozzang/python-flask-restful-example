#!/usr/bin/python3
##################################################
#
# Code by Jioh L. Jung <ziozzang@gmail.com>
#
##################################################

# Import Flask Restful API library
from flask import Flask, request, abort
from flask_restful import Resource, Api
from flask_restful import reqparse

# Import Password String Generator
import hashlib
import os

# Process JSON
import json

# Process Network Masking
from netaddr import IPNetwork, IPAddress

# Configuration Add from conf.py file
from conf import *

# for Debugging Purpose
import pickle

# for store ID/PW
import base64

####################################################
# Base Parameters
PARAMS = [
  "param1", # IP Allowed
]

####################################################
# Base Shared Connection.
app = Flask(__name__)
api = Api(app)


# Request Parsing
parser = reqparse.RequestParser()
parser.add_argument('param0')
for i in PARAMS:
  parser.add_argument(i)

####################################################
# IP Filtering Functions
# Get Real IP, Behind Reverse Proxy.
def get_real_ip():
  ipaddr = request.remote_addr
  if ("X-Forwarded-For" in request.headers.keys()
      and ipaddr != request.headers["X-Forwarded-For"]):
    ipaddr = request.headers["X-Forwarded-For"].strip()
  if ("X-Real-Ip" in request.headers.keys()
      and ipaddr != request.headers["X-Real-Ip"]):
    ipaddr = request.headers["X-Real-Ip"].strip()
  return ipaddr

# Check if IP is restricted
def check_allowed_ip():
  ipaddr = get_real_ip()
  for i in ALLOWED_FROM:
    if IPAddress(ipaddr) in IPNetwork(i):
      return True
  for i in DENYED_FROM:
    if IPAddress(ipaddr) in IPNetwork(i):
      return False
  return False

def abort_if_ip_not_allowed():
  if not  check_allowed_ip():
    detected_ip = get_real_ip()
    abort(403, "Your IP is not allowed to call API: (Detected IP - {})".format(detected_ip))

####################################################
class Some(Resource):
  def get(self, param0):
    abort_if_ip_not_allowed()
    return {'result': 'get'}
  
  def put(self, param0):
    abort_if_ip_not_allowed()
    return {'result': 'put'}

  def delete(self, param0):
    abort_if_ip_not_allowed()
    try:
      pass
    except:
      abort(404, "Failed - No such User")
    try:
      con.delete_s(dn) #,204
      return {'result':'delete'}
    except Exception as e:
      abort(500, "FAILED - %s" % (e.message,))



####################################################
api.add_resource(Some, '/Some/<string:param0>')

####################################################
if __name__ == '__main__':
  app.run(host=BIND_ADDR, debug=DEBUG)
