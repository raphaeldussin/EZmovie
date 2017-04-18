import matplotlib.pylab as plt
import matplotlib.cm as cm
import matplotlib.colors as mc
from mpl_toolkits.basemap import Basemap
import numpy as np

def setup_contour(vmin,vmax,ncontours):
        ''' set the contours and norm '''
        plotcmin = float(vmin)
        plotcmax = float(vmax)
        stepticks = (plotcmax - plotcmin) / 10.
        ticks  = np.arange(plotcmin,plotcmax+stepticks,stepticks)
        step = (plotcmax - plotcmin) / ncontours
        contours = np.arange(plotcmin,plotcmax+step,step)
        norm = mc.Normalize(vmin=plotcmin, vmax=plotcmax)
        return contours, norm, ticks

def setup_colorbar_fmt(data):
        ''' setup the format for colorbar '''
        if data.max() < 0.1:
                cbarfmt = '%.1e'
        elif data.max() > 10.:
                cbarfmt = '%.0f'
        else:
                cbarfmt = '%.2f'
        return cbarfmt

def plot_map(ax,diag,coord1,coord2,data,current_date):
	''' single plot '''
	contours, norm, ticks = setup_contour(diag['vmin'],diag['vmax'],40)
	cbarfmt = setup_colorbar_fmt(data)

	# background
        if diag['run']['grid'] == 'CCS1':
                bmap = Basemap(projection='cyl',llcrnrlat=18,urcrnrlat=51,\
                                                llcrnrlon=219,urcrnrlon=251,resolution='l')
                parallels = np.arange(20.,60.,10.)
                bmap.drawparallels(parallels,labels=[True,False,False,True])
                meridians = np.arange(220.,260.,10.)
                bmap.drawmeridians(meridians,labels=[True,False,False,True])
        elif diag['run']['grid'] == 'NWA':
                bmap = Basemap(projection='cyl',llcrnrlat=5,urcrnrlat=55, llcrnrlon=250, \
                                                urcrnrlon=320,resolution='l')
                parallels = np.arange(0.,70.,10.)
                bmap.drawparallels(parallels,labels=[1,0,0,0],fontsize=10)
                meridians = np.arange(240.,340.,10.)
                bmap.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10)
        else:
                pass
        bmap.drawcoastlines()
        bmap.fillcontinents(color='grey',lake_color='white')

        C = ax.contourf(coord1,coord2,data,contours,cmap=diag['pal'],norm=norm,extend='both')
        cbar = plt.colorbar(C,format=cbarfmt,shrink=0.8,ticks=ticks)
	fmt = "%Y %m %d"
        plt.title(diag['label'] + ' ' + current_date.strftime(fmt))

	return ax
