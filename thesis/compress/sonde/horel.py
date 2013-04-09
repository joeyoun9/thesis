"""
read horel pcaps-cpin formatted soundings, and compress them into a single hdf5 document
"""
import numpy as np
from thesis.tools.core.pytables import *
from thesis.tools import s2t

def read(files, save):
	"""
		each file is a sounding (an ob) so, read the file, and save it at save
	"""
	# NOTE all soundings are size obs long, they must be filled in with zeros for this data format...
	# create the HDF5 document
	doc = h5(save)
	size = 450  # this hopefully exceeds the size of the arrays # CPIN Files are much shorter...
	doc.create(pres=size, temp=size, dewpt=size, rh=size, r=size, u=size, v=size, z=size, lat=1, lon=1, theta=size, thte=size,
		wspd=size, wdir=size, gamma=size, stab=size, N=size, rich=size, thtdef=size, cpin=size)
	# those last two do not have to be included...
	# Z=geopotenital height

	# now read the files!
	for f in sorted(files):
		fname = f.split('/')[-1]
		if 'smth' not in fname and 'NCAR' not in fname: continue
		print 'reading', fname
		# launch time comes from line 2 of the file, the last element
		df = open(f, 'r')
		txt = df.read(2000).split('\n')  # way more than we need
		df.close()
		latln = txt[0].split()  # keys 1,2 will be what we want
		try:
			tm = s2t(txt[1].split()[-1] + 'UTC', '%Y%m%d%H%M%Z')
		except:
			# drat.
			print txt.split('\n')[1]
			continue
		if 'cpin' in fname:
			z, p, t, td, rh, r, wb, tv, tht, thte, thtw, ws, wd, u, v, vflg, gamma, stab, N, rich, thtdef, cpin = np.loadtxt(f, skiprows=4, unpack=True)
			# r is mixing ratio
		else:
			z, p, t, td, rh, r, wb, tv, tht, thte, thtw, ws, wd, u, v, vflg, gamma, stab, N, rich = np.loadtxt(f, skiprows=4, unpack=True)
			# r is mixing ratio

		# and append this data! I will trust the time seconds, instead of recomputing the time
		# but, before that, we have to make them all the same size - size long
		nl = np.zeros(size - t.shape[0]) - 999.00  # -999 array to fluff the end
		p = np.concatenate((p, nl))
		t = np.concatenate((t, nl))
		td = np.concatenate((td, nl))
		rh = np.concatenate((rh, nl))
		r = np.concatenate((r, nl))
		tv = np.concatenate((tv, nl))
		tht = np.concatenate((tht, nl))
		thte = np.concatenate((thte, nl))
		ws = np.concatenate((ws, nl))
		wd = np.concatenate((wd, nl))
		gamma = np.concatenate((gamma, nl))
		stab = np.concatenate((stab, nl))
		N = np.concatenate((N, nl))
		rich = np.concatenate((rich, nl))
		u = np.concatenate((u, nl))
		v = np.concatenate((v, nl))
		z = np.concatenate((z, nl))
		if 'cpin' in fname:
			cpin = np.concatenate((cpin, nl))
			thtdef = np.concatenate((thtdef, nl))
			doc.append(tm, persist=True, pres=p, temp=t, dewpt=td, rh=rh, r=r, u=u, v=v, z=z, lat=[latln[1]], lon=[latln[2]],
				theta=tht, thte=thte, wspd=ws, wdir=wd, gamma=gamma, stab=stab, N=N, rich=rich, cpin=cpin, thtdef=thtdef)
		else:
			doc.append(tm, persist=True, pres=p, temp=t, dewpt=td, rh=rh, r=r, u=u, v=v, z=z, lat=[latln[1]], lon=[latln[2]],
				theta=tht, thte=thte, wspd=ws, wdir=wd, gamma=gamma, stab=stab, N=N, rich=rich)
	doc.close()
