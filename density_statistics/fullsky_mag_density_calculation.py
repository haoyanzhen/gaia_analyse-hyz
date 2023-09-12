import numpy as np
import pandas as pd
import time

dty = np.uint16
def float2index(d,bin,min=0):
    # d = d.fillna(99)  # fill nan in mag with value 99.
    return dty((d-min)/bin)

def density_sky_mag_calculation(data='a',mode='m',coor='icrs',bin_sky=1,m_min=2, m_max=25, bin_mag=0.01):
    '''
    data='a' or number of files
    mode='g','r','b','m','a'
    '''
    # read path
    with open('/media/hyz/dwarfcave/data/gaiaDR3/ms/gaiasource_path.list','r') as _list:
        path = _list.readlines()
        if type(data) == int:
            path = path[0:data]
        elif data == 'a':
            pass
    
    bins  = np.array([360/bin_sky,180/bin_sky,(m_max-m_min)/bin_mag],dtype=np.uint16)
    range = ([0,360],[-90,90],[m_min,m_max])
    count_g,count_r,count_b,count_m = np.empty(bins),np.empty(bins),np.empty(bins),np.empty(bins)
    edges = np.histogramdd(np.empty((1,3)),bins,range)[1]
    
    # statistics
    for _,_line in enumerate(path):
        _p = _line.strip()
        print("reading:%s ==> "%_,_p)
        _d    = pd.read_csv(_p,comment='#',usecols=['ra','dec','phot_g_mean_mag','phot_rp_mean_mag','phot_bp_mean_mag'])
        _d['phot_all_mean_mag'] = _d[['phot_g_mean_mag','phot_rp_mean_mag','phot_bp_mean_mag']].mean(axis=1)  # calculate mean of 3 band. obtain all objects
        _d = _d.fillna(m_min).to_numpy()
        if mode == 'a':
            count_g = np.array(np.histogramdd(_d[:,[0,1,2]], bins=bins, range=range)[0] + count_g, dtype=dty)
            count_r = np.array(np.histogramdd(_d[:,[0,1,3]], bins=bins, range=range)[0] + count_r, dtype=dty)
            count_b = np.array(np.histogramdd(_d[:,[0,1,4]], bins=bins, range=range)[0] + count_b, dtype=dty)
            count_m = np.array(np.histogramdd(_d[:,[0,1,5]], bins=bins, range=range)[0] + count_m, dtype=dty)
        if mode == 'm':
            if _ == 0:
                del count_g,count_r,count_b
            count_m = np.array(np.histogramdd(_d[:,[0,1,5]], bins=bins, range=range)[0] + count_m, dtype=dty)
        if (_+1)%10 == 0:
            ti = time.time() - start
            print('used time in:  %s =====>\t\t\t%.02fs / %.02fh\n'%(_+1,ti,ti/3600)+'-'*30)
    if mode == 'a':
        count_g[:,:,0] = 0
        count_r[:,:,0] = 0
        count_b[:,:,0] = 0
        count_m[:,:,0] = 0
        count = np.array([count_g,count_r,count_b,count_m],dtype=dty)
    if mode == 'm':
        count_m[:,:,0] = 0
        count = count_m
    
    # coordinate alternation
    if coor == 'icrs':
        return [edges, count]
    # elif coor == 'gal':
    #     grid_ra = np.arange(0,360,bin)
    #     grid_dec = np.arange(-90,90,bin)
    #     grid_icrs = SkyCoord(grid_ra,grid_dec,frame='icrs',unit='deg')
    #     grid_gal = grid_icrs.galactic
    #     count = grid_gal.to_string('decimal')
    #     return [edges, count]
    else:
        print('coordination assign is out of index, please choose "icrs" or "gal".')
        
if __name__ == '__main__':
    start = time.time()
    edge, h = density_sky_mag_calculation(data='a',mode='a',bin_sky=0.2,bin_mag=0.1,m_min=10,m_max=21)
    end = time.time()
    tm = end - start
    print('----------------time in main func: %.02fs / %.02fh'%(tm,tm/3600))
    np.set_printoptions(threshold=np.inf)
    save_pre = 'gaia_fullsky_mag_density_allband_skyclear_02_01_10-20.5'
    np.save('%s.npy'%save_pre, h)
    np.save('%s.edge.npy'%save_pre, np.array(edge))
    with open('%s.txt'%save_pre,'w') as w:
        header = '# gaia star density with sky and mag.sky by 1 and mag by 0.01.[all band]\n# created by hyz in 2022.12.2\n\ngrid:'
        w.write(header)
        for i in edge:
            w.write('  ('+str(i.max())+', '+str(i.min())+'), '+str(i[:].size))
        w.write('\n')
        for _,_h in enumerate(h):
            for _i,i in enumerate(_h):
                for _j,j in enumerate(i):
                    if _ == 0:
                        w.write('band: -----> g'.ljust(15))
                    elif _ == 1:
                        w.write('band: -----> r'.ljust(15))
                    elif _ == 2:
                        w.write('band: -----> b'.ljust(15))
                    elif _ == 3:
                        w.write('band: -----> m'.ljust(15))
                    w.write('icrs: ------> '+str(edge[0][_i])+', '+str(edge[1][_j])+'\n')
                    w.write(str(j)+'\n')

    tw = time.time() - end
    tu = time.time() - start
    print('----------------time in write: %.02fs / %.02fh'%(tw,tw/3600))
    print('----------------time overused: %.02fs / %.02fh'%(tu,tu/3600))
    
    
#TODO: make changes:
# line10, m_min  -> 2
# line34, fillna -> m_min
# line48-... turn first lines of mag to 0
# line85, write rule
# line74,75,99,101, time show
