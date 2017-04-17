import numpy as np
import datetime as dt
import matplotlib.pylab as plt
import pyroms
import netCDF4 as nc
import ezmovie_plots as ezp
import os

class EZmovie():

	def __init__(self,diags,plotdir='./anim/'):
		self.diags = diags
		self.plotdir = plotdir
		self.ncol=0
		self.nrow=0
		return

	def __call__(self,fileout,start_date,end_date,means='no',step=5):

		if (means == 'no'):
			total_days = (end_date -start_date).days
			add_days = np.arange(0,total_days+step,step)
			list_dates = [start_date + dt.timedelta(n) for n in add_days]
		elif (means == 'monthly'):
			# do something else
			pass
		elif (means == 'annual'):
			# do something else
			pass
		else:
			pass

		for current_date in list_dates:
			print current_date.isoformat()
			self.write_one_frame(current_date)

		self.make_animated_gif(fileout)
		return

	def write_one_frame(self,current_date):
		''' write one frame of plots '''
		# find number of subplots
		for diag in self.diags:
			self.ncol = max(self.ncol,diag['col'])
			self.nrow = max(self.nrow,diag['row'])

		
		plt.figure(figsize=[8*self.ncol,8*self.nrow])

		for diag in self.diags:
			this_subplot = diag['col'] + (diag['row'] - 1) * self.ncol
			ax = plt.subplot(self.nrow,self.ncol,this_subplot)
			coord1, coord2, data = self.read_data(diag,current_date)
			ezp.plot_map(ax,diag,coord1,coord2,data,current_date)

		gifname = self.plotdir + 'frame_' + current_date.isoformat() + '.gif'
		pngname = self.plotdir + 'frame_' + current_date.isoformat() + '.png'
		plt.savefig(pngname,bbox_inches='tight')
		os.system(' convert ' + pngname + ' ' + gifname)
		os.system(' rm ' + pngname )
		return None

	def make_animated_gif(self,fileout):
		os.system(' rm  ' + self.plotdir + fileout)
		os.system(' gifsicle -d 20 -l ' + self.plotdir + '*.gif -o ' + self.plotdir + fileout)
		os.system(' rm ' + self.plotdir + 'frame*gif')
		return None

	def read_data(self,diag,current_date):
		''' read the data for each diag '''

		ncfile = diag['run']['directory'] + str(current_date.year) + '/' + diag['run']['name'] + '_' + diag['filetype'] + '_' + current_date.isoformat() + '.nc'
		print 'reading file ', ncfile

		if diag['type'] == 'map':
			if diag['level'] is not None and diag['depth'] is not None:
				exit('you can choose a level or a depth')
			if diag['level'] is not None:
				tmp = self.readnc(ncfile,diag['variable'])
				if len(tmp.shape) == 2:
					data = tmp
				elif len(tmp.shape) == 3:
					data = tmp[diag['level'],:]

				grd = pyroms.grid.get_ROMS_grid(diag['run']['grid'])
				coord1 = grd.hgrid.lon_rho
				coord2 = grd.hgrid.lat_rho
			if diag['depth'] is not None:
				# call pyroms zslice
				pass
		elif diag['type'] == 'section':
			# pyroms islice, jslice
			pass


		return coord1, coord2, data

	def readnc(self,myfile,myvar,myframe=None):
                ''' read data from netcdf '''
                fid = nc.Dataset(myfile,'r')
                if myframe is None:
                        out = fid.variables[myvar][:].squeeze()
                else:
                        out = fid.variables[myvar][myframe,:].squeeze()
                fid.close()
                return out
