import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

tagId= {"584185707224":"casio", "585508657864":"chocolatto",
        "585519407700":"lays", "584185445084":"uvmatt",
        "585518488921":"ssd", "585508137202":"colgate",
        "585509526928":"khopra", "585513263862":"shan",
        "585513385399":"casio", "585523939182":"chocolatto",
        "585512275414":"lays", "585517191682":"uvmatt",
        "585524655889":"ssd", "585519149632":"colgate",
        "585518760506":"khopra", "451877895973":"shan",
        "331606535965":"2%", "168809715562": "5%"
        }
classes= dict()
classes.setdefault('10')
classes['casio'] = '1'
classes['chocolatto'] = '2'
classes['lays'] = '3'
classes['uvmatt'] = '4'
classes['ssd'] = '5'
classes['colgate'] = '6'
classes['khopra'] = '7'
classes['shan'] = '8'
classes['bad'] = '9'
classes['2%'] = '2%'
classes['5%'] = '5%'

reader = SimpleMFRC522()

def rfidRead():
    result="bad"
    try:
        id, text = reader.read()
        print(id)
        result=tagId[str(id)]
        print(text)
    finally:
        GPIO.cleanup()
    return(classes[result])

