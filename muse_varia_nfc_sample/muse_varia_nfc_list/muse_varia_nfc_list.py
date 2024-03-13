from mojo import context
from ele_lib import varia_nfc
from ele_lib import muse_pulse

# デバイス定義 ------------------------------------------------------------------------------------------
dvVARIA = context.devices.get("AMX-10001")
dvTP = dvVARIA.port[1]


# NFC用オブジェクト生成
nfc_data_list = []
nfc_list_filename = "nfc_data.csv"
nfc = varia_nfc.VariaNFCList(dvTP,255,nfc_data_list)

# PULSE用オブジェクト生成
pl = muse_pulse.Pulse()


# イベント処理 ------------------------------------------------------------------------------------------
def NFCChannelEvent(e):
    # ONの時
    if e.value:
        last_read = nfc.get_last_read() # 直近の読み取りデータを取得
        type_list = nfc.get_type_list() # タイプリストのテキストを取得

        dvTP.send_command("^TXT-1,0,%s" %(type_list[last_read["type"]]))
        dvTP.send_command("^TXT-2,0,%s" %(last_read["data"]))

        if last_read["hit"]:    # リストに該当があったら
            dvTP.send_command("^TXT-3,0,Hit")
            pl.pulse_netlinx(dvTP,254,5)
        else:
            dvTP.send_command("^TXT-3,0,N/A")

def ButtonEvent(e):
    ch = int(e.id)

    dvTP.channel[ch] = e.value

    if e.value: # PUSH
        if ch == 1: # append
            nfc.append_last_read()
            draw_list_text()
        if ch == 2: # remove
            nfc.remove_last_read()
            draw_list_text()
        if ch == 3: # save
            count = nfc.save(nfc_list_filename)
            dvTP.send_command("^TXT-3,0,SAVE: %s" %(count))
        if ch == 4: # load
            count = nfc.load(nfc_list_filename)
            if count >= 0:
                dvTP.send_command("^TXT-3,0,LOAD: %s" %(count))
                draw_list_text()
            else:
                dvTP.send_command("^TXT-3,0,Not Found")
        
def draw_list_text():
    count = 0
    for ls in nfc_data_list:
        dvTP.send_command("^TXT-%s,0,%s" %(count+11,ls["data"]))
        count += 1
        if count > 9:
            return
    for add in range(count,10):
        dvTP.send_command("^TXT-%s,0," %(add+11))




# イベント登録 ------------------------------------------------------------------------------------------
dvTP.channel[255].watch(NFCChannelEvent)    # NFC読み取り検知
dvTP.button[1].watch(ButtonEvent)           # リストに追加
dvTP.button[2].watch(ButtonEvent)           # リストから削除
dvTP.button[3].watch(ButtonEvent)           # リストを保存
dvTP.button[4].watch(ButtonEvent)           # リストを読み込み

context.run(globals())
