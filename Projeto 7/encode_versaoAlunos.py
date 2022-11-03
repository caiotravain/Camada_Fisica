
#importe as bibliotecas
from email.mime import audio
from pydub import AudioSegment
from re import X
import wavio
from suaBibSignal import *
from math import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt

#funções a serem utilizadas
# def signal_handler(signal, frame):
#         print('You pressed Ctrl+C!')
#         sys.exit(0)

#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)




def main():
    
   
    #********************************************instruções*********************************************** 
    # seu objetivo aqui é gerar duas senoides. Cada uma com frequencia corresposndente à tecla pressionada
    # então inicialmente peça ao usuário para digitar uma tecla do teclado numérico DTMF
    # agora, voce tem que gerar, por alguns segundos, suficiente para a outra aplicação gravar o audio, duas senoides com as frequencias corresposndentes à tecla pressionada, segundo a tabela DTMF
    # Essas senoides tem que ter taxa de amostragem de 44100 amostras por segundo, entao voce tera que gerar uma lista de tempo correspondente a isso e entao gerar as senoides
    # Lembre-se que a senoide pode ser construída com A*sin(2*pi*f*t)
    # O tamanho da lista tempo estará associada à duração do som. A intensidade é controlada pela constante A (amplitude da senoide). Construa com amplitude 1.
    # Some as senoides. A soma será o sinal a ser emitido.
    # Utilize a funcao da biblioteca sounddevice para reproduzir o som. Entenda seus argumento.
    # Grave o som com seu celular ou qualquer outro microfone. Cuidado, algumas placas de som não gravam sons gerados por elas mesmas. (Isso evita microfonia).
    
    # construa o gráfico do sinal emitido e o gráfico da transformada de Fourier. Cuidado. Como as frequencias sao relativamente altas, voce deve plotar apenas alguns pontos (alguns periodos) para conseguirmos ver o sinal
    

    print("Inicializando encoder")
    numero = input("Digite um número de 0 a 9: ")

    print("Aguardando usuário")
    def calculoSenoide(numero):
        if numero == '1':
            f1 = 697
            f2 = 1209
        elif numero == '2':
            f1 = 697
            f2 = 1336
        elif numero == '3':
            f1 = 697
            f2 = 1477
        elif numero == '4':
            f1 = 770
            f2 = 1209
        elif numero == '5':
            f1 = 770
            f2 = 1336
        elif numero == '6':
            f1 = 770
            f2 = 1477
        elif numero == '7':
            f1 = 852
            f2 = 1209
        elif numero == '8':
            f1 = 852
            f2 = 1336
        elif numero == '9':
            f1 = 852
            f2 = 1477
        elif numero == '0':
            f1 = 941
            f2 = 1336
        else:
            print("Número inválido")
            return
        return [f1, f2]



    sinal = calculoSenoide(numero)
    fs = 44100
    t = 3
    t = np.arange(0, t, 1/fs)

    #Cálculo das senoides
    sinal1 = np.sin(2*pi*sinal[0]*t)
    sinal2 = np.sin(2*pi*sinal[1]*t)
    sinal = sinal1 + sinal2

    print("Gerando Tons base")
    print("Executando as senoides (emitindo o som)")
    #Tocando o sinal
    sd.play(sinal, fs)
    sd.wait()
    wavio.write("sinal.wav", sinal, fs, sampwidth=3)

    #Plot do sinal
    plt.plot(t, sinal)
    plt.xlabel('Tempo (s)')
    plt.ylabel('Amplitude')
    plt.title('Gráfico das duas frequências somadas no tempo')
    plt.axis([0, 0.01, -2, 2])
    plt.show()


    #Plot da FFT
    sinal1 = signalMeu()
    sinal1.plotFFT(sinal, fs)
    plt.xlabel('Tempo (s)')
    plt.ylabel('Amplitude')
    plt.title('Gráfico da frequências do sinal emitido (COM FOURIER) no tempo')
    plt.show()
    # print(.format(NUM))
    # sd.play(tone, fs)
    # # Exibe gráficos
    # plt.show()
    # # aguarda fim do audio
    # sd.wait()
    

if __name__ == "__main__":
    main()
