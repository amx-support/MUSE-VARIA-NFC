# -------------------------------------------------------------------------------------------------
#
# Muse Varia NFC読み取り・リスト管理モジュール v1.2
#
# Program: KEI
#
# v.1.2     リストをメインプログラム側から引数で指定する方式に変更
#
#--------------------------------------------------------------------------------------------------

from ele_lib import muse_pulse

# NFC読み取りのみ ---------------------------------------------------------------------------------------
class VariaNFCRead:
    # 初期化
    def __init__(self,dvTP,channel):
        self.dvTP = dvTP
        self.channel = channel
        self.last_read = {"type":0,"data":""}
        self.tag_type_list = ["------","ISO 15693","ISO 14443A","ISO 14443B","FeliCa"]
        self.dvTP.custom.listen(self.CustomEvent)
        self.pl = muse_pulse.Pulse()
    
    # NFCの読み取り
    def CustomEvent(self,e):
        custom_type = e.arguments["type"]

        if custom_type == 700: # NFCのイベントタイプは700
            tag_type = e.arguments["value1"]
            tag_data = e.arguments["data"].decode()   

            self.last_read["type"] = tag_type
            self.last_read["data"] = tag_data
            self.pl.pulse_netlinx(self.dvTP,self.channel,5)
    
    # 最後に読み取ったデータを取得
    def get_last_read(self):
        return self.last_read
    
    # タグタイプのリストを取得
    def get_type_list(self):
        return self.tag_type_list


# NFC読み取り＋リスト管理 -----------------------------------------------------------------------------------
class VariaNFCList(VariaNFCRead):
    # 初期化
    def __init__(self,dvTP,channel,data_list):
        super().__init__(dvTP,channel)
        self.data_list = data_list
        self.last_read = {"type":0,"data":"","hit":False}
    
    # NFCの読み取り
    def CustomEvent(self,e):
        custom_type = e.arguments["type"]

        if custom_type == 700: # NFCのイベントタイプは700
            tag_type = e.arguments["value1"]
            tag_data = e.arguments["data"].decode()   

            self.last_read["hit"] = False
            for ls in self.data_list:
                if ls == {"type":tag_type,"data":tag_data}:
                    self.last_read["hit"] = True
                    break

            self.last_read["type"] = tag_type
            self.last_read["data"] = tag_data
            self.pl.pulse_netlinx(self.dvTP,self.channel,5)

    # 最後に読み取ったデータをリストに追加
    def append_last_read(self):
        # 未登録であれば登録
        for ls in self.data_list:
            if ls == {"type":self.last_read["type"],"data":self.last_read["data"]}:
                return
        self.data_list.append({"type":self.last_read["type"],"data":self.last_read["data"]})
        
    # リストに追加
    def append(self,type,data):
        # 未登録であれば登録
        for ls in self.data_list:
            if ls == {"type":self.last_read["type"],"data":self.last_read["data"]}:
                return
        self.data_list.append({"type":self.last_read["type"],"data":self.last_read["data"]})

    # 最後に読み取ったデータをリストから削除
    def remove_last_read(self):
        try:
            self.data_list.remove({"type":self.last_read["type"],"data":self.last_read["data"]})
        except ValueError:
            print("[ELELIB:VariaNFC] .delete_last_read - data not in list")

    # リストから削除
    def remove(self,type,data):
        try:
            self.data_list.remove({"type":type,"data":data})
        except ValueError:
            print("[ELELIB:VariaNFC] .delete - data not in list")
    
    # リストファイルの読み込み
    def load(self,filename):
        try:    # ファイルがある場合
            with open(filename,"r",encoding="UTF-8") as f:
                self.data_list.clear()
                data_list = [data.rstrip() for data in f.readlines()]   # 末尾の改行を削除
                count = 0
                for ls in data_list:
                    s = ls.split(",")
                    self.data_list.append({"type":int(s[0]),"data":s[1]})
                    count += 1

                return count

        except FileNotFoundError:   # ファイルがない場合
            print("[ELELIB:VariaNFC] .load - file not found")
            return -1
    
    # リストファイルを保存
    def save(self,filename):
        with open(filename,"w",encoding="UTF-8") as f:
            count = 0
            for ls in self.data_list:
                f.write("%s,%s\n" %(ls["type"],ls["data"]))
                count += 1
            
            return count