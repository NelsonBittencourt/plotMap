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

import matplotlib as mpl
import matplotlib.pyplot as plt
import cartopy
import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature

# Classe para definir o layout do mapa a plotar
class Mapa:    
    def __init__(self):
        self.mapa_nome = ''
        self.mapa_tipo = ''        
        self.barraCores_titulo = ''
        self.barraCores_extensao = ''  
        self.barraCores_orientacao = ''  
        self.barraCores_valores = []  
        self.barraCores_codigos = []


# Função para plotar um mapa com barra de cores
def plotarMapa(titulo_mapa, lons, lats, dados, shapeFile, modeloMapa, destino=''):
    """
    Rotina para plotar um mapa considerando os dados fornecidos
    Argumentos:
        tituloMapa  - Título da primeira linha sobre a figura do mapa
        lons        - lista com as longitutes
        lats        - lista com as latitudes
        shapeFike   - nome do arquivo de shapefile para ou deixar em branco para exibir na tela        
        modeloMapa  - string ou 'Mapa'. 
                    A string deve conter um nome de arquivo de template válido.
                    Mapa deve conter uma instância do tipo 'Mapa'        

        destino     - nome do arquivo de saída para a figura. Se não declarado, exibe na tela

    """

    # Verifica o tipo de 
    if type(modeloMapa) is str:
        myMap = loadMapTemplate(modeloMapa)
    elif type(modeloMapa) is Mapa:
        myMap = modeloMapa
    else:
        raise NameError("O argumento 'mapa' deve ser uma string ou um tipo 'Mapa'!")
    
    # Fecha uma figura anterior, se houve    
    plt.close()

    # Determina o tamanho do gráfico no console do Python
    fig = plt.figure(figsize=(5,5))  

    # Detemina tipo de projeção
    ax = fig.add_subplot(1,1,1,projection=ccrs.PlateCarree())
   
    # Determina coordenada do mapa

    # set_extent(loni, lonf, lati, latf)
    ax.set_extent([-75,-35,-35,5],ccrs.PlateCarree())
    
    # Adiciona as caracteristica do mapa
    ax.add_feature(cartopy.feature.LAND)
    #ax.add_feature(cartopy.feature.OCEAN)
    ax.add_feature(cartopy.feature.COASTLINE)
    ax.add_feature(cartopy.feature.BORDERS)
        
    shape_feature = ShapelyFeature(Reader(shapeFile).geometries(), ccrs.PlateCarree(), facecolor='none')
    ax.add_feature(shape_feature)

    # Cria mapa de cores
    cmap = (mpl.colors.ListedColormap(myMap.barraCores_codigos))
     
    # Cria o gráfico do tipo contornos preenchidos
    filled = ax.contourf(lons, lats, dados, transform=ccrs.PlateCarree(), cmap=cmap)

    # Ajusta a barra de cores
    
    if myMap.barraCores_orientacao!="None":
        
        norm = mpl.colors.BoundaryNorm(myMap.barraCores_valores, cmap.N, extend=myMap.barraCores_extensao)

        cbar = fig.colorbar(
                    mpl.cm.ScalarMappable(norm=norm, cmap=cmap),
                    orientation= myMap.barraCores_orientacao,
                    label= myMap.barraCores_titulo,
                    spacing = 'uniform', pad = 0.10, fraction = 0.05)

        cbar.set_ticks(myMap.barraCores_valores)        
    
    # Define título do gráfico 
    plt.title(titulo_mapa)

    # Adiciona grid          
    g1=ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,linewidth=1, color='gray', alpha=0.5, linestyle='--')
    g1.top_labels = False
    g1.right_labels = False
    g1.xlabel_style = {'size': 9, 'color': 'blue', 'weight': 'bold'}
    g1.ylabel_style = {'size': 9, 'color': 'red', 'weight': 'bold'}
    
    # Mostra ou salva
    if destino == '':        
        plt.show(block=True)
        
    else:              
        fig.savefig(destino)
    

def loadMapTemplate(arquivoTemplateMapa):
    """
    Rotina para ler o template do mapa de um arquivo
    Argumentos:

        arquivoTemplateMapa - nome do arquivo contendo template do Mapa        


    Retorno:
        objeto Mapa (ver definição da classe 'Mapa' neste arquivo)
        Utilize esse objeto para customizar um template de mapa lido de um arquivo
        ou use-o para criar um template em tempo de execução
    """
    
    # Lista com as linhas lidas do arquivo de template de um mapa
    lines = []

    # Linha corrente do arquivo 
    num_line = 0

    # Número de linhas válidas esperada
    check_valid_lines = 10

    # Contados de linhas válidas
    valid_lines = 0

    # Dicionário com dados lidos
    map_dict = {}

    # Abre arquivo e lê as linhas válidas
    # O caracter considerado '#' é utilizado para comentários
    # Se a número de linhas válidas for diferente do esperado, lança uma exceção  
    with open(arquivoTemplateMapa, 'r') as f:
        
        for line in f:
            line = line.rstrip()
            num_line = num_line + 1
            prefix = line.strip()

            if len(prefix) > 0 and prefix[0] != '#':
                if (':' in line):
                    lines.append(line)
                    valid_lines = valid_lines + 1
                    listValues = line.split(':')                    
                    map_dict[listValues[0]]= listValues[1]                    
                else:
                    raise NameError("Linha inválida no arquivo de template '{}'. Verique a linha {}.".format(arquivoTemplateMapa, num_line))


    # Aloca os valores em um objeto do tipo 'Mapa'
    local_map = Mapa()        
    local_map.barraCores_orientacao = map_dict['barra_cores_orientacao']
    local_map.barraCores_titulo = map_dict['barra_cores_titulo']
    local_map.barraCores_extensao = map_dict['barra_cores_extensao']

    tmp = map_dict['barra_cores_valores'].split(',')    
    local_map.barraCores_valores = [float(i) for i in tmp]    
    local_map.barraCores_codigos = map_dict['barra_cores_codigos'].split(',')    
    
    if valid_lines !=check_valid_lines:
        raise NameError("O arquivo de template '{}' contêm {} linhas válidas, quando o esperado são {} linhas.".format(arquivoTemplateMapa,valid_lines,check_valid_lines))

    return(local_map)
        

