#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from re import T
from enlace import *
import time
#import numpy as np
import sys
from datetime import datetime
from PyCRC.CRC16 import CRC16


# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM4"                  # Windows(variacao de)


#Definindo HEAD pacote
def headPacote(id, tamanho, tipo, quantos,payload,  reenvio = 0):
    head = []
    head.append(tipo.to_bytes(1, byteorder='little'))
    head.append(b'\x01')
    head.append(b'\x00')
    head.append(quantos.to_bytes(1, byteorder='little'))
    head.append(id.to_bytes(1, byteorder='little'))
    if tipo == 1:
        head.append(b'\x01')
    else:
        head.append(tamanho.to_bytes(1, byteorder='little'))
    head.append(reenvio.to_bytes(1, byteorder='little'))
    if id > 1:
        head.append((id-1).to_bytes(1, byteorder='little'))
    else:
        head.append((0).to_bytes(1, byteorder='little'))
    a = CRC16().calculate(payload).to_bytes(2, byteorder='little')
    print(a)
    head.append(a[0].to_bytes(1, byteorder='little'))
    head.append(a[1].to_bytes(1, byteorder='little'))
    
    f = b''
    for a in head:
        f +=  a
    return f

#Definindo EOP pacote
def eopPacote():
    eop = []
    eop.append(b'\xAA')
    eop.append(b'\xBB')
    eop.append(b'\xCC')
    eop.append(b'\xDD')
    
    f = b''
    for a in eop:
        f +=  a
    

    return f  

def criacaoDePacotes(tipo, dados=b'', reenvio = 0):
    tamanho = len(dados)

    
    pacotes = []
    id = 0
    if dados == b'':
        head = headPacote(id, 0,tipo, int(tamanho/114), dados, reenvio )
        eop = eopPacote()

        pacotes.append(head + eop)
    else:    
        for i in range(0, tamanho, 114):
            dadosPacote = dados[i:i+114]
            size = len(dadosPacote)
            
            head = headPacote(id, size,tipo, int(tamanho/114), dadosPacote , reenvio)
            eop = eopPacote()

            pacotes.append(head+ (dadosPacote)  + eop)
            id += 1
    return pacotes 


    


def main():
    try:
        print("Iniciou o main")
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        tudo = ''
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        time.sleep(.2)
        com1.sendData(b'00')
        time.sleep(1)
        print("_______Inicio da verificação________")
        

        inicia = False
        while inicia == False:
            print("Quero falar com você")
            for pacote in criacaoDePacotes(1):
                com1.sendData(pacote)
                time.sleep(0.2)
                print("{0} / envio / {1} / {2} / {3} / {4}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), pacote[0], len(pacote), pacote[4]+1, pacote[3]+1))
                tudo += ("{0} / envio / {1} / {2} / {3} / {4}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), pacote[0], len(pacote), pacote[4]+1, pacote[3]+1))+ "\n"


            print("Na escuta")
            time.sleep(5)
            
            if com1.rx.getIsEmpty() == False:
                
                rxBuffer, nRx = com1.getData(10)
                if rxBuffer[1] == 2 and rxBuffer[0] == 2:
                    inicia = True
 
                com1.rx.clearBuffer()
        cont = 1

        dados = b'\xc3'*554
        pacotes = criacaoDePacotes(3, dados)
        
        numPck = len(pacotes)
        print("Pacotes criados")
        print(pacotes)
        print("Numero de pacotes: ", numPck)
        while cont <= numPck:
            print('Pckg')
            
            try:
                com1.sendData(pacotes[cont-1])
                print("{0} / envio / {1} / {2} / {3} / {4}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), pacotes[cont-1][0], len(pacotes[cont-1]), pacotes[cont-1][4]+1, pacotes[cont-1][3] +1))
                tudo +=("{0} / envio / {1} / {2} / {3} / {4}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), pacotes[cont-1][0], len(pacotes[cont-1]), pacotes[cont-1][4]+1, pacotes[cont-1][3] +1))+ "\n"

            except: ''
            time.sleep(0.2)

            timer1 = time.time()
            timer2 = time.time()
            
            ainda = True
            while ainda:
                agora  = time.time()
                if com1.rx.getIsEmpty() == False:
                    rxBuffer, nRx = com1.getData(10)
                    sizePayload = rxBuffer[5]
                    p, x = com1.getData(sizePayload)
                    lixo,y = com1.getData(4)
                    print("{0} / receb/ {1} / {2}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), rxBuffer[0], len(rxBuffer) + sizePayload + len(lixo)))
                    tudo +=("{0} / receb/ {1} / {2}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), rxBuffer[0], len(rxBuffer) + sizePayload + len(lixo)))+ "\n"
                    if rxBuffer[1] == 2 and rxBuffer[0] == 4:
                        print ('Pckg ok')
                        id = rxBuffer[6]
                        cont = id +1
                        
                        ainda = False
                        com1.rx.clearBuffer()
                        time.sleep(0.5)

                    else:

                            
                        if agora - timer1 > 5:
                            com1.sendData(pacotes[cont])
                            time.sleep(0.2)
                            timer1 = time.time()
                            print("{0} / envio / {1} / {2} / {3} / {4}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), pacotes[cont][0], len(pacotes[cont]), pacotes[cont][4] +1, pacotes[cont][3] +1))
                            tudo +=("{0} / envio / {1} / {2} / {3} / {4}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), pacotes[cont][0], len(pacotes[cont]), pacotes[cont][4] +1, pacotes[cont][3] +1))+ "\n"

                        if agora - timer2 > 20:
                            com1.rx.clearBuffer()
                            for pacote in criacaoDePacotes(5):
                                com1.sendData(pacote)
                                time.sleep(0.2)
                                print("{0} / envio / {1} / {2} / {3} / {4}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), pacote[0], len(pacote), pacote[4] +1, pacote[3] +1))
                                tudo +=("{0} / envio / {1} / {2} / {3} / {4}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), pacote[0], len(pacote), pacote[4] +1, pacote[3] +1))+ "\n"

                            com1.disable()
                            ainda = False
                            print (' :-( ')
                            sys.exit()
                        elif com1.rx.getIsEmpty() == False:
                            rxBuffer, nRx = com1.getData(10)
                            sizePayload = rxBuffer[5]
                            p, x = com1.getData(sizePayload)
                            lixo,y = com1.getData(4)
                            print("{0} / receb/ {1} / {2}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), rxBuffer[0], len(rxBuffer) + sizePayload + len(lixo)))
                            tudo +=("{0} / receb/ {1} / {2}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), rxBuffer[0], len(rxBuffer) + sizePayload + len(lixo)))+ "\n"

                            if rxBuffer[1] == 2 and rxBuffer[0] == 6:
                                id = rxBuffer[6]
                                cont = id 
                                com1.sendData(pacotes[cont])
                                print("{0} / envio / {1} / {2} / {3} / {4}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), pacotes[cont][0], len(pacotes[cont]), pacotes[cont][4] +1, pacotes[cont][3] + 1))
                                tudo +=("{0} / envio / {1} / {2} / {3} / {4}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), pacotes[cont][0], len(pacotes[cont]), pacotes[cont][4] +1, pacotes[cont][3] + 1)) + "\n"   

                                time.sleep(0.2)
                                timer1 = time.time()
                                timer2 = time.time()
                                com1.rx.clearBuffer()
                                ainda = True
                        
                       
                else:
                    if agora - timer1 > 5:
                            com1.sendData(pacotes[cont])
                            time.sleep(0.2)
                            timer1 = time.time()
                            print("{0} / envio / {1} / {2} / {3} / {4}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), pacotes[cont][0], len(pacotes[cont]), pacotes[cont][4] +1, pacotes[cont][3] +1))
                            tudo +=("{0} / envio / {1} / {2} / {3} / {4}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), pacotes[cont][0], len(pacotes[cont]), pacotes[cont][4] +1, pacotes[cont][3] +1)) + "\n"

                    if agora - timer2 > 20:
                        com1.rx.clearBuffer()
                        for pacote in criacaoDePacotes(5):
                            com1.sendData(pacote)
                            time.sleep(0.2)
                            print("{0} / envio / {1} / {2} / {3} / {4}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), pacote[0], len(pacote), pacote[4] +1, pacote[3] +1))
                            tudo +=("{0} / envio / {1} / {2} / {3} / {4}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), pacote[0], len(pacote), pacote[4] +1, pacote[3] +1))+ "\n"

                        com1.disable()
                        ainda = False

                        
                        print (' :-( ')
                        sys.exit()

        com1.disable()
        print ('WUNDERBAR!! WIR SIND SUPER!    :-D ') 
     


























          
        print ('\n')
        print("_______Fim da verificação________")
        

        with open( "Client4.txt", "w") as f:
            f.write(tudo)
            f.close()
        print (tudo)   
        
        
        
        
        
            


      
        


        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
