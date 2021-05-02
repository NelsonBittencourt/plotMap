# -*- coding: utf-8 -*-

"""
******************************************************************************
exemplos.py - Rotina para testar o módulo 'plotMap'
              Nestes teste será lido um arquivo binário no formato 'Grads' com 
              dados de chuva prevista. Os dados deste arquivo serão plotados em
              um mapa com modelo semelhante ao utilizado pelo ONS.

Autor   : Nelson Rossi Bittencourt
Versão  : 0.1
Licença : MIT
Dependências: numpy, struct, plotMap
******************************************************************************
"""

import numpy as np
import struct
import plotMap

def main():

    # Lista para acomodar os dadoss de chuva a serem lidos do arquivo tipo 'Grads'.
    chuva = []

    # Abre o arquivo 'ETA_24_000.bin' e aloca seus dados na lista 'chuva'.
    arquivo_dados = open('ETA_24_000.bin','rb')
    
    try:
        byte1 = arquivo_dados.read(4)                           # lê 4 bytes de dados.
        chuva.append(struct.unpack('f', byte1))                 # Converte para float.
        while byte1 != b"":                                     # Repete o processo até o fim do arquivo.
            byte1 = arquivo_dados.read(4)
            if len(byte1)==4:                                   # Verifica se o dado lido é mesmo um byte.
                    chuva.append(struct.unpack('f', byte1))        
        arquivo_dados.close()
    finally:
        arquivo_dados.close()                                   # Fecha o arquivo em caso de erro.

    # listas com as coordenads (longitudes e latitudes) do arquivo 'Grads'.
    # Estes valores poderiam ser lidos do arquivo de configuração. Por simplicidade, foram inseridos no código.
    # Ver método 'arange' do 'numpy' para detalhes do funcionamento da construção das listas.
    lons = np.arange(-83.0,-25.6,0.4)
    lats = np.arange(-50.2,12.6,0.4)

    # Transforma a lista 'chuva' em uma matriz e altera o seu 'formato' para compatibilidade com a o número de longitutes 
    # e latitudes. Veja o método 'reshape' do 'numpy' para maiores detalhes.
    chuva = np.array(chuva)
    chuva = np.reshape(chuva,(157,-1))

    # Nome de shape para obter os estados brasileiros.
    # São necessários os arquivos *.shp, *.shx e *.dbf
    shapeFile = 'shapes/BRA_adm1.shp'

    # Nome do arquivo com parâmetros do mapa.
    mapTemplate = 'templates/ChuvaPrevistaONS.dat'

    # Título do mapa
    titulo_mapa = 'Precipitação (mm)\nTeste'

    # Exemplo 1: Usando o modelo de mapa de forma integral.
    #            Neste caso:
    #                        1) o mapa utilizará todos os parâmetros do arquivo especificado em 'mapTemplate';
    #                        2) O quinto argumento do método 'plotarMapa' corresponde ao nome do arquivo contendo 
    #                        os parâmetros do modelo de mapa.               

    plotMap.plotarMapa(titulo_mapa, lons,lats,chuva,shapeFile,mapTemplate, 'Teste1.jpg')


    # Exemplo 2: Usando o modelo de mapa de forma parcial.
    #            Neste exemplo:
    #                           1)Vamos ler os parâmetros do mapa modelo para o objeto 'Mapa', alterar alguns
    #                           parâmetros e plotar os mesmos dados de chuva;
    #                           2) O quinto argumento do método 'plotarMapa' corresponde ao objeto 'Mapa' que
    #                           teve seus parâmetros alterados.

    # O método 'loadMapTemplate' recebe o nome do arquivo de modelo do mapa e retorna um objeto 'Mapa'.
    meuMapaCustomizado = plotMap.loadMapTemplate(mapTemplate)

    # Com o objeto 'Mapa', podemos alterar quaisquer dos parâmetros do objeto.
    meuMapaCustomizado.barraCores_titulo = "barra de cores alterada!"
    meuMapaCustomizado.barraCores_orientacao = 'vertical'
    meuMapaCustomizado.barraCores_posicao = 'left' 

    plotMap.plotarMapa(titulo_mapa, lons,lats,chuva,shapeFile,meuMapaCustomizado, 'Teste2.jpg')


    # Exemplo 3: Repetindo o exemplo 2, com mapa na tela.
    #            Para isso, basta não informar nada como 'destino' (sexto argumento) do método 'plotarMapa'.

    plotMap.plotarMapa(titulo_mapa, lons,lats,chuva,shapeFile,meuMapaCustomizado)


if __name__ == '__main__':
    main()