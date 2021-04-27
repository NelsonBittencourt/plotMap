# -*- coding: utf-8 -*-
"""
Created on Sat Aug 25 20:35:13 2018

@author: Nelson Rossi Bittencourt

******************************************************************************
Rotina para plotar dados de chuva a partir de uma arquivo no formato GRADS 
Neste exemplo, o arquivo GRADS tem nome 'ETA_24_000.bin'
O arquivo 'shad50_1.gif' é uma representação oficial do arquivo 'bin' acima
Esta rotina é somente uma demonstração e não foi otimizada para uso comercial
******************************************************************************

Alterado em 19/03/2021 para ser executado no Python 3.7 (VS Code)

"""

# Importação das dependências
# Duas linhas abaixo foram removidas em 19/03/2021. Eram utilizada na versão anterior do Python
# import os
# os.environ["PROJ_LIB"] = "C:\\ProgramData\\Anaconda3\\Library\\share"

# Em 26/03/2021 
# Foi necessário instalar o matplotlib no Windows com: py -m pip install matplotlib
# Foi necessário baixar e instalar 'basemap-1.2.2-cp39-cp39-win_amd64.whl'
#   O arquivo foi obtido em https://www.lfd.uci.edu/~gohlke/pythonlibs/
#   O arquivo foi copiado no diretório atual e instalado com py -m pip install basemap-1.2.2-cp39-cp39-win_amd64.whl

# Em 20/04/2021
# Instalar Cartopy do mesmo site acima
# Instalar scipy


import matplotlib as mpl
import matplotlib.pyplot as plt
import cartopy
import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature

import numpy as np
import struct

#import plotMap
#from plotMap import Mapa

#meuMapa1 = Mapa()
#meuMapa2 = Mapa()
#meuMapa1.nome = 'Teste1'
#meuMapa2.nome = 'Teste2'
#plotMap.testeMapa(meuMapa2)




# Abrir arquivo de dados binários com dados de chuva
# O arquivo está no formato GRADS sendo necessário convertê-lo
arquivo_dados = open('ETA_24_000.bin','rb')

# Lista temporária contendos os dados de chuva
chuva = []

# Loop para ler os dados do grads
try:
    byte1 = arquivo_dados.read(4)                           # lê 4 bytes 
    chuva.append(struct.unpack('f', byte1)[0])              # Converte para float
    while byte1 != b"":                                     # Repete o processo até o fim do arquivo
        byte1 = arquivo_dados.read(4)
        if len(byte1)==4:                                   # Verifica se o dado lido é mesmo um byte
            chuva.append(struct.unpack('f', byte1)[0])       
finally:
    arquivo_dados.close()                                   # Fecha o arquivo em caso de erro
                                                    

# Fecha o arquivo de dados em condição normal
arquivo_dados.close()

# Converte a lista em matriz e redimensiona
# Este procedimento é necessário para adequar as dimensões das matrizes 
# no momento de utilizar a função p
chuva = np.array(chuva)
chuva = np.reshape(chuva,(157,-1))

# longitudes
lons = np.arange(-83.0,-25.6,0.4)

# latitudes
lats = np.arange(-50.2,12.6,0.4)

# Determina o tamanho do gráfico no console do Python
fig = plt.figure(figsize=(5,5))

# Detemina tipo de projeção
ax = fig.add_subplot(1,1,1,projection=ccrs.PlateCarree())

# Determina coordenada do mapa

# set_extent(loni, lonf, lati, latf)
ax.set_extent([-75,-35,-35,5],ccrs.PlateCarree() )



# Adiciona as caracteristica do mapa
ax.add_feature(cartopy.feature.LAND)
#ax.add_feature(cartopy.feature.OCEAN)
ax.add_feature(cartopy.feature.COASTLINE)
ax.add_feature(cartopy.feature.BORDERS)


fname = "BRA_adm1.shp"
shape_feature = ShapelyFeature(Reader(fname).geometries(), ccrs.PlateCarree(), facecolor='none')

ax.add_feature(shape_feature)

# Cria a escala de valores para escala de cores
valores_escala = [0,5,10,15,20,25,30,40,50,75,100,150,200]
etiquetas_escala = valores_escala

# Cria o gráfico do tipo contornos preenchidos
filled = ax.contourf(lons, lats, chuva, transform=ccrs.PlateCarree(), cmap='hsv')

# Ajusta a barra de cores
cmap = mpl.cm.viridis.with_extremes(over='red', under='white')
norm = mpl.colors.BoundaryNorm(valores_escala, cmap.N, extend='both')

cbar = fig.colorbar(
            mpl.cm.ScalarMappable(norm=norm, cmap=cmap),
            orientation='horizontal',
            label="Precipitação (mm)",
            spacing = 'uniform')


cbar.set_ticks(valores_escala)
cbar.set_ticklabels(etiquetas_escala)

# Carrega um arquivo do tipo shapefile    
# Foram mantidos todos os arquivos 'BRA_adm1' por convenção.
# TODO: verificar que arquivos 'BRA_adm1' são realmente necessários
#m.readshapefile('BRA_adm1', 'Brasil')

# Define título do gráfico 
plt.title('Chuva Prevista - Modelo ETA (mm)')

# Adiciona grid de coordenadas ao mapa
#paralelos = np.arange(-35,5,5)
#meridianos = np.arange(-75,-30,5)
#m.drawparallels(paralelos,labels=[True,False,False,False])
#m.drawmeridians(meridianos,labels=[False,False,False,True])

# Salva o gráfico em um arquivo png com resolução de 200 dpi
#plt.savefig('arquivo_saida.png', bbox_inches='tight', dpi=240)
plt.show()  # Adicionado em 19/03/2021
