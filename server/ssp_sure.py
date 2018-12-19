#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#from flask import Flask,request
import json
import flask #フレームワーク
from datetime import datetime as time
import os
import requests
import threading #スレッド生成
import uuid #UUIを生成
from queue import Queue  #スレッドの戻り値を取得






#複数のDSP名の取得
with open("dsp_name","r") as file:
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
    

    #並列処理開始　スレッド　

    Thread_list=[]
    que=[]
    
    for i in range(len(dsp_name)):
        que.append( Queue()  )
        Thread_list.append( threading.Thread(target=send_to_req , args=(user_id['app_id'],dsp_name[i],uid,que[i])))


    for i in range(len(dsp_name)):
        Thread_list[i].start()

    for i in range(len(dsp_name)):
        Thread_list[i].join()
        sample.append(que[i].get())


    #並列処理終了　スレッド
    
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
            "request_id":"mishima-"+ uid,
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




def send_to_req(id,name,uui,que):

    
    
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
            timeout=0.1
        )
        
    except :
        print(str(name)+" : タイムアウト")
        que.put([])#スレッドの戻り値を取得
        
    else :
        print(str(name)+" : 接続成功")
        #print(data)
        data=data.json()
        data.update({u'dsp' : name})        
        que.put(data)#スレッドの戻り値を取得

    finally:
        pass

    

if __name__ == '__main__':
    app.run(host='0.0.0.0' , port=8000, debug=False, threaded=True)





    
