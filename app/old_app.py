#!/usr/bin/env python3
from flask import Flask,render_template, request,abort
from typing import List
from os import path,system
from sys import exit
import json
app = Flask(__name__)

BIND_DIRECTORY = '.' #'/etc/bind'
DB_FILE = path.join(BIND_DIRECTORY,'db.laser')

def main():
    try:
        loadConf(DB_FILE)
    except AssertionError as e:
        print(f"Could not find configuration file : {DB_FILE}")
        exit(1)
    system('sh /usr/local/bin/docker-entrypoint.sh')
    app.run()

@app.route('/')
def index():
    return render_template("home.html")

@app.route('/list',methods=["GET"])
def list():
    q = request.args.get("q",default=None)
    conf = loadConf(DB_FILE)
    i = conf.index(";A - Record HostName To Ip Address\n")+1
    data = {"json":[ {"domainName":line.split()[0],"recordType":line.split()[2],"address":line.split()[3]} for line in conf[i+1:]]}
    if q != None:
        if q =='err':
            data['flashMsg'] = "An error has occoured during bind update."
            data['flashClass'] = "alert-danger"
        elif q == 'success':
            data['flashMsg'] = "Successfully updated bind configuration."
            data['flashClass'] = "alert-success"
    return render_template("list.html",data=json.dumps(data))

@app.route('/submit-list',methods=['POST'])
def submitList():
    try:
        if request.form['data'] != None:
            data = json.loads(request.form['data'])
            conf = loadConf(DB_FILE)
            serialIndex = conf.index("@	IN	SOA	dns.laser.di.unimi.it. dnsadmin.security.di.unimi.it. (\n")+1
            newSerial = int(conf[serialIndex])+1
            i = conf.index(";A - Record HostName To Ip Address\n")+1
            newConf = "".join(l for l in conf[:serialIndex])+\
                f"\t\t\t{newSerial}\n"+\
                "".join(l for l in conf[serialIndex+1:i])+\
                "".join(f"{dom['domainName']}\tIN\t{dom['recordType']}\t{dom['address']}\n" for dom in data)
            with open(DB_FILE,'w') as f:
                f.write(newConf)
                f.close()
    except Exception as e:
        print(e)
        abort(500)
    system('service named restart')
    return 'OK'

@app.route('/submit-edit',methods=['POST'])
def submitEdit():
    try:
        if request.form['data'] != None:
            data = json.loads(request.form['data'])
            with open(DB_FILE,'w') as f:
                f.write(data)
                f.close()
    except Exception as e:
        print(e)
        abort(500)
    system('service named restart')
    return 'OK'

@app.route('/edit')
def edit():
    q = request.args.get("q",default=None)
    conf = loadConf(DB_FILE)
    data= {}
    if q != None:
        if q =='err':
            data['flashMsg'] = "An error has occoured during bind update."
            data['flashClass'] = "alert-danger"
        elif q == 'success':
            data['flashMsg'] = "Successfully updated bind configuration."
            data['flashClass'] = "alert-success"
    return render_template("edit.html",conf="".join(conf), q=json.dumps(data))

def loadConf(file: str) -> List[str]:
    assert(path.isfile(file))
    with open(file,'r') as f:
        lines = f.readlines()
        f.close()
    return lines


if __name__ == '__main__':
    main()