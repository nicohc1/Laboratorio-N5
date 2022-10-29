#!/usr/bin/env python

#Variables
host = 'localhost'
port = 8050
#Se importa el módulo
import socket
from Crypto.Cipher import DES



def CIPHER_DES():
    key=b'password'
    file = open("mensajeentrada.txt","r+")
    lineas = file.readlines() # se lee el archivo
    file.close()
    
    lineas = "".join(lineas) # Se juntan las lineas
    lineas = lineas.encode("ASCII") # se transforman en bytes
    
    # padding
    n = len(lineas)%8 # se calcula el padding a añadir
    lineas = lineas+b' '*(8-n) if n!= 0 else lineas+ b''

    des = DES.new(key, DES.MODE_ECB)
    encrypted_text = des.encrypt(lineas)
    
    file = open("mensajecifrado.txt", "w+")
    file.write(str(encrypted_text))
    file.close()

    
    return encrypted_text

#Creación de un objeto socket (lado cliente)
obj = socket.socket()

#Conexión con el servidor. Parametros: IP (puede ser del tipo 192.168.1.1 o localhost), Puerto
obj.connect((host, port))
print("Conectado al servidor")
print()


#Creamos un bucle para retener la conexion
while True:
    verificador=input("pulsa cualquier tecla para seguir (ingresar x para salir)")
    if verificador != 'x':
        #Instanciamos una entrada de datos para que el cliente pueda enviar mensajes
        keys = obj.recv(1024)   
        print(keys)
        b = input("Ingresa tu llave privada entre P Y G >> ")
        #Con el método send, enviamos el mensaje
        obj.send(b.encode('ascii'))
        #obj.send(mens)
        
        alerta=obj.recv(1024)
        print(alerta)
        msg_encrypt=CIPHER_DES()
        
        obj.send(msg_encrypt)
        
        
        
        
        
        

    else:
        obj.send(verificador.encode())
        #cerramos el socket
        obj.close()

#Cerramos la instancia del objeto servidor
obj.close()
