#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from turtle import Terminator
from enlace import *
import time
import numpy as np

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM4"                  # Windows(variacao de)


def main():
    
    try:
        print("Iniciou o main")
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        
        
            
        #Definindo HEAD pacote
        def headPacote(id, tamanho, tipo, quantos):
            head = []
            head.append(id.to_bytes(1, byteorder='little'))
            head.append(tamanho.to_bytes(1, byteorder='little'))
            head.append(tipo.to_bytes(1, byteorder='little'))
            head.append(quantos.to_bytes(1, byteorder='little'))
            head.append(b'\x00')
            head.append(b'\x00')
            head.append(b'\x00')
            head.append(b'\x00')
            head.append(b'\x00')
            head.append(b'\x00')
            
            f = b''
            for a in head:
                f +=  a
            print(f)

            return f

        #Definindo EOP pacote
        def eopPacote():
            eop = []
            eop.append(b'\x15')
            eop.append(b'\xff')
            eop.append(b'\xd9')
            eop.append(b'\x13')
            
            f = b''
            for a in eop:
                f +=  a
            print(f)

            return f  

        def criacaoDePacotes(dados,tipo):
            tamanho = len(dados)
            
            pacotes = []
            id = 0
            for i in range(0, tamanho, 114):
                dadosPacote = dados[i:i+114]
                size = len(dadosPacote)
                head = headPacote(id, size,tipo, int(tamanho/114))
                eop = eopPacote()
                pacotes.append(head+ (dadosPacote)  + eop)
                id+=1
            print(pacotes)
            return pacotes 


        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        #com1.enable()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        #print("Abriu a comunicação")
        
           
                  
        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são um array bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.
        
        #txBuffer = imagem em bytes!
        #txBuffer = b'\x12\x13\xAA'  #isso é um array de bytes
       
        #print("meu array de bytes tem tamanho {}" .format(len(txBuffer)))
        #faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.
       
            
        #finalmente vamos transmitir os todos. Para isso usamos a funçao sendData que é um método da camada enlace.
        #faça um print para avisar que a transmissão vai começar.
        #tente entender como o método send funciona!
        #Cuidado! Apenas trasmita arrays de bytes!
               
        
        #com1.sendData(np.asarray(txBuffer))  #as array apenas como boa pratica para casos de ter uma outra forma de dados
          
        # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        # O método não deve estar fincionando quando usado como abaixo. deve estar retornando zero. Tente entender como esse método funciona e faça-o funcionar.
        #txSize = com1.tx.getStatus()
        #print('enviou = {}' .format(txSize))
        
        #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        #Observe o que faz a rotina dentro do thread RX
        #print um aviso de que a recepção vai começar.
        
        #Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        #Veja o que faz a funcao do enlaceRX  getBufferLen
      
        #acesso aos bytes recebidos
        #txLen = len(txBuffer)
        com1 = enlace(serialName)
        com1.enable()
        print("esperando 1 byte de sacrifício")
        rxBuffer1, nRx = com1.getData(1)
        com1.rx.clearBuffer()
        time.sleep(.1)
        print("Passou")
        handshake = False
        erro = True
        rxBuffer1, nRx = com1.getData(10)
        if rxBuffer1[2] == 0x01:
            tamanho = rxBuffer1[1]
            
            

            
            print("tamanho do pacote = {}" .format(tamanho))
            

            
            rxBuffer, nRx = com1.getData(tamanho)
            
            for i in range(len(rxBuffer)):
                print("recebeu {}" .format(rxBuffer[i]))
            
            print("______Inicio da resposta_______")   
            resposta = 5*b'\xcc'
            for pacote in criacaoDePacotes(resposta,2):
                print(len(pacote))
                com1.sendData(pacote)
                time.sleep(.2)
                print("Pacote enviado")  
                handshake = True    
            rxBufferf, nRx = com1.getData(4)  
        rxtotal = b''
        
        if handshake:
            id_ant = -1
            print("Handshake feito com sucesso")
            sim = True
            
            while sim:
                payload_errado = False
                rxBuffer, nRx = com1.getData(10)
                if rxBuffer[0] == rxBuffer[3]:
                    sim = False
                tamanho = rxBuffer[1]
                id = rxBuffer[0]
                print("rxbuffer",rxBuffer)
                print("bufferlen", com1.rx.getBufferLen())
                time.sleep(0.3)
                buffer_len =  com1.rx.getBufferLen() - 4
                if tamanho != buffer_len:
                    payload_errado = True    
                if (rxBuffer[2] == 0x03) and not payload_errado :
                    
                    
                    rxBuffer, nRx = com1.getData(tamanho)
                
                    rxtotal += rxBuffer
                print("Tamonho",tamanho, "len", buffer_len)    
                
                
                rxBuffer, nRx = com1.getData(4)
                
                if (id - id_ant == 1) and rxBuffer == b'\x15\xff\xd9\x13' and (not payload_errado):
                    id_ant = id
                    corrompe = False
                    print("Pacote recebido com sucesso")
                else:
                    print("Pacote corrompido")
                    corrompe = True
                
                if not corrompe:
                    print("______Inicio da resposta_______")
                    resposta = 5*b'\xcc'
                    for pacote in criacaoDePacotes(resposta,4):
                        print(len(pacote))
                        com1.sendData(pacote)
                        time.sleep(.2)
                    print("Confirmação enviada")   
                else:
                    print("______Inicio da resposta_______")
                    resposta = 5*b'\xcc'
                    for pacote in criacaoDePacotes(resposta,5):
                        print(len(pacote))
                        com1.sendData(pacote)
                        time.sleep(.2)
                    print("Not Confirmação enviada")
                    sim=False                 

                
                
            print("______Fim do recebimento_______")
            with open("CamadaFisica2022.2\\Projeto 3\\Server\\recebido.txt", "wb") as f:
                f.write(rxtotal)

            
            print(len(rxtotal))
            
                
            
        '''

        contador = 0
        
        quant = tamanho


        for i in stringRxBuffer:
            if i == "c":
                ''
            else:
                contador += 1   
        print("contador = {}" .format(contador))'''
        # tamanhoDoRec = stringRxBuffer[:contador-2] 
        # #convert from string to bytes
        # tamanhoDoRec = bytes(tamanhoDoRec, 'utf-8')
        # tamanhoDoRec = int.from_bytes(tamanhoDoRec, byteorder='little')

        # print ("tamanhoDoRec = {}" .format(tamanhoDoRec))

        # print("recebeu {} bytes" .format(len(rxBuffer)))
        









       
       
    
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
