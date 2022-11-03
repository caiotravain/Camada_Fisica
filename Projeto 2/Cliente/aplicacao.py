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

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM5"                  # Windows(variacao de)


#Definindo HEAD pacote
def headPacote(id, tamanho):
    head = np.zeros(10, dtype=np.uint8)
    head[0] = id
    head[1] = tamanho
    head[2] = b'\x00'
    head[3] = b'\x00'
    head[4] = b'\x00'
    head[5] = b'\x00'
    head[6] = b'\x00'
    head[7] = b'\x00'
    head[8] = b'\x00'
    head[9] = b'\x00'
    return head

#Definindo EOP pacote
def eopPacote():
    eop = np.zeros(4, dtype=np.uint8)
    eop[0] = b'\x15'
    eop[1] = b'\xff'
    eop[2] = b'\xd9'
    eop[3] = b'\x13'
    return eop  

def criacaoDePacotes(dados):
    tamanho = len(dados)
    pacotes = []
    for i in range(0, tamanho, 114):
        dadosPacote = dados[i:i+114]
        head = headPacote(i, len(dadosPacote))
        eop = eopPacote()
        pacote = np.concatenate((head, dadosPacote, eop))
        pacotes.append(pacote)
    return pacotes 


    


def main():
    try:
        print("Iniciou o main")
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        time.sleep(.2)
        com1.sendData(b'00')
        time.sleep(1)

           
                  
        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são um array bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.
        
        #txBuffer = imagem em bytes!
        imageR = 'mengo.jpeg'
        imageW = 'mengo_transmitido.jpeg'
        
        comandos = [b"x00\xFA\x00\x00", b"x00\x00\xFA\x00", b"xFA\x00\x00", b"x00\xFA\x00", b"x00\x00\xFA", b"x00\xFA", b"xFA\x00", b"x00", b"xFA"]
        randQntComandos = np.random.randint(10, 30)
        
        listaComandosEnviados = []
        for i in range(randQntComandos):
            randDoComando = np.random.randint(0, len(comandos))
            listaComandosEnviados.append(comandos[randDoComando])
        print("Tam listaComandosEnviados: ", len(listaComandosEnviados))
        
        
        
        add = b"\xCC"
        txBuffer = add.join(listaComandosEnviados)
        txLen = len(txBuffer)
        print("txLen: ", txLen)


        txLenBytes = txLen.to_bytes(1, byteorder='little')
        txBuffer = txLenBytes + txBuffer
    
        print("txBuffer: ", txBuffer)
        


        print("meu array de bytes tem tamanho {}" .format(len(txBuffer)))
        #faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.
       
            
        #finalmente vamos transmitir os todos. Para isso usamos a funçao sendData que é um método da camada enlace.
        #faça um print para avisar que a transmissão vai começar.
        #tente entender como o método send funciona!
        #Cuidado! Apenas trasmita arrays de bytes!
               
        

        com1.sendData(np.asarray(txBuffer))  #as array apenas como boa pratica para casos de ter uma outra forma de dados
        
        txSize = com1.tx.getStatus()
        print('enviou = {}' .format(txSize))
        # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        # O método não deve estar fincionando quando usado como abaixo. deve estar retornando zero. Tente entender como esse método funciona e faça-o funcionar.
        
        
        #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        #Observe o que faz a rotina dentro do thread RX
        #print um aviso de que a recepção vai começar.
        
        #Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        #Veja o que faz a funcao do enlaceRX  getBufferLen
      
        #acesso aos bytes recebidos
        print("_______Inicio da verificação________")
        inicio = time.time()
        end = inicio + 5
        passou = False
        while time.time()<=end:
            print("Verificando")
            time.sleep(0.5)
            if com1.rx.getIsEmpty() == False:
                rxBuffer, nRx = com1.getData(1)
                passou = True
                break
            
        if passou:    
            print(int.from_bytes(rxBuffer, byteorder='little'))
            if int.from_bytes(rxBuffer, byteorder='little') != len(listaComandosEnviados):
                print("Erro tamanho diferente")
        else:
            print("TimeOut")
        print("_______Fim da verificação________")
        
            
        
        
        
        
        
            


      
        




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
