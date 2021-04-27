import plotMap
import numpy as np
import struct

chuva = []

arquivo_dados = open('ETA_24_000.bin','rb')
    # Loop para ler os dados do grads
try:
    byte1 = arquivo_dados.read(4)                           # lê 4 bytes 
    chuva.append(struct.unpack('f', byte1))                 # Converte para float
    while byte1 != b"":                                     # Repete o processo até o fim do arquivo
        byte1 = arquivo_dados.read(4)
        if len(byte1)==4:                                   # Verifica se o dado lido é mesmo um byte
            chuva.append(struct.unpack('f', byte1))        
finally:
    arquivo_dados.close()                                   # Fecha o arquivo em caso de erro


lons = np.arange(-83.0,-25.6,0.4)
lats = np.arange(-50.2,12.6,0.4)
chuva = np.array(chuva)
chuva = np.reshape(chuva,(157,-1))
shapeFile = 'BRA_adm1.shp'
mapTemplate = 'mapateste.dat'
titulo_mapa = 'Precipitação (mm)\nTeste'

# Teste 1: usando o template do mapa
plotMap.plotarMapa(titulo_mapa, lons,lats,chuva,shapeFile,mapTemplate)

# Teste 2: carregando o template e alterando uma característica
meuMapaCustomizado = plotMap.loadMapTemplate(mapTemplate)
meuMapaCustomizado.barraCores_titulo = "barra de cores alterada!"
meuMapaCustomizado.barraCores_orientacao = 'vertical'
plotMap.plotarMapa(titulo_mapa, lons,lats,chuva,shapeFile,meuMapaCustomizado, 'Teste2.jpg')