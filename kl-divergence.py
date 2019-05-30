import numpy as np

n_bins = 100

def compute_kld(raw_p, raw_q):
    density_p, bins_p = np.histogram(raw_p, bins=n_bins, normed=True, density=True)
    density_q, bins_p = np.histogram(raw_q, bins=n_bins, normed=True, density=True)
    p = density_p / density_p.sum()
    q = density_q / density_q.sum()
    print( np.sum(np.where(p != 0, p*np.log(p/q), 0)) )

instances_x = np.random.rand(1000)
instances_y = np.random.rand(1000)
compute_kld(instances_x, instances_y)
