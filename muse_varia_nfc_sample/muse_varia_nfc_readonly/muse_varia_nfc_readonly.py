from mojo import context
from ele_lib import varia_nfc
from ele_lib import muse_pulse

# デバイス定義 ------------------------------------------------------------------------------------------
dvVARIA = context.devices.get("AMX-10001")
dvTP = dvVARIA.port[1]

# NFC用オブジェクト生成
nfc = varia_nfc.VariaNFCRead(dvTP,255)

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

# イベント登録 ------------------------------------------------------------------------------------------
dvTP.channel[255].watch(NFCChannelEvent)    # NFC読み取り検知

context.run(globals())