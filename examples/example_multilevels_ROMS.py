#!usr/bin/env python
from EZmovie import lib_EZmovie as lez
import datetime as dt
import matplotlib.cm as cm

run1 = {'grid':'CCS1','name':'CCS1-RD.NVOcobalt29R','directory':'/Volumes/P7/ROMS/CCS1/CCS1-RD.NVOcobalt29R/'}

sst      = {'variable':'temp','type':'map','level':49, 'vmin':0,'vmax':30,'filetype':'avg','pal':cm.gist_ncar}
t100     = {'variable':'temp','type':'map','depth':100,'vmin':6,'vmax':20,'filetype':'avg','pal':cm.gist_ncar}
t200     = {'variable':'temp','type':'map','depth':200,'vmin':6,'vmax':20,'filetype':'avg','pal':cm.gist_ncar}

chl0     = {'variable':'chl','type':'map','level':49, 'vmin':0,'vmax':1,   'filetype':'dia','pal':cm.bwr}
chl100   = {'variable':'chl','type':'map','depth':100,'vmin':0,'vmax':0.1, 'filetype':'dia','pal':cm.bwr}
chl200   = {'variable':'chl','type':'map','depth':200,'vmin':0,'vmax':0.01,'filetype':'dia','pal':cm.bwr}

diag1 = {'label':'SST 2PS',  'run':run1,'row':1,'col':1}
diag2 = {'label':'T100m 2PS','run':run1,'row':1,'col':2}
diag3 = {'label':'T200m 2PS','run':run1,'row':1,'col':3}
diag4 = {'label':'Surface logChl 2PS','run':run1,'row':2,'col':1}
diag5 = {'label':'logChl 100m 2PS','run':run1,'row':2,'col':2}
diag6 = {'label':'logChl 200m 2PS','run':run1,'row':2,'col':3}

diag1.update(sst)
diag2.update(t100)
diag3.update(t200)
diag4.update(chl0)
diag5.update(chl100)
diag6.update(chl200)

diags = [diag1,diag2,diag3,diag4,diag5,diag6]

start = dt.datetime(1996,1,2)
end = dt.datetime(1996,12,27)
#end = dt.datetime(2006,12,30)

movie = lez.EZmovie(diags,plotdir='/Volumes/P4/workdir/raphael/Movies_EZ/')
movie.ROMS_movie('multilevels_T_Chl.gif',start,end)
