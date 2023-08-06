from pushbullet import PushBullet
import pyautogui as auto
import os
import logging

API_KEY = os.environ.get('PB_API_KEY')
if API_KEY == None:
    auto.alert("No API Key Found in Your Environment")
else:
    pass

pb = PushBullet(api_key=API_KEY)

def sale(systemtime,place,amount,totalamount): # Sales Working Perfectly 
    try:
        pb.push_note(title="₹."+str(amount)+" 💰Sale in "+place,body="🃏₹.%(amount)s sale in %(place)s\n🖼️Total Sales Made ₹. %(totalamount)s\n🖥️ Time: %(systemtime)s"%{"amount":str(amount),"place":place,"totalamount":str(totalamount),"systemtime":systemtime})
    except:
        logging.error("🔥🔥 Got Problem in Connectivity...📡")


def sale_return(systemtime,place,amount,totalamount): # Sales Return Looks Good
    try:
        pb.push_note(title="💵₹"+str(amount)+" Sales Return in "+place,body="🃏₹.%(amount)s sale in %(place)s\n🖼️Total Sales Made ₹. %(totalamount)s\n🖥️ Time: %(systemtime)s"%{"amount":str(amount),"place":place,"totalamount":str(totalamount),"systemtime":systemtime})
    except:
        logging.error("🔥🔥 Got Problem in Connectivity...📡")

def delete_sale(systemtime,place,amount,reason):
    try:
        pb.push_note(title="⚠️₹."+str(amount)+" Sale Deleted in "+place,body="⚔️ Deleted a Sale of ₹.%(amount)s \n📍 Place: %(place)s\n🖥️ Time: %(systemtime)s\n📖 Reason: %(reason)s"%{"amount":str(amount),"place":str(place),"systemtime":str(systemtime),"reason":reason})
    except:
        logging.error("🔥🔥 Got Problem in Connectivity...📡")

def delete_sale_return(systemtime,place,amount,reason):
    try:
        pb.push_note(title="⚠️₹."+str(amount)+" Sales Return Deleted in "+place,body="⚔️ Deleted a Sales Return of ₹.%(amount)s\n📍 Place: %(place)s \n🖥️ Time: %(systemtime)s\n📖 Reason: %(reason)s"%{"amount":str(amount),"place":str(place),"systemtime":str(systemtime),"reason":reason})
    except:
        logging.error("🔥🔥 Got Problem in Connectivity...📡")
