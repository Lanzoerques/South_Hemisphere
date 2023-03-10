import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cf
import cartopy as cartopy
import numpy as np
import xarray as xr
import proplot as pplt
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.util import add_cyclic_point

def fill_meridian(dataset, variable):
    '''
    Function to complete a gridded data without the prime meridian line.
    Currently, this is one of the most upsetting problems with xarray/cartopy/etc.
    Arguments:
           dataset: a gridded dataset.
           variable: your variable string.
           Returns:
           dset: a new gridded dataset with data in the prime meridian.
    '''
    lon_idx = dataset[variable].dims.index('lon')
    dset_c, lon = add_cyclic_point(dataset[variable],
                                   coord=dataset['lon'], axis=lon_idx)
    dset = xr.Dataset(data_vars={'lat': ('lat', dataset['lat']),
                                 'lon': ('lon', lon),
                                 'time': ('time', dataset['time']),
                                 variable: (['time', 'lat', 'lon'], dset_c)
                                 })
    return dset

dsetlgm = xr.open_dataset('/content/drive/MyDrive/doc/atva_media_anual_lgm_850.nc').squeeze()
dsetpi = xr.open_dataset('/content/drive/MyDrive/doc/atva_media_anual_pi_850.nc').squeeze()
dsetlgm

lon_idxlgm = dsetlgm['vargh'].dims.index('lon')
dset_lgm, lon = add_cyclic_point(dsetlgm['vargh'], coord=dsetlgm['lon'], axis=lon_idxlgm)
lon_idxpi = dsetpi['vargh'].dims.index('lon')
dset_pi, lon = add_cyclic_point(dsetpi['vargh'], coord=dsetpi['lon'], axis=lon_idxpi)

lgm = (dsetlgm['vargh'])
pi = (dsetpi['vargh'])

fig, ax = pplt.subplots(axheight=3, nrows=2, ncols=1, tight=True, proj='spaeqd', facecolor='white', gridalpha=False, space=9)

ax.format(coast=True, borders=True)
ax.gridlines(draw_labels=True, color="black", linewidth=0.25, xlabel_style = {'size': 15}, linestyle='--', xlocs=np.arange(-180, 180, 30), ylocs=np.arange(-90, 90, 30))

map1 = ax[0].contourf(lon, dsetlgm['lat'], dset_lgm,  
                   levels = pplt.arange(0, 7500, 500), extend='max', cmap='tempo')

ax[0].set_title('LGM', fontsize=15, fontweight='bold')
ax[1].contourf(lon, dsetpi['lat'], dset_pi,
                   levels = pplt.arange(0, 7500, 500), extend='max', cmap='tempo')
ax[1].set_title('PI', fontsize=15, fontweight='bold')

fig.colorbar(map1, loc='b', label='Vari??ncia Geopotencial (m$^2$)', shrink=1, ticklabelsize=14, labelsize=18)
pplt.show()

fig.save('vargh.png', dpi=300)

dif = lgm - pi

lon_idxdif = dif.dims.index('lon')
dset_dif, diflon = add_cyclic_point(dif, coord=dif['lon'], axis=lon_idxdif)

fig, ax = pplt.subplots(axwidth=5, tight=True, proj='spaeqd', facecolor='white', gridalpha=False)

ax.format(coast=True, borders=True)
ax.gridlines(draw_labels=True, color="black", linewidth=0.25, xlabel_style = {'size': 15}, linestyle='--', xlocs=np.arange(-180, 180, 30), ylocs=np.arange(-90, 90, 30))

map1 = ax[0].contourf(diflon, dif['lat'], dset_dif, 
                   levels = pplt.arange(-300, 300, 50), extend='both', drawedges=False, cmap='negpos')
ax[0].set_title('LGM - PI', fontsize=15, fontweight='bold')

fig.colorbar(map1, loc='b', label='Vari??ncia Geopotencial (m$^2$)', shrink=1, ticklabelsize=12, labelsize=15)

pplt.show()

fig.save('varghdif.png', dpi=300)

