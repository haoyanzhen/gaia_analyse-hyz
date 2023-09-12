import numpy as np
import pandas as pd
import time

dty = np.uint16
def density_sky_calculation(data='a',coor='icrs',bin=1):
    # read path
    with open('/media/hyz/dwarfcave/data/gaiaDR3/ms/gaiasource_path.list','r') as _list:
        path = _list.readlines()
        if type(data) == int:
            path = path[0:data]
        elif data == 'a':
            pass
        
    # make grid
    bins = np.array([360/bin,180/bin],dtype=np.uint32)
    range = [[0,360],[-90,90]]
    edges = np.histogramdd(np.empty((1,2)),bins,range)[1]
    count = np.empty(bins)
    
    # statistics
    for _,_line in enumerate(path):
        _p = _line.strip()
        print("reading:%s ==> "%_,_p)
        _d = pd.read_csv(_p,comment='#',usecols=['ra','dec'])
        _d = _d.fillna(-1).to_numpy()
        count = np.array(np.histogramdd(_d,bins=bins,range=range)[0] + count, dtype=dty)
        if (_+1)%10 == 0:
            ti = time.time() - start
            print('time used in %02d: ===>\t\t'%(_+1),'%.02fs / %.02fh'%(ti,ti/3600))
        
    return [edges, count]

if __name__ == '__main__':
    start = time.time()
    edge, h = density_sky_calculation(data='a',bin=0.01)
    end = time.time()
    tm = end - start
    print('----------------time in main func: %.02fs / %.02fh'%(tm,tm/3600))
    np.set_printoptions(threshold=np.inf)
    save_pre = 'gaia_fullsky_density_map_0.01'
    np.save('%s.npy'%save_pre, h)
    np.save('%s.edge.npy'%save_pre, np.array(edge))
    with open('%s.txt'%save_pre,'w') as w:
        header = '# gaia star density in full sky by 0.001 deg.\n# created by hyz in 2022.12.06\n\ngrid:'
        w.write(header)
        h = h.T
        w.write(str(edge[0]))
        for _dec,dec in enumerate(h):
            w.write(str(edge[1][_dec])+'\t')
            w.write(str(dec)+'\n')

    tw = time.time() - end
    tu = time.time() - start
    print('----------------time in write: %.02fs / %.02fh'%(tw,tw/3600))
    print('----------------time overused: %.02fs / %.02fh'%(tu,tu/3600))
