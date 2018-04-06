#!usr/bin/env python
from EZmovie import lib_EZmovie as lez
import datetime as dt
import matplotlib.cm as cm

run1 = {'grid':'CCS1','name':'CCS1-RD.NVOcobalt29R','directory':'/Volumes/P7/ROMS/CCS1/CCS1-RD.NVOcobalt29R/'}
run2 = {'grid':'CCS1','name':'CCS1-RD.NVOcobalt31S','directory':'/Volumes/P7/ROMS/CCS1/CCS1-RD.NVOcobalt31S/'}

tsec1      = {'variable':'temp','type':'section','jindex':275,'vmin':-1,'vmax':20,'filetype':'avg','pal':cm.gist_ncar,'max_depth':200}
chl_sec1   = {'variable':'chl', 'operation':'log10','type':'section','jindex':275,'vmin':-2,'vmax':2, 'filetype':'dia','pal':cm.gist_ncar,'max_depth':200}

diag1 = {'label':'section Temp   2PS','run':run1,'row':1,'col':1}
diag2 = {'label':'section logChl 2PS','run':run1,'row':1,'col':2}
diag3 = {'label':'section Temp   3PS','run':run2,'row':2,'col':1}
diag4 = {'label':'section logChl 3PS','run':run2,'row':2,'col':2}

diag1.update(tsec1)
diag2.update(chl_sec1)
diag3.update(tsec1)
diag4.update(chl_sec1)

diags = [diag1,diag2,diag3,diag4]

start = dt.datetime(1996,1,2)
end = dt.datetime(1996,12,27)
#end = dt.datetime(2006,12,30)

movie = lez.EZmovie(diags,plotdir='/Volumes/P4/workdir/raphael/Movies_EZ/')
movie.ROMS_movie('compare_section_2PS-3PS.gif',start,end)
