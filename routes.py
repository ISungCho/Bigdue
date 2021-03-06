import sys
import os
import json
from flask import Flask, render_template, request, jsonify
from threading import Thread
from app.bigdue_app import main
from app.bigdue_app import Export_csv_file
from app.bigdue_app import WiresharkParsing
from app.makecsv import main as maincsv
from app.makecsv import Read_packet

app = Flask(__name__)      

def get_csv_list():
  csvlist = list()
  file_path = os.getcwd()+'/static/data/packet/'
  for file in os.listdir(file_path):
    if file.endswith('.csv'):
        csvlist.append(file)

  csvlist.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
  return csvlist

def get_wireshark_list():
  csvlist = list()
  file_path = os.getcwd()+'/static/data/wireshark/'
  for file in os.listdir(file_path):
    if file.endswith('.csv'):
        csvlist.append(file)

  csvlist.sort(key=lambda f: str(''.join(filter(str.isalpha, f))))
  return csvlist

def get_pcap_list():
    pacplist = list()
    file_path = os.getcwd()+'/static/wiresharkFolder/'
    for file in os.listdir(file_path):
        if file.endswith('.pcap'):
            pacplist.append(file)

    pacplist.sort(key=lambda f: str(''.join(filter(str.isalpha, f))))
    return pacplist

def get_previous_file():
  previousfile = ''
  file_path = os.getcwd()+'/static/data/time'
  for file in os.listdir(file_path):
    if file.endswith('.csv'):
      previousfile = file

  return str(previousfile).split('_')[0]

@app.route('/')
def home():
  timestamp_array = get_csv_list()
  wireshark_list = get_wireshark_list()
  pcap_list = get_pcap_list()
  previous_file_name = get_previous_file()
  # values from JS for selected timestamp
  first = request.args.get('first')
  last = request.args.get('last')
  timestamp = request.args.get('current_timestamp')

  # value from JS for selected .pcap files
  pcap = request.args.get('pcap')

  # value from JS for selected .csv files
  csv = request.args.get('selected_csv')
  
  if not pcap == None:
    pcap_array = json.loads(pcap)
    WiresharkParsing.main(pcap_array)
    print(pcap_array)

  if not csv == None:
    csv_array = json.loads(csv)
    print("file list : "+ str(csv_array) + " filename: " + timestamp)
    maincsv.main([csv_array, timestamp])
    print("----- All csv file writting end -----")

  if not first == None:
    print("start: " + first + ", " + "end: " + last + ", " + "filename: " + timestamp)
    maincsv.main([first, last, timestamp])
    print("----- All csv file writting end -----")
    
  return render_template(
    'home.html',
    title = 'Main',
    timestamp = timestamp_array,
    pcapfilelist = pcap_list,
    wiresharkfiles = wireshark_list,
    previousfile = previous_file_name)

@app.route('/raw_data')
def rawData():
  timestamp_array = get_csv_list()
  return render_template(
    'raw_data.html',
    title = 'Raw Data',
    timestamp = timestamp_array)

@app.route('/graph')
def graph():
  return render_template(
    'graph.html',
    title = 'Graph')

@app.route('/map')
def map():
  return render_template(
    'map.html',
    title = 'Map')

@app.route('/bubble')
def bubble():
  return render_template(
    'bubble.html',
    title = 'Bubble')

@app.route('/timeGraph')
def timeGraph():
  return render_template(
    'timeGraph.html',
    title = 'Time - Graph')

if __name__ == '__main__':
  t1 = Thread(target = main.main)
  t1.setDaemon(True)
  t1.start()

  t2 = Thread(target = app.run)
  t2.setDaemon(True)
  t2.start()
  while True:
    if not t1.isAlive():
      print("Program Exit")
      sys.exit(0)
    pass