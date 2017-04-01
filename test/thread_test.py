import requests

url = "http://study.163.com/dwr/call/plaincall/LessonLearnBean.getVideoLearnInfo.dwr"

querystring = {"1491032520926":""}

payload = "callCount=1&scriptSessionId=%24%7BscriptSessionId%7D190&httpSessionId=707dc2ff5b79498d82d16bea17b3ab1c&c0-scriptName=LessonLearnBean&c0-methodName=getVideoLearnInfo&c0-id=0&c0-param0=string%3A1004219036&c0-param1=string%3A1003687003&batchId=1491032520926"
headers = {
    'cookie': "NTESSTUDYSI=707dc2ff5b79498d82d16bea17b3ab1c; EDUWEBDEVICE=eb6449c747cd49bfa0648c2c2236e6ef;",
    }

response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

print(response.text)