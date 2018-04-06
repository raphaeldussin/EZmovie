#!usr/bin/env python
from EZmovie import lib_EZmovie as lez
import datetime as dt
import matplotlib.cm as cm

run1 = {'grid':'','name':'','directory':'/Users/raphael/WORK/RUNS_MITGCM/tutorial_global_oce_latlon/run'}

ssh      = {'variable':'Eta','type':'map','vmin':-2,'vmax':2,'filetype':'','pal':cm.gist_ncar}
sst      = {'variable':'T','type':'map','level':0,'vmin':-2,'vmax':30,'filetype':'','pal':cm.gist_ncar}

plotting = {'cbar_shrink':0.35}

diag1 = {'label':'SSH ','run':run1,'row':1,'col':1}
diag2 = {'label':'SST ','run':run1,'row':1,'col':2}

diag1.update(ssh)
diag2.update(sst)

diag1.update(plotting)
diag2.update(plotting)

diags = [diag1,diag2]

movie = lez.EZmovie(diags,plotdir='./')
movie.MITgcm_movie('test_mitgcm.gif',10,360,delta_step=10)
