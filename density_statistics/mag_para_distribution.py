import numpy as np
import pandas as pd
import time

dty = np.uint32
def mag_para_distribution(data='a',coor='icrs',bin_mag=0.1,bin_r=0.1):
    # read path
    with open('/media/hyz/dwarfcave/data/gaiaDR3/ms/gaiasource_path.list','r') as _list:
        path = _list.readlines()
        if type(data) == int:
            path = path[0:data]
        elif data == 'a':
            pass
        
    # make grid
    range = [[2,25],[0,300]]
    bins = np.array([23/bin_mag,300/bin_r],dtype=np.uint32)
    edges = np.histogramdd(np.empty((1,2)),bins,range)[1]
    count = np.empty(bins)
    
    # statistics
    for _,_line in enumerate(path):
        _p = _line.strip()
        print("reading:%s ==> "%_,_p)
        _d = pd.read_csv(_p,comment='#',usecols=['phot_g_mean_mag','parallax'])
        _d = _d.dropna().to_numpy()
        count = np.array(np.histogramdd(_d,bins=bins,range=range)[0] + count, dtype=dty)
        if (_+1)%10 == 0:
            ti = time.time() - start
            print('time used in %02d: ===>\t\t'%(_+1),'%.02fs / %.02fh'%(ti,ti/3600))
        
    return [edges, count]

if __name__ == '__main__':
    start = time.time()
    edge, h = mag_para_distribution(data='a')
    end = time.time()
    tm = end - start
    print('----------------time in main func: %.02fs / %.02fh'%(tm,tm/3600))
    np.set_printoptions(threshold=np.inf)
    save_pre = 'gaia_mag_parallax_distribution_0.1_0.1'
    np.save('%s.npy'%save_pre, h)
    np.save('%s.edge.npy'%save_pre, np.array(edge))
    with open('%s.txt'%save_pre,'w') as w:
        header = '# gaia aparent magnitude and parallax distribution in 0.1 deg and 0.1 mas.\n# created by hyz in 2022.12.08\n\ngrid:'
        w.write(header)
        w.write(str(edge[0])+'\n')
        w.write(str(edge[1])+'\n')
        for _m,p in enumerate(h):
            w.write(str(p)+'\t')

    tw = time.time() - end
    tu = time.time() - start
    print('----------------time in write: %.02fs / %.02fh'%(tw,tw/3600))
    print('----------------time overused: %.02fs / %.02fh'%(tu,tu/3600))
