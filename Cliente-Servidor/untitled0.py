import socket
import random
import base32hex
import hashlib
import pyDes,base64
from Crypto.Cipher import AES

def DeffieHellman(a,b,P,G):
    A=(G**a)%P
    B=(G**b)%P
    
    Ka=(B**a)%P
    Kb=(A**b)%P
        
    if(Ka==Kb):
        DF=True
        return DF
    else:
        DF=False
        return DF


def aes(key,mensaje):
    lineas = mensaje.encode("ASCII")
    n = len(lineas)%16
    lineas = lineas+b' '*(16-n) if n!= 0 else lineas+b''
    aes = AES.new(key, AES.MODE_EAX)
    ciphertext = aes.encrypt(lineas)
    return ciphertext

##def quitarPadding(texto):
##    contador = 0
##    for i in range(1,len(texto)+2):
##        if texto[-i] == 32: # b' ' es 32, que es el byte utilizado para padding
##            contador +=1
##        else:
##            break
##    return texto[0:len(texto)-contador]
##
##def desaes(key,mensaje):
##    key = b"narcotraficantes"
##    cipher = AES.new(kay, AES.MODE_ECB) 
##    textoplano = cipher.decrypt(Recibir)
##    textoplano = quitarPadding(textoplano)
##    
    


#instanciamos un objeto para trabajar con el socket
ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Puerto y servidor que debe escuchar
ser.bind(("", 8050))

#Aceptamos conexiones entrantes con el metodo listen. Por parámetro las conexiones simutáneas.
ser.listen(1)

#Instanciamos un objeto cli (socket cliente) para recibir datos
cli, addr = ser.accept()

while True:

#Recibimos el mensaje, con el metodo recv recibimos datos. Por parametro la cantidad de bytes para recibir
    primos=[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89,97]
    P= random.choice(primos)
    Pkey=str(P)
    G= random.randrange(1,P)
    print(G)
    Gkey=str(G)
    PublicKeysMSG=("Las llaves publicas son P= "+ Pkey+" y G= "+Gkey)
    cli.send(PublicKeysMSG.encode('ascii')) 
    
    a=random.randrange(1,P)
    b = cli.recv(1024)
    b=int(b)
    
    DF=DeffieHellman(a,b,P,G)
    
    if (DF==True):
        ##SE LE SOLICITA EL MENSAJE Y SE REALIZAN LOS CIFRADOS
        alerta=("Las llaves coinciden")
        cli.send(alerta.encode('ascii'))
        
        msg=cli.recv(1024)
        
        msg_enc=aes(msg)
        print(msg)
        
        
        
        
    else:
        #SE COMUNICA QUE LAS LLAVES NO CONCUERDAN Y SE CIERRA LA COMUNICACION
        print("Las llaves no coinciden")
        
    

#Cerramos la instancia del socket cliente y servidor
cli.close()