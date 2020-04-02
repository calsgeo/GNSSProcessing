
##################################################
## autor: Camilo Leon contacto: cleon@unal.edu.co
## version: 0.1
## version python: 3.7
## fecha publicacion: 
##
## INDICACIONES PARA EL USO DEL SCRIPT
## Se requiere que el usuario actualice las dos lineas siguientes a la linea #### Info requerida al usuario
## Se debe tener permiso de escritura en la carpeta donde se ejecuta el script puesto que todo se almacenara en esta carpeta
##
## Ciudad:
## se ingresa en la linea 16, contiene el listado de estaciones magnaeco del IGAC, EAAB, UDistrial a 2020-04-01. El Diccionario de ciudades disponibles esta en la linea 109
##
## Archivos que descarga:
## 1- Informacion de los satelites: efemerides precisas, correciones de reloj
## Servicios: 
##      GLONASS
##      Center for Orbit Determination in Europe (CODE)
##      ESA
## 2- Archivos RINEX estaciones magnaeco
##      Accede al ftp del IGAC para la descarga de los archivos RINEX disponibles para la fecha de observacion GNSS. Importante tener presente las especificaciones de acceso a los archivos segun la entidad.
## 3- Coordenadas conocidas:
##      Intenta la descarga de archivos desde SIRGAS. Busca las coordenadas de las ultimas 4 semanas GPS incluyendo la correspondiente a la fecha de toma.
##      Descarga el archivo de coordenadas xyz2 del servicio Nevada Geodetic Laboratory de la estacion BOGT (unico que se mantiene actualizado)
##################################################


import datetime, calendar
import requests
import os,sys
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from pathlib import Path

rutaActual = os.path.realpath(__file__)
carpetaActual = os.path.dirname(rutaActual)

os.chdir(carpetaActual)

#### Info requerida al usuario
obsDate = datetime.date(2020,2,15)
cuidadBase = 'Bogotá'

def gpsCalendar(obsDate):
    time0 = datetime.date(1980, 1, 6)
    delta = obsDate - time0
    delta = delta.total_seconds()
    gpsWeek = int(delta//604800)
    gpsDoW = int(round((delta/604800 - gpsWeek) * 7,1))
    gpsDoY = str(obsDate.timetuple().tm_yday)
    if len(gpsDoY) ==2:
        gpsDoY = f'0{gpsDoY}'
    else:
        gpsDoY = f'{gpsDoY}'
    obsDate = obsDate.strftime('%Y-%m-%d')
    return [obsDate,gpsWeek,gpsDoW,gpsDoY]
    

def folderCreation(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def CalendarD2GPST(date):
    time0 = datetime.date(1980, 1, 6)
    delta = date - time0
    delta = delta.total_seconds()
    weeks = delta//604800 # Number of Weeks
    dow = round((delta/604800 - weeks) * 7,1)
    doy = date.timetuple().tm_yday
    strDOY = f'{doy}'
    print (f'Date: {date}')
    print (f'week: {weeks}')
    print (f'Day of Week: {int(dow)}')
    print (f'Day of Year: {doy}')
    if len(strDOY)==2:
        strDOY = '0'+strDOY
    print (f'ftp ephemerides: ftp://ftp.glonass-iac.ru/MCC/PRODUCTS/{str(date.year)[0:2]}{strDOY}')
    print (f'ftp://ftp.sirgas.org/pub/gps/SIRGAS/{int(weeks)}')
    print(f'http://ftp.aiub.unibe.ch/CODE_MGEX/CODE/2020/COM{int(weeks)}{int(dow)}.EPH.Z')
    print(f'http://ftp.aiub.unibe.ch/CODE_MGEX/CODE/2020/COM{int(weeks)}{int(dow)}.CLK.Z')

def fileDownload(path,urlAddress):
    fileName = urlAddress.split('/')[-1]
    myFile = Path(f'{path}/{fileName}')
    if not myFile.is_file():
        now = datetime.datetime.now()
        print("Download start =", now)
        try:
            with urlopen(urlAddress) as response:
                with open(f'{path}/{fileName}', 'wb') as tarball:
                    while True:
                        chunk = response.read(16384)
                        if chunk:
                            tarball.write(chunk)
                        else:
                            break
        except HTTPError as e:
            print('Error code: ', e.code)
            if e.code == 404:
                print (f'Archivo {fileName} no disponible')
        except URLError as e:
            print (f'Archivo {fileName} no disponible')
        now = datetime.datetime.now()
        print("Download ends =", now)
    else:
        print(f'El archivo {fileName} fue descargado previamente')
    

listGPSValues = gpsCalendar(obsDate)

print(f'Fecha: {listGPSValues[0]}')
print(f'Fecha: {listGPSValues[0]}')
print(f'Fecha: {listGPSValues[0]}')
print(f'Fecha: {listGPSValues[0]}')
print(f'Fecha: {listGPSValues[0]}')

for i in listGPSValues:
    print(i)

folderCreation(listGPSValues[0])
rinexPath = folderCreation(f'{listGPSValues[0]}/RINEX magnaeco') # Donde se almacenara los datos RINEX
satellitesPath = folderCreation(f'{listGPSValues[0]}/info Satelites') # Donde se almacenara los datos de los satelites
coordPath = folderCreation(f'{listGPSValues[0]}/Coordenadas Conocidas') # Donde se alacemara los archivos de coordenadas conocidas

glonass30sClock = f'ftp://ftp.glonass-iac.ru/MCC/PRODUCTS/{listGPSValues[0][:2]}{listGPSValues[3]}/final/Sta30s{listGPSValues[1]}{listGPSValues[2]}.clk'
glonassClock = f'ftp://ftp.glonass-iac.ru/MCC/PRODUCTS/{listGPSValues[0][:2]}{listGPSValues[3]}/final/Sta{listGPSValues[1]}{listGPSValues[2]}.clk'
glonassEphemeris = f'ftp://ftp.glonass-iac.ru/MCC/PRODUCTS/{listGPSValues[0][:2]}{listGPSValues[3]}/final/Sta{listGPSValues[1]}{listGPSValues[2]}.sp3'
CODEClock = f'http://ftp.aiub.unibe.ch/CODE_MGEX/CODE/{listGPSValues[0][:4]}/COM{listGPSValues[1]}{listGPSValues[2]}.CLK.Z'
CODEEphemeris = f'http://ftp.aiub.unibe.ch/CODE_MGEX/CODE/{listGPSValues[0][:4]}/COM{listGPSValues[1]}{listGPSValues[2]}.EPH.Z'

igs30sClock = f'ftp://gssc.esa.int/gnss/products/{listGPSValues[1]}/igs{listGPSValues[1]}{listGPSValues[2]}.clk_30s.Z'
igsClock = f'ftp://gssc.esa.int/gnss/products/{listGPSValues[1]}/igs{listGPSValues[1]}{listGPSValues[2]}.clk.Z'
igsEphemeris = f'ftp://gssc.esa.int/gnss/products/{listGPSValues[1]}/igs{listGPSValues[1]}{listGPSValues[2]}.sp3.Z'

estMagnaEco = {'Aguachica':['AGCA'], 'San Alberto':['ALBE'], 'San Andrés':['ANDS'], 'Apartadó':['APTO'], 'Arauca':['ARCA'], 'Becerril':['BECE'], 'Barrancabermeja':['BEJA'], 'Puerto Berrío':['BERR'], 'Bucaramanga':['BNGA'], 'Bosconia':['BOSC'], 'Barranquilla':['BQLA'], 'Buenaventura':['BUEN'], 'Cali':['CALI'], 'Puerto Carreño':['CANO'], 'Cartagena':['CART'], 'Caucasia':['CASI'], 'Cúcuta':['CUCU'], 'La Dorada':['DORA'], 'Fúquene':['FQNE'], 'Garagoa':['GARA'], 'Guaviare':['GVRE'], 'Ibagué':['IBAG'], 'Inírida':['INIR'], 'Leticia':['LETA'], 'Magangué':['GGUE'], 'Medellín':['MEDE'], 'Montería':['MOTE'], 'Neiva':['NEVA'], 'Pamplona':['PAMP'], 'Pereira':['PERA'], 'Popayán':['POPA'], 'Pasto':['PSTO'], 'Quibdó':['QUIB'], 'Riohacha':['RIOH'], 'Santa Marta':['SAMA'], 'Sincelejo':['SINC'], 'Sonsón':['SNSN'], 'Tumaco':['TUMA'], 'Tunja':['TUNA'], 'Valledupar':['VALL'], 'Villavicencio':['VIVI'], 'Yopal':['YOPA'], 'Zarzal':['ZARZ'], 'Puerto Gaitán':['RUBI'], 'Túquerres':['TUQU'], 'Florencia':['AEFO'], 'Chaparral':['AECH'], 'Ovejas':['OVEJ'], 'Bogotá':['BOGA','AEGU','BOGT','ABCC','ABPW']}

estBase = estMagnaEco[cuidadBase]

## Descarga IGAC
for estacion in estBase:
    obsFilesPath = folderCreation(f'{rinexPath}/{listGPSValues[0][:2]}o')
    gpsNavFiles = folderCreation(f'{rinexPath}/{listGPSValues[0][:2]}n')
    glonassNavFiles = folderCreation(f'{rinexPath}/{listGPSValues[0][:2]}g')
    if estacion != 'BOGT':
        downloadOBSFile = f'{estacion}{listGPSValues[3]}0.{listGPSValues[0][:2]}o.gz'
        downloadGPSFile = f'{estacion}{listGPSValues[3]}0.{listGPSValues[0][:2]}n.gz'
        downloadGLONASSFile = f'{estacion}{listGPSValues[3]}0.{listGPSValues[0][:2]}g.gz'
    else:
        downloadOBSFile = f'{estacion}{listGPSValues[3]}0.{listGPSValues[0][:2]}o.z'
        downloadGPSFile = f'{estacion}{listGPSValues[3]}0.{listGPSValues[0][:2]}n.z'
        downloadGLONASSFile = f'{estacion}{listGPSValues[3]}0.{listGPSValues[0][:2]}g.z'
    rinexOBS = f'ftp://magnaeco:magnaeco1@geodesia.igac.gov.co/{listGPSValues[3]}/{listGPSValues[0][:2]}o/{downloadOBSFile}'
    rinexGPSNAV = f'ftp://magnaeco:magnaeco1@geodesia.igac.gov.co/{listGPSValues[3]}/{listGPSValues[0][:2]}n/{downloadGPSFile}'
    rinexGLONASSNAV = f'ftp://magnaeco:magnaeco1@geodesia.igac.gov.co/{listGPSValues[3]}/{listGPSValues[0][:2]}g/{downloadGLONASSFile}'
    fileDownload(obsFilesPath,rinexOBS)
    fileDownload(gpsNavFiles,rinexGPSNAV)
    fileDownload(glonassNavFiles,rinexGLONASSNAV)

## Descarga Datos Satelitales
fileDownload(satellitesPath,CODEClock)
fileDownload(satellitesPath,CODEEphemeris)
fileDownload(satellitesPath,glonass30sClock)
fileDownload(satellitesPath,glonassClock)
fileDownload(satellitesPath,glonassEphemeris)
fileDownload(satellitesPath,igs30sClock)
fileDownload(satellitesPath,igsClock)
fileDownload(satellitesPath,igsEphemeris)

## Descarga Coordenadas conocidas
weekMin = listGPSValues[1]-3
weekMax = listGPSValues[1]+1

listWeeks = range(weekMin,weekMax)
for i in listWeeks:
    yy = str(i)[:2]
    urlSIRGAS = f'ftp://ftp.sirgas.org/pub/gps/SIRGAS/{i}/sir{yy}P{i}.crd'
    urlIGBE = f'ftp://ftp.sirgas.org/pub/gps/SIRGAS/{i}/ibg{yy}P{i}.crd'
    fileDownload(coordPath,urlSIRGAS)
    fileDownload(coordPath,urlIGBE)
urlNGL = 'http://geodesy.unr.edu/gps_timeseries/txyz/IGS14/BOGT.txyz2'
fileDownload(coordPath,urlNGL)


print('Descarga finalizada')