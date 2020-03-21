import requests
import json
#以下参考云片网 短信接口文档

def send_single_sms(apikey, code, mobile):
    #发送单条短信
    url = "https://sms.yunpian.com/v2/sms/single_send.json"
    text = "【精品课程在线网】您的验证码是{}。如非本人操作，请忽略本短信".format(code)

    res = requests.post(url, data={
        "apikey": apikey,
        "mobile": mobile,
        "text": text
    })
    re_json = json.loads(res.text)
    return re_json

#测试
if __name__ == "__main__":
    ##45543e74a80df71bb2d6fa1c697a3bcc
    res = send_single_sms("d6c4ddbf50ab36611d2f52041a0b949e", "123456",          "19862171708")
    import json
    res_json = json.loads(res.text)
    code = res_json["code"]
    msg = res_json["msg"]
    #code 判断
    if code == 0:
        print("发送成功")
    else:
        print("发送失败: {}".format(msg))
    print(res.text)