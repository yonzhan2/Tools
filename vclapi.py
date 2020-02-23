import time
import subprocess
import json
import requests


class VclApi:
    """
    VCLAPI to start/stop recording via VLC
    need check below two VLC settings before using:
    1. Tools->Preferences->Interface->Enable "Allow only one instance"
    2. Tools->Preferences->show settings->All->Advanced->Logger->Enable log to file
    """

    def __init__(self):
        self.isrecording = False

    def startRecording(self, recording_name):
        subprocess.call("taskkill /F /IM vlc.exe", stderr=subprocess.PIPE)
        p_ret = subprocess.call(
            r"""START C:\"Program Files"\VideoLAN\VLC\vlc.exe screen:// --qt-start-minimized :screen-fps=5 :sout=#transcode{vcodec=h264,vb072}:standard{access=file,mux=mp4,dst="C:\vlc\%s.mp4"}""" % recording_name,
            shell=True)
        self.isrecording = True if 0 == p_ret else False
        if self.isrecording:
            return True
        return False

    def stopRecording(self):
        if self.isrecording:
            p_ret = subprocess.call(r"""START C:\"Program Files"\VideoLAN\VLC\vlc.exe vlc://quit""", shell=True)
            time.sleep(3)
            if 0 == p_ret:
                return True
            return False
        return False

    def sendRecordingToSpark(self, recording_name, roomId=None):
        if not roomId:
            # default is USTA room
            roomId = "Y2lzY29zcGFyazovL3VybjpURUFNOnVzLWVhc3QtMl9hOmlkZW50aXR5TG9va3VwL1JPT00vMjg0ZTFjZDAtZWZmMy0xMWU5LWJlN2YtN2YyYWMzYzE0YjVi/"
        sparkapi = 'https://api.ciscospark.com/v1/messages'
        # this Authorization is JobBot's token.
        headers = {'Content-Type': 'application/json;charset=UTF-8',
                   'Authorization': 'Bearer MTBkM2Q4ZGMtM2I4OC00NzE1LTliMjMtMTVmMWU4NDc0NjI1OTIzYWYyZDEtZjc2_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f'}
        msg = f"PVT job failed, please check the recording http://xxxxx/{recording_name}.mp4 for detail."
        data = {"roomId": roomId, "text": msg, "markdown": "**%s**" % msg}
        try:
            req = requests.post(sparkapi, data=json.dumps(data), headers=headers)
            if req.status_code == 200:
                print("send msg successfully")
        except Exception as e:
            print(f'send msg failed due to {e}')


if __name__ == "__main__":
    vcl = VclApi()
    print(vcl.startRecording("test"))
    time.sleep(10)
    print(vcl.stopRecording())
