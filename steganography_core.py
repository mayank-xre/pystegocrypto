import cv2
import numpy as np
from cryptography.fernet import Fernet
from hashlib import md5
from base64 import urlsafe_b64encode
import binascii as t
import os
os.chdir("/home/mayank/Desktop")
print(os.getcwd())
def str2bin(message):
    return bin(int(t.hexlify(message),16))[2:]
def bin2str(bin):
    return t.unhexlify('%x' % int('0b'+bin,2))
def rgb2bin(pixel):
    return [format(i,"08b")for i in pixel]
def messageenc(secretmessage,key):
    hash=md5(key.encode()).hexdigest()
    ferkey=urlsafe_b64encode(hash.encode())
    f=Fernet(ferkey)
    enctoken=f.encrypt(secretmessage.encode())
    binoftoken=str2bin(enctoken)
    binoftoken+='10010000100100001001000010010000100100'
    return binoftoken
def hidedata(imagefi,secretmessage,key,newfilen):
    finmessage=messageenc(secretmessage,key)
    image=cv2.imread(imagefi)
    datai=0
    datal=len(finmessage)
    for values in image:
        for pixel in values:
            r,g,b=rgb2bin(pixel)
            if(datai<datal):
                pixel[0]=int(r[:-1]+finmessage[datai],2)
                datai+=1
            if(datai<datal):
                pixel[1]=int(g[:-1]+finmessage[datai],2)
                datai+=1
            if(datai<datal):
                pixel[2]=int(b[:-1]+finmessage[datai],2)
                datai+=1
            if(datai>=datal):
                break   
    cv2.imwrite(f"{newfilen}.png",image)
    return image
def showdata(imagefi,key):
    image=cv2.imread(f"{imagefi}.png")
    bindata=""
    datai=0
    for values in image:
        for pixel in values:
            r,g,b=rgb2bin(pixel)
            bindata+=r[-1]
            bindata+=g[-1]
            bindata+=b[-1]
    ddata,steg=bindata.split('10010000100100001001000010010000100100')
    return "the message is: "+messagedec(bin2str(ddata),key)
def messagedec(message,key):
    hash=md5(key.encode()).hexdigest()
    ferkey=urlsafe_b64encode(hash.encode())
    f=Fernet(ferkey)
    return f.decrypt(message).decode()
encodec=input("what do you want to do (answer in enc or dec)\n")
if(encodec=="enc"):
    filen=input("input filename\n")
    message=input("type your message\n")
    password=input("enter password\n")
    filenfornew=input("filename (without extension) note:stored in png\n")
    hidedata(filen,message,password,filenfornew)
    print("successfully done")
else:
    filen=input("input filename (without extension) note:file taken in png\n")
    password=input("give password for file\n")
    print(showdata(filen,password))
    input("successfully extracted")