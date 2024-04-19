# MUSEでのVARIAシリーズ NFCリーダー機能の実装

### 機能
VARIAシリーズのNFCリーダー機能を使用し、カードデータを取得します。

### 使用方法

プログラムフォルダに **ele_libフォルダ** をコピーし、メインプログラムから **import** します。
- varia_nfc.py
- muse_pulse

##### オブジェクト生成

###### 読み取りのみの場合
`nfc = varia_nfc.VariaNFCRead(device,channel)`<br/><br/>
読み取りのみを行う<br/>
**device**はNFC読み取りに使用するタッチパネルを指定<br/>
**channel**はNFCの読み取り時に指定チャンネルをパルスする<br/>

###### リスト生成も行う場合
`nfc = varia_nfc.VariaNFCList(device,channel,list)`<br/><br/>
読み取り機能の他にリストを生成してリスト内データと合致するか確認する<br/>
**device**はNFC読み取りに使用するタッチパネルを指定<br/>
**channel**はNFCの読み取り時に指定チャンネルをパルスする<br/>
**list**は読み取ったデータを格納するリストを指定

##### 読み取り

読み取りを行うと指定のチャンネルがパルスされ、読み取ったデータが**last_data**に格納される。
メインプログラム側では指定のチャンネルの**watch**を行い、読み取り時に行いたい処理を実装する。

##### データ構造

読み取ったデータは辞書型で格納される

`{"type","data","hit"}`<br>

**type**は1～4の数値データ<br/>
0 ------ (なし)<br/>
1 ISO 15693<br/>
2 ISO 14443A<br/>
3 ISO 14443B<br/>
4 FeliCa<br/>

**data**はカード番号データ文字列<br>
**hit**はリスト生成も行った場合のみで、リスト内に同一のデータがあった場合**True**、ない場合は**False**<br/>

#### 関数（共通）

##### get_last_read()

`last_read = nfc.get_last_read()`<br/>

最後に読み取ったデータを取得する<br/><br/>


##### get_type_list()
`type_list = nfc.get_type_list()`<br/>

カードのタイプを文字列リストで取得する<br/><br/>

#### 関数（VariaNFCListのみ）

##### append_last_read()
`nfc.append_last_read()`<br/>

最後に読み取ったデータをリストに追加する<br/><br/>

##### append(type,data)
`nfc.append(1,"00:00:00:00:00:00:00:00")`<br/>

リストにデータを追加する<br/>
**type**は1～4の数値<br/>
**data**は文字列で指定<br/><br/>

##### remove_last_read()
`nfc.remove_last_read()`<br/>

最後に読み取ったデータをリストから削除する<br/><br/>

##### remove(type,data)
`nfc.remove(1,"00:00:00:00:00:00:00:00")`

該当するデータをリストから削除する<br/>
**type**は1～4の数値<br/>
**data**は文字列で指定<br/><br/>

##### load(filename)
`nfc.load("hoge.csv")`

ファイルからリストデータを読み込む<br/>
**filename**はファイル名を指定<br/>
読み込んだデータの数を戻り値として返す<br/><br/>

##### save(filename)
`nfc.save("hoge.csv")`

リストデータをファイルに保存する<br/>
**filename**はファイル名を指定<br/>
書き込んだデータの数を戻り値として返す<br/><br/>
