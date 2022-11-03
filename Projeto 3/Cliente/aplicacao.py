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
serialName = "COM4"                  # Windows(variacao de)


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
    print("size",head[1])
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
    

    return f  

def criacaoDePacotes(dados,tipo):
    tamanho = len(dados)
    
    pacotes = []
    id = 0
    for i in range(0, tamanho, 114):
        dadosPacote = dados[i:i+114]
        size = len(dadosPacote)
        
        head = headPacote(id, size, tipo, int(tamanho/114))
        eop = eopPacote()

        pacotes.append(head+ (dadosPacote)  + eop)
        id += 1
    if tamanho == 0:
        head = headPacote(id, 0,tipo, int(tamanho/114))
        eop = eopPacote()

        pacotes.append(head + eop)
    print(pacotes)
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
        


        print("_______Inicio da verificação________")
        #Enviando o handshake
        continua = True
        first = True
        while continua:
            if first:
                print("Byte de Sacrificio")
                com1.sendData(b'00')
                time.sleep(1)
                first = False
            dados = b'\xcc'*0
            time.sleep(0.1)
            for pacote in criacaoDePacotes(dados,1):
                print(len(pacote))
                com1.sendData(pacote)
                time.sleep(.2)
                print("Pacote enviado")
            inicio = time.time()
            end = inicio + 5
            passou = False
            
            while time.time()<=end:
                print("Verificando")
                time.sleep(0.5)
                if com1.rx.getIsEmpty() == False:
                    rxBuffer, nRx = com1.getData(10)
                    if rxBuffer[2] == 0x02:
                        print("Handshake recebido")
                        passou = True
                        break
                    else:
                        print("Handshake Errado")
                        quer = input ("Quer tentar denovo? S/N")
                        if quer == "S":
                            continua = True 
                            first = True
                            break
                        else:
                            continua = False
                            break
            if not passou:
                print("Handshake não recebido")
                quer = input ("Quer tentar denovo? S/N")
                if quer == "S":
                    continua = True 
                    first = True
                    
                else:
                    continua = False
            if passou:
                continua = False
                    
        
        if passou == True:
            print("Enviando dados")
            with open ("Projeto 3\\Cliente\\flamengo.txt","rb") as file:
                dados = file.read()

            
            vai  = True
            while vai:
                vai = False
                for pacote in criacaoDePacotes(dados,3):
                    continua = False
                    
                    print(len(pacote))
                    com1.sendData(pacote)
                    time.sleep(.2)
                    print("Pacote enviado" ,pacote)
                    com1.rx.clearBuffer()
                    rxBuffer, nRx = com1.getData(10)
                    if rxBuffer[2] == 0x04:
                        continua = True
                        print("Dados recebidos")
                    else:
                        continua = False
                        print("Erro de transmissão, pacote corrompido")
                        vai = False
                        break
                        




           
                  
        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são um array bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.
        
        #txBuffer = imagem em bytes!
        imageR = 'mengo.jpeg'
        imageW = 'mengo_transmitido.jpeg'
        



        #faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.
       
            
        #finalmente vamos transmitir os todos. Para isso usamos a funçao sendData que é um método da camada enlace.
        #faça um print para avisar que a transmissão vai começar.
        #tente entender como o método send funciona!
        #Cuidado! Apenas trasmita arrays de bytes!
               
        
        #as array apenas como boa pratica para casos de ter uma outra forma de dados
        
        # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        # O método não deve estar fincionando quando usado como abaixo. deve estar retornando zero. Tente entender como esse método funciona e faça-o funcionar.
        
        
        #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        #Observe o que faz a rotina dentro do thread RX
        #print um aviso de que a recepção vai começar.
        
        #Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        #Veja o que faz a funcao do enlaceRX  getBufferLen
      
        #acesso aos bytes recebidos
        
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
