# -*- coding: utf-8 -*-

"""
******************************************************************************
Rotina para testar o módulo 'plotMap'
Nestes teste será lido um arquivo binário no formato 'Grads' com dados de chuva
prevista. Os dados deste arquivo serão plotados em um mapa com modelo semelhante
ao utilizado pelo ONS.

Autor   : Nelson Rossi Bittencourt
Versão  : 0.121
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
    arquivo_dados = 'ETA_24_000.bin'
    
    # Lê o arquivo de dados binário tipo 'Grads'    
    try:
        with open(arquivo_dados, 'rb') as f:
            while True:
                byte = f.read(4)
                if not byte:
                    break                
                chuva.append(struct.unpack('f',byte))                   
    except:
        raise NameError('Erro ao tentar abrir/acessar arquivo: {}'.format('ETA_24_000.bin'))       
  

    # listas com as coordenads (longitudes e latitudes) do arquivo 'Grads'.
    # Estes valores poderiam ser lidos do arquivo de configuração. Por simplicidade, foram inseridos no código.
    # Ver método 'arange' do 'numpy' para detalhes do funcionamento da construção das listas.
    lons = np.arange(-83.0,-25.6,0.4)
    lats = np.arange(-50.2,12.6,0.4)

    # Transforma a lista 'chuva' em uma matriz e altera o seu 'formato' para compatibilidade com a o número de longitutes 
    # e latitudes. Veja o método 'reshape' do 'numpy' para maiores detalhes.
    chuva = np.array(chuva,dtype=float)    
    chuva = np.reshape(chuva,(157,-1))
    
    # Nome do arquivo com parâmetros do mapa.
    mapTemplate = 'templates/ChuvaPrevistaONS.dat'

    # Título do mapa
    titulo_mapa = 'Precipitação (mm)\nTeste'
        
    # Utilize a classe 'ArquivoShape' para criar uma instância de um arquivo shape com uma cor e uma 
    # espessura da linha especificados.
    # Para utilizar arquivos tipo 'shape', são necessários os arquivos '*.shp', '*.shx' e '*.dbf'.
    # Repare que você ainda poderá utilizar como 'shapeFile' apenas uma 'string' ou um objeto 'ArquivoShape'.

    # Criando um objeto 'ArquivoShape' com os Estados do Brasil, cor da linha cinza e espessura da linha 1.0.
    shapeEstadosBrasil = plotMap.ArquivoShape(nomeArquivo='shapes/BRA_adm1.shp', corLinha='gray', espLinha=1.0)
    
    # Criando um objeto 'ArquivoShape' com das bacias hidrográficas , cor da linha azul e espessura da linha 0.25.
    shapeBaciasBrasil =  plotMap.ArquivoShape(nomeArquivo='shapes/Bacias.shp', corLinha='blue', espLinha=0.25)    
    
    # Lista contendo os dois 'ArquivosShape' acima. Ao passar uma lista de shapes, a rotina 'plotarMapa' irá adicionar
    # cada arquivo ao mapa na mesma ordem da lista.
    listaShapes = [shapeEstadosBrasil, shapeBaciasBrasil]


    # Exemplo 1: Usando o modelo de mapa de forma integral.
    # Neste caso o mapa utilizará todos os parâmetros do arquivo especificado em 'mapTemplate'.
    # Também usaremos os 'shapes' dos Estados e das bacias.         
    plotMap.plotarMapa( titulo=titulo_mapa,
                        lons=lons,
                        lats=lats, 
                        dados=chuva,
                        modeloMapa=mapTemplate,                       
                        destino='exemplo1_mapaTipoONS.jpg',
                        shapeFile=listaShapes                   
                        )


    # Exemplo 2: Usando o modelo de mapa de forma parcial.
    # Neste exemplo vamos ler os parâmetros do mapa modelo para o objeto 'Mapa' e alterar alguns.
    # O método 'loadMapTemplate' recebe o nome do arquivo de modelo do mapa e retorna um objeto 'Mapa'. 
    # Usaremos somente o 'shape' dos Estados.   
    meuMapaCustomizado = plotMap.loadMapTemplate(mapTemplate)

    # Com o objeto 'Mapa', podemos alterar quaisquer dos parâmetros.
    meuMapaCustomizado.barraCores_titulo = "barra de cores alterada!"
    meuMapaCustomizado.barraCores_orientacao = 'vertical'
    meuMapaCustomizado.barraCores_posicao = 'right' 
    meuMapaCustomizado.barraCores_dist = 0.05
    plotMap.plotarMapa(titulo_mapa, lons,lats,chuva,meuMapaCustomizado, 'exemplo2_MapaCustomizado.jpg',listaShapes[0])


    # Exemplo 3: Repetindo o exemplo 2, com mapa na tela.
    # Para isso, basta não informar nada como 'destino' (sexto argumento) do método 'plotarMapa'.
    # Importante: como o parâmetro 'destino' não foi definido, é mandatório nomear o parâmetro posterior a ele na
    # lista de argumentos (neste caso 'shapeFile').
    # Usaremos somente o 'shape' das bacias.
    plotMap.plotarMapa(titulo_mapa, lons,lats,chuva, meuMapaCustomizado, shapeFile=listaShapes[1])


    # Exemplo 4: Repetindo o exemplo 2, com mapa do tipo 'anomalias' do site WXMaps.
    # Neste exemplo, não será utilizado 'shapefile'.   
    plotMap.plotarMapa( titulo='Anomalia (mm)\nWXMaps',
                        lons=lons,
                        lats=lats,
                        dados=chuva,
                        modeloMapa='templates/AnomaliaWxmaps.dat',
                        destino='exemplo4_MapaTipoWXMaps_Anomalia.jpg'
                       )    


if __name__ == '__main__':
    main()