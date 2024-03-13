# -------------------------------------------------------------------------------------------------
#
# Muse PULSE実行モジュール v1.0
#
# Program: KEI
#
#--------------------------------------------------------------------------------------------------

from mojo import context

class Pulse:
    # 初期化 -----------------------------------------------------------------------------------------
    def __init__(self):
        self.pulse_list = []
        self.tl = context.services.get("timeline")
        self.tl.expired.listen(self.pulse_check)


    # PULSE登録 -------------------------------------------------------------------------------------
    # PULSE追加
    def pulse_append(self,dev,ch,time,type):

        # リストが空だったらtimelineを開始
        if self.pulse_list == []:
            self.tl.start([100],False,-1)
        
        # 多重登録チェック
        for ls in self.pulse_list:
            if ls["device"] == dev and ls["channel"] == ch:
                return
        
        # タイプ別処理
        if type == "muse relay":
            dev[ch].state = True
        elif type == "muse ir":
            dev.onIr(ch)
        elif type == "muse io":
            dev[ch].output = True
        elif type == "netlinx":
            dev.channel[ch] = True
        
        # パルス追加
        self.pulse_list.append({"type":type,"device":dev,"channel":ch,"time":time})
 
    ##### MUSE系 relay #####
    def pulse_muse_relay(self,dev,ch,time):
        self.pulse_append(dev,ch,time,"muse relay")
        
    ##### MUSE系 ir #####
    def pulse_muse_ir(self,dev,ch,time):
        self.pulse_append(dev,ch,time,"muse ir")
    
    ##### MUSE系 io #####
    def pulse_muse_io(self,dev,ch,time):
        self.pulse_append(dev,ch,time,"muse io")

    ##### netlinx #####
    def pulse_netlinx(self,dev,ch,time):
        self.pulse_append(dev,ch,time,"netlinx")


    # PULSE終了チェック ---------------------------------------------------------------------------------
    def pulse_check(self,e):

        # カウントダウンと終了済みの確認
        check = False
        for l in self.pulse_list:
            l["time"] -=1
            if l["time"] <= 0:
                check = True
        
        # 終了済みがあった場合
        if check:
            tmp = []

            # PULSEリストを確認
            while self.pulse_list:
                ls = self.pulse_list.pop()
                
                # PULSE継続
                if ls["time"]:
                    tmp.append(ls)
                
                # PULSE終了
                else:
                    # Muse系デバイス
                    if ls["type"] == "muse relay":
                        ls["device"][ls["channel"]].state = False
                    elif ls["type"] == "muse ir":
                        ls["device"].offIr(ls["channel"])
                    elif ls["type"] == "muse io":
                        ls["device"][ls["channel"]].output = False
                    
                    # Netlinx系デバイス
                    elif ls["type"] == "netlinx":
                        ls["device"].channel[ls["channel"]] = False

            # リスト再構成
            if tmp:
                while tmp:
                    self.pulse_list.append(tmp.pop())
            else:
                self.tl.stop()