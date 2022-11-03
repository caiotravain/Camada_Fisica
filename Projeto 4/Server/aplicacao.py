#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 




from enlace import *
import time
import numpy as np
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
serialName = "COM4"
def headPacote(id, tamanho, tipo, quantos, reenvio = 0):
    head = []
    head.append(tipo.to_bytes(1, byteorder='little'))
    head.append(b'\x02')
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
    head.append(b'\x00')
    head.append(b'\x00')
    
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
        head = headPacote(id, 0,tipo, int(tamanho/114), reenvio)
        eop = eopPacote()

        pacotes.append(head + eop)
    else:    
        for i in range(0, tamanho, 114):
            dadosPacote = dados[i:i+114]
            size = len(dadosPacote)
            
            head = headPacote(id, size,tipo, int(tamanho/114), reenvio)
            eop = eopPacote()

            pacotes.append(head+ (dadosPacote)  + eop)
            id += 1
    return pacotes 


    
def main():
    
    try:
        tudo = ''
        print("Iniciou o main")
        com1 = enlace(serialName)
        nap = False
        com1.enable()
        time.sleep(.2)
        com1.getData(1)
        time.sleep(1)
        com1.rx.clearBuffer()

        print("_______Inicio da verificação________")
        print("Esperando mensagem")
        ocioso = True
        total = b''
        while ocioso:
            if com1.rx.getIsEmpty() == False:
                print("Recebendo mensagem")
                msg, a = com1.getData(10)
                lixo, x = com1.getData(4)
                sizePayload = msg[5]
                print("{0} / receb/ {1} / {2}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), msg[0], len(msg) + len(lixo)))
                tudo += ("{0} / receb/ {1} / {2}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), msg[0], len(msg) + len(lixo))) + "\n"

                if msg[0] == 1:
                    if msg[1] == 1:
                        ocioso = False
            time.sleep(1)

        com1.rx.clearBuffer()


        for pacote in criacaoDePacotes(2):
            com1.sendData(pacote)
            time.sleep(0.2)
        numPckg = 2
        cont = 1
        while cont <= numPckg + 1:
            timer1 = time.time()
            timer2 = time.time()
            ainda = True
            while ainda :
                time.sleep(0.5)
                if com1.rx.getIsEmpty() == False:
                    rxBuffer, nRx = com1.getData(10)
                    
                    id = rxBuffer[4]
                    sizePayload = rxBuffer[5]
                    sizepay = com1.rx.getBufferLen() - 4

                    # if cont == 8 and nap == False:
                    #     id = 10
                    #     nap = True
                    p, x = com1.getData(sizePayload)
                    lixo,y = com1.getData(4)
                    numPckg = rxBuffer[3]
                    print("Crc: {0}".format(rxBuffer[8:9]))
                    expected = CRC16().calculate(p).to_bytes(2, byteorder='little')[:-1]
                    print("Crc2: {0}".format(expected))
                    if rxBuffer[1] == 1 and rxBuffer[0] == 3  and rxBuffer[8:9] == expected:
                        
                        print("{0} / receb/ {1} / {2}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), rxBuffer[0], len(rxBuffer) + sizePayload + len(lixo), rxBuffer[8]))
                        tudo += "{0} / receb/ {1} / {2}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), rxBuffer[0], len(rxBuffer) + sizePayload + len(lixo)) + "\n"
                        if id+1 == cont and sizePayload == sizepay:
                            payload = p
                            
                            
                            print ('Pckg ok')
                            
                            ainda = False
                            
                            total+= payload
                            
                            for pacote in criacaoDePacotes(4, reenvio=cont):
                                com1.sendData(pacote)
                                time.sleep(0.2)
                                print("{0} / envio / {1} / {2} / {3} / {4}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), pacote[0], len(pacote), pacote[4]+1, pacote[3] +1))
                                tudo += ("{0} / envio / {1} / {2} / {3} / {4}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), pacote[0], len(pacote), pacote[4]+1, pacote[3] +1)) + "\n"
                                
                            cont += 1
                            
                        else:
                            for pacote in criacaoDePacotes(6, reenvio=cont-1):
                                com1.sendData(pacote)
                                time.sleep(0.2)
                                print("{0} / envio / {1} / {2} / {3} / {4}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), pacote[0], len(pacote), pacote[4]+1, pacote[3] +1))
                                tudo += ("{0} / envio / {1} / {2} / {3} / {4}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), pacote[0], len(pacote), pacote[4]+1, pacote[3] +1)) + '\n'
                                ainda = False
                                
                else:
                    time.sleep(1)
                    if time.time() - timer2 > 20:
                        ocioso = True
                        for pacote in criacaoDePacotes(5):
                            com1.sendData(pacote)
                            time.sleep(0.2)
                            print("{0} / envio / {1} / {2} / {3} / {4}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), pacote[0], len(pacote), pacote[4]+1, pacote[3] +1))
                            tudo += ("{0} / envio / {1} / {2} / {3} / {4}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), pacote[0], len(pacote), pacote[4]+1, pacote[3] +1)) + '\n'

                        com1.disable()
                        print (':-(  Sheiße')
                        ainda = False
                        with open ("Server3.txt", "w") as f:
                            f.write(tudo)
                            f.close()
                        print (tudo)
                        sys.exit()
                            
                    else:
                        if time.time() - timer1>2:
                            for pacote in criacaoDePacotes(4, reenvio=cont-1):
                                com1.sendData(pacote)
                                time.sleep(0.2)
                                print("{0} / envio / {1} / {2} / {3} / {4}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), pacote[0], len(pacote), pacote[4] +1, pacote[3]+1))
                                tudo += ("{0} / envio / {1} / {2} / {3} / {4}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), pacote[0], len(pacote), pacote[4] +1, pacote[3]+1)) + '\n'

                            timer1 = time.time()
                            ainda = True


























        with open ("Server4.txt", "w") as f:
            f.write(tudo)
            f.close()
        print (tudo)



        
        print(len(total))
        print (tudo)
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
