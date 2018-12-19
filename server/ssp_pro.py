#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#from flask import Flask,request
import json
import flask
from datetime import datetime as time
import os
import requests
import threading
import uuid #UUIを生成

from multiprocessing import Process,Pool,cpu_count #プロセスを生成




#複数のDSP名の取得
with open("Dsp_name","r") as file:
    dsp_server=file.readlines()


dsp_name=[]

for line in dsp_server:
    dsp_name.append(line.strip())

    
app = flask.Flask(__name__)

@app.route('/req', methods=['POST'])
def req():

    #ユーザidを取得する
    user_id=flask.request.json
    #print("user_id:",user_id)
    sample=[]
    uid = str(uuid.uuid4())


    #並列処理開始  プロセス
    rap_data=[[user_id['app_id'],i,uid] for i in dsp_name]    
    p= Pool(processes= len(dsp_server)  )
    sample=p.map(wrapper,rap_data)

    #複数プロセスの終了　並列処理終了
    p.close()    

    print(sample)
    
    
    #空要素を取り除く
    sample = list(filter(lambda a: a != [], sample))
    
    if not sample :
        d= {
            "url":"https://www.fancs.com"
        }

        return flask.jsonify(d)

    #ソート
    anser= sorted(sample, key=lambda x:x['price'])
    
    if len(sample)==1:
                
        win_data={

            "request_id":"mishima-"+uid,
            "price": 1
        }
        
    else :
              
        win_data={
            "request_id":"mishima-"+uid,
            "price":anser[-2]['price']
        }
        
    
    #WinNotice
    win=requests.post(
        anser[-1]['dsp']+"win",
        win_data,
        headers={'Content-Type':'application/json'}
     )
    
    
    with open("Invoice", 'a') as f:
        f.write(anser[-1]['dsp']+'\t'+ anser[-1]['url']+'\t'+str(win_data['price'])+'\n')

    
    
    d = { "url" : anser[-1]['url']  }
    

    return flask.jsonify(d)


#ラッパー
def wrapper(args):
    return send_to_req(*args)




def send_to_req(id,name,uui):

    
    
    send_data={

        "ssp_name":"mishima",
        "request_time": time.now().strftime("%c"),
        "request_id": "mishima-"+uui,
        "app_id": id
    }
    

    try :
        print (str(name)+" : 接続開始")
        data=requests.post(
            name+"req",
            data=json.dumps(send_data),
            headers={'Content-Type': 'application/json'},
            timeout=0.01
        )
        
    except :
        print(str(name)+" : タイムアウト")
        return []
        
    else :
        print(str(name)+" : 接続成功")
        #print(data)
        data=data.json()
        data.update({u'dsp' : name})        
        return data

    finally:
        pass







if __name__ == '__main__':
    app.run(host='0.0.0.0' , port=8000, debug=False, threaded=True)





    
