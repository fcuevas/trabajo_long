#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 12:10:09 2019
@author: fcuevas
"""

import numpy as np
import pandas as pd
import holoviews as hv
import geoviews as gv
import cartopy

from cartopy import crs as ccrs

from bokeh.tile_providers import STAMEN_TONER
from bokeh.models import WMTSTileSource, OpenURL, TapTool, HoverTool
#from bokeh.models.callbacks import CustomJS

renderer = hv.renderer('bokeh').instance(mode='server')
hv.extension('bokeh')

# nuevo encabezado del archivo 'plantas_solares.csv'
header = ['Nombre','Nombre_prop','Nombre_grup','Comuna','Tipo_central','Nemotec','Descr','Estado','Nombre_emb',
          'Nombre_cuenca','Unid_gen','Punto_conex','Pot_max','Cons_prop','Cap_max','Pot_min','Fecha_op',
          'Clasificacion','Distribuidora','Diagrama','Tipo_conv','conv_ernc','medio_gen','tipo',
          'region','provincia','comuna','nro_comuna','sala_maq','bocatoma','represa','emb1','emb2',
          'emb3','UTM_este','UTM_oeste','huso','param_part','seguimiento','tecnologia',
          'area_pan','modelo','gen_diseno','inversion','empresa','ingSEIA','aprSEIA','link','a']

# diccionario para cambiar nombre de las regiones
reg_names = {'TARAPACÁ': 'Región de Tarapacá', 
             'ARICA Y PARINACOTA': 'Región de Arica y Parinacota',
             'ANTOFAGASTA': 'Región de Antofagasta',
             'ATACAMA': 'Región de Atacama',
             'COQUIMBO': 'Región de Coquimbo',
             'VALPARAISO':'Región de Valparaíso' ,
             'VALPARAÍSO': 'Región de Valparaíso',
             'METROPOLITANA DE SANTIAGO':'Región Metropolitana de Santiago',
             'METROPOLITANA':'Región Metropolitana de Santiago',
             'LIBERTADOR GENERAL BERNARDO OHIGGINS':"Región del Libertador Bernardo O'Higgins",
             'MAULE':"Región del Maule",
             'ÑUBLE':"Región de Ñuble",
             'BÍO BÍO':"Región del Bío-Bío",
             'ARAUCANÍA':"Región de La Araucanía",
             'DE LOS RIOS':"Región de Los Ríos",
             'DE LOS RÍOS':"Región de Los Ríos"}  
   
#'pt_size', 'Cap_max','Nombre','Comuna','Estado','Punto_conex',
#
 

# columnas a utilizar 
cols = ['Nombre','Nombre_prop','Nombre_grup','Comuna','region', 'Tipo_central','Nemotec','Descr','Estado',
        'Punto_conex','Cap_max','UTM_este','UTM_oeste','huso','Fecha_op','seguimiento','tecnologia',
          'area_pan','modelo','gen_diseno','inversion']
########################################################################################
tiles = {'OpenMap': WMTSTileSource(url='http://c.tile.openstreetmap.org/{Z}/{X}/{Y}.png'),
         'ESRI': WMTSTileSource(url='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{Z}/{Y}/{X}.jpg'),
         'Wikipedia': WMTSTileSource(url='https://maps.wikimedia.org/osm-intl/{Z}/{X}/{Y}@2x.png'),
         'Stamen Toner': STAMEN_TONER}
########################################################################################
# leer archivo 'plantas_solares.csv'
# cambio: encoding="ISO-8859-1" a encoding="utf-8"
geners = pd.read_csv('../datos/central_solar/plantas_solares.csv', 
                     encoding="utf-8",names=header,sep=';',skiprows=1,decimal=",",thousands='.')

# leer archivo ids.txt. El archivo se genera al procesar los datos del CEN y contiene el ID de todas
# las plantas solares que aparecen en los archivos de generación real
idSols = pd.read_csv('../datos/central_solar/ids.txt')
idSols.index = idSols['0']

# filtrar arreglo geners. Ahora el arreglo contiene solo las plantas solares
solar2 = geners[geners.Tipo_central == 'Solares']
# máscara para eliminar filas que contienen valores nan en la columna UTM_este
mask = solar2.UTM_este.notna()
# aplicar máscara
solar2 = solar2[mask]
# máscara para eliminar filas que el nombre es nan
mask = solar2.Nombre.notna()
# aplicar máscara
solar2 = solar2[mask]

# variable pl_sol, intersección del índice para dejar plantas que tienen datos
pl_sol = set(idSols.index).intersection(solar2.index)
pl_sol = pd.DataFrame(index = pl_sol)
pl_sol['num'] = 1

solar2['Cap_max'] = solar2['Cap_max'].str.replace(',', '.').astype(float)
solar2['UTM_este'] = solar2['UTM_este'].str.replace(',', '.').astype(float)
solar2['UTM_oeste'] = solar2['UTM_oeste'].str.replace(',', '.').astype(float)

solar2 = solar2[cols]
solar2 = pl_sol.join(solar2, how='inner')
##########
#en este lugar se modificó el csv, cambiando el huso, la utm y la potencia
huso2 = pd.DataFrame({'Nombre':['LAGUNILLA','MARÍA ELENA FV', 'LA HUAYCA II', 'CORDILLERILLA SOLAR',
            'ALTURAS DE OVALLE','MARCHIGUE II', 'CALAMA SOLAR I', 'PMG ANTAY', 'CERRO DOMINADOR',
            'PANQUEHUE II', 'LA FRONTERA','AMPARO DEL SOL','LOS LIBERTADORES', 'VILLA PRAT', 'LAS PALOMAS', 'ENCON SOLAR', 
            'PIQUERO','VALLE SOLAR ESTE 2','VALLE SOLAR OESTE 2', 'EL QUEMADO', 'PUNTA BAJA SOLAR', 'LA BLANQUINA', 'CALLE LARGA'],
                     'huso':['19J','19K','19K',
                     '19J','19J','19H','19K','19J','19k','19H','19H','19J','19H','19H',
                     '19H','19H','19H','19J','19J','19H','19J','19H','19H']},
                      index=[357,394, 403, 427, 428, 462, 480, 489,490, 501, 514, 534, 555, 559, 560,
                    573, 577,578,579, 580, 589, 592, 593])


utm=pd.DataFrame([['PAMPA SOLAR NORTE',379821, 7174646],
                  ['CORDILLERILLA SOLAR',305770,6106832],
                  ['ALTURAS DE OVALLE',285225,6617403],
            ['EL SAUCE',367831,7221038],
                  ['EL ROBLE',279532,6231325],
                  ['URIBE SOLAR',375836,7393726],
                  ['LA ESPERANZA II',266258,6197524],
          ['CERRO DOMINADOR',450821,7481640],
                  ['PANQUEHUE II',329892, 6371890],
                  ['LA FRONTERA',246626.1,6142710],
                  ['VALLE SOLAR ESTE 2',364187,6974786],
                  ['VALLE SOLAR OESTE 2',362288,6976716],
                 ['LA BLANQUINA',348247,6229034]],
                  index=[332,427,428,439,442,455,457,490, 501, 514,578, 579, 592],columns=['Nombre','UTM_este','UTM_oeste'])


potenc=pd.DataFrame([['CERRO DOMINADOR',99.05],
                  ['EL PELICANO',100],
                  ['EL SAUCE',2.98],
                  ['ENCON SOLAR',9],
                  ['FRANCISCO',3],
                  ['LAUREL',9],
                  ['MARCHIGUE II',9],
                  ['PSF LOMAS COLORADAS',1.99],
                  ['SOLAR ESPERANZA',2.87],
                  ['SOLAR JAMA',31.5],
                  ['SOLAR LOMA LOS COLORADOS',1.07]],
                  index=[490,426,439,573,500,443,462,307,346,400,317],
                  columns=['Nombre','Cap_max'])

comunas=pd.DataFrame([['LAS PALOMAS','ÑUBLE'],
                      ['VALLE SOLAR OESTE 2','ATACAMA']],
                    index=[560,579],
                    columns=['Nombre','region'])
solar2.update(huso2)
solar2.update(utm)
solar2.update(potenc)
solar2.update(comunas)
############
solar2.seguimiento = solar2.seguimiento.fillna('S/I')
solar2.tecnologia = solar2.tecnologia.fillna('S/I')
#solar2.area_pan = solar2.area_pan.fillna('S/I')
solar2.modelo = solar2.modelo.fillna('S/I')
#solar2.inversion = solar2.inversion.fillna('S/I')
##########
pt_size = np.log(solar2.Cap_max+1)
solar2['pt_size'] = pt_size
wl = []
for pl in solar2.index:
    try:
       wl_tmp = "http://localhost:5509/dash" + "?idPlanta=" + str(int(pl))
        # wl_tmp = "http://www.comitesolar.cl/dash" + "?idPlanta=" + str(int(pl))
    except (ValueError):
       wl_tmp = "http://localhost:5509/dash" + "?idPlanta="
        # wl_tmp = "http://www.comitesolar.cl/dash" + "?idPlanta="
    wl.append(wl_tmp)
    
solar2['weblink'] = wl
#######################
#Dejar solo el número del huso en una columna
hs_tmp = []
for hs in solar2.huso:
    tmp = str(hs)[0:2]
    hs_tmp.append(tmp)    
solar2['huso_num'] = hs_tmp
##########
from pyproj import Proj, transform
outProj = Proj(init='epsg:4326')
lt = []
lg = []
for utm_e, utm_o, hus in zip(solar2.UTM_este, solar2.UTM_oeste, solar2.huso_num):
    if hus == '18':
        inProj = Proj(init='epsg:32718')
    elif hus == '19':
        inProj = Proj(init='epsg:32719')
    elif hus == '12':
        inProj = Proj(init='epsg:32712')
    else:
        inProj = Proj(init='epsg:32718')
        
    x2,y2 = transform(inProj,outProj,utm_e,utm_o)
    lg.append(x2)
    lt.append(y2)

solar2['Latitud'] = lt 
solar2['Longitud'] = lg
#######################
# agrupar por regiones
solar2['Region'] = solar2.region.map(reg_names)
pot_regiones = solar2.groupby('Region').sum()
pot_regiones = pot_regiones[['Cap_max','num']]

pot_regiones = pot_regiones.rename(columns={'Region': 'NOM_REG'})
########################################################################################
regiones = pd.read_csv('../datos/shape_reg/regiones.csv')
regiones= regiones.join(pot_regiones, on=["NOM_REG"])
regiones=regiones.fillna('0')

shape_reg = '../datos/shape_reg/reg.shp'
shapesReg = cartopy.io.shapereader.Reader(shape_reg)
hover6 = HoverTool(tooltips=[("Región: ", "@NOM_REG"),("Número de plantas: ", "@num"),("Potencia (MW): ", "@Cap_max{0.0}")])
layer_reg=gv.Shape.from_records(shapesReg.records(), regiones, on='COD_REGI',
                                value='NOM_REG', index=['Cap_max','num']).opts(tools=[hover6],width=750, height=800,alpha=0.0, fill_alpha=0.0)
########################################################################################
solar_gv = gv.Dataset(solar2,kdims=['Nombre'])
########################################################################################
tile_options = dict(width=700,height=800,xaxis=None,yaxis=None,bgcolor='black',show_grid=False,tools=['pan','wheel_zoom'])
layer_1 = gv.WMTS(tiles['OpenMap']).opts(plot=tile_options)
#####################
url2 = "@weblink"
callback2 = OpenURL(url=url2)
tap2 = TapTool(callback=callback2)

ns_alpha=0.75
mt_alpha=0.0
#####################
hover2 = HoverTool(tooltips=[("Nombre central: ", "@Nombre"),
                             ("Potencia: ", "@Cap_max{(0.0)}"),
                             ("Estado: ", "@Estado"),
                             ("Fecha operación: ","@Fecha_op"),
                             ("Propietario: ","@Nombre_prop"),
                             ("Grupo: ","@Nombre_grup"),
                             ("Nombre comuna: ","@Comuna"),
                             ("Punto conexión: ","@Punto_conex"),
                             ("Seguimiento: ","@seguimiento"),
                             ("Tecnología: ","@tecnologia"),
                             ("Modelo: ","@modelo"),
                             ("Inversión: ","@inversion{0,0}")]) 

#
    
layer_2 = solar_gv.to(gv.Points , kdims=['Longitud', 'Latitud'],
              vdims=['pt_size','weblink','Cap_max','Nombre','Comuna','Estado',
                     'Nombre_prop','Nombre_grup','Punto_conex','Fecha_op','seguimiento','tecnologia',
          'area_pan','modelo','gen_diseno','inversion'], 
              crs=ccrs.PlateCarree()).options(color='orangered',size_index=2, size=4.5, tools=[hover2, tap2,'pan','wheel_zoom'],
                                  nonselection_alpha=ns_alpha, nonselection_color='orangered', legend_position='top_left',
                                  muted_alpha=mt_alpha)
######################
mapa = layer_1 * layer_reg * hv.NdOverlay({'Plantas Solares SEN':layer_2}) 
########################################################################################
doc = renderer.server_doc(mapa)
doc.title = 'Mapa'