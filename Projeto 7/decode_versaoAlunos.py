
#Importe todas as bibliotecas
from suaBibSignal import *
import peakutils    #alternativas  #from detect_peaks import *   #import pickle
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time
import soundfile as sf
import math
#funcao para transformas intensidade acustica em dB, caso queira usar
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)


def main():

    #*****************************instruções********************************
 
    #declare um objeto da classe da sua biblioteca de apoio (cedida)   
    # algo como:
    signal = signalMeu() 
       
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    sd.default.samplerate = 44100#taxa de amostragem
    sd.default.channels = 2 #numCanais # o numero de canais, tipicamente são 2. Placas com dois canais. Se ocorrer problemas pode tentar com 1. No caso de 2 canais, ao gravar um audio, terá duas listas
    duration =  4 # #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic
    

    #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes) durante a gracação. Para esse cálculo você deverá utilizar a taxa de amostragem e o tempo de gravação
    numAmostras = int(duration * sd.default.samplerate)

    # faca um print na tela dizendo que a captacao comecará em n segundos. e entao 
    print("Gravação em 3 segundos")
    #use um time.sleep para a espera
    time.sleep(3)
    #Ao seguir, faca um print informando que a gravacao foi inicializada
    print("Gravação em andamento")
    #para gravar, utilize
    audio = sd.rec(int(numAmostras), 44100, channels=1)
    sd.wait()
    print("...     FIM")
    # filename = 'CamadaFisica2022.2\Projeto 7\sinal.wav'
    # # Extract data and sampling rate from file
    # audio, fs = sf.read(filename, dtype='float32')  
    dados = audio[:,0]    
    vetor_tempo = np.linspace(0, duration, numAmostras)
    plt.plot(vetor_tempo, dados)
    
    plt.show()
    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista, isso dependerá so seu sistema, drivers etc...
    #extraia a parte que interessa da gravação (as amostras) gravando em uma variável "dados". Isso porque a variável audio pode conter dois canais e outas informações). 
    
    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
  
    # plot do áudio gravado (dados) vs tempo! Não plote todos os pontos, pois verá apenas uma mancha (freq altas) . 
       
    ## Calcule e plote o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    xf, yf = signal.calcFFT(dados, 44100)
    signal.plotFFT(dados, 44100)
    plt.show()
    #agora, voce tem os picos da transformada, que te informam quais sao as frequencias mais presentes no sinal. Alguns dos picos devem ser correspondentes às frequencias do DTMF!
    #Para descobrir a tecla pressionada, voce deve extrair os picos e compara-los à tabela DTMF
    #Provavelmente, se tudo deu certo, 2 picos serao PRÓXIMOS aos valores da tabela. Os demais serão picos de ruídos.

    # para extrair os picos, voce deve utilizar a funcao peakutils.indexes(,,)
    # Essa funcao possui como argumentos dois parâmetros importantes: "thres" e "min_dist".
    # "thres" determina a sensibilidade da funcao, ou seja, quao elevado tem que ser o valor do pico para de fato ser considerado um pico
    #"min_dist" é relatico tolerancia. Ele determina quao próximos 2 picos identificados podem estar, ou seja, se a funcao indentificar um pico na posicao 200, por exemplo, só identificara outro a partir do 200+min_dis. Isso evita que varios picos sejam identificados em torno do 200, uma vez que todos sejam provavelmente resultado de pequenas variações de uma unica frequencia a ser identificada.   
    # Comece com os valores:
    index = peakutils.indexes(yf, thres=0.3, min_dist=50)
    #printe os picos encontrados! 
    # Aqui você deverá tomar o seguinte cuidado: A funcao  peakutils.indexes retorna as POSICOES dos picos. Não os valores das frequências onde ocorrem! Pense a respeito
    
    

    teclas = [[1209, 697], [1336, 697], [1477, 697],
                  [1209, 770], [1336, 770], [1477, 770],
                  [1209, 852], [1336, 852], [1477, 852],
                   [1336, 941]]
    certo = 15
   


    freq = []
    for tecla in teclas:
        for j in index:
            if  math.isclose(xf[j], tecla[1], abs_tol=10):
               if tecla[1] not in freq:
                   freq.append(tecla[1])
            if  math.isclose(xf[j], tecla[0], abs_tol=10):
                if tecla[0]not in freq:
                    freq.append(tecla[0])



    i= 1
    
    for tecla in teclas:
        if math.isclose(min(tecla), min(freq),abs_tol=10) and math.isclose(max(tecla), max(freq),abs_tol=10):
            certo = i
        i+=1
            
    if certo == 10:
        certo = 0
    print("Frequencias dos picos {}" .format(xf[index]))
    print("Tecla pressionada: {}" .format(certo))
    print("Frequencias da tecla pressionada {}" .format(freq))
    # print("Teclas {}" .format(teclas((xf[index]) == teclas)))
    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    #print o valor tecla!!!
    #Se acertou, parabens! Voce construiu um sistema DTMF

    #Você pode tentar também identificar a tecla de um telefone real! Basta gravar o som emitido pelo seu celular ao pressionar uma tecla. 

      
    ## Exiba gráficos do fourier do som gravados 
    plt.show()

if __name__ == "__main__":
    main()
