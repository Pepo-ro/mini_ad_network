# ミニアドネットワークの構築
インターンの中で小規模なアドネットワークの構築を行いました。
アドネットワークの仕様として与えられた要件定義に基づいて構築を行いました。

## 使用言語・ライブラリなど
Python3  
Gunicorn  
Flask  
Nginx  


## 要件
1.  ＳＤＫからリクエストをうけとって、広告を返す。
1.  複数のＤＳＰに対して、AdRequestを投げ、AdResponseを受け取る
1.  1番高い入札を行ったＤＳＰに対して、WinNoticeを送り、2ndPriceをつけて送る
1.  入札時間は、Requestを送ってから100ms以内とする
1.  すべてのＤＳＰからのレスポンスを得られなかった場合、自社広告をDSKに対して返す
1.  レスポンスが1つしか得られなかった場合、2ndプライスを1円として、WinNoticeを返す


## 使用方法
DSPサーバを複数立ち上げます。
```bash
$ bash run_dsp.sh
```
SSPサーバを立ち上げます
```bash
$ gunicorn ssp(サーバのファイル名):app --config guniconf.py(gunicornの設定ファイル)　
```
ssp_proは並列処理をプロセスで行います。  
ssp_sureは並列処理をスレッドで行います。

以下のＵＲＬには工夫点・成果などを載せています。
https://tech-blog.fancs.com/entry/2018/09/12/ssp_by_python
