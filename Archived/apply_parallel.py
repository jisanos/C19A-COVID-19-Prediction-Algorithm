# https://gist.github.com/psinger/6e5f11981588378bc9316397131be66a
from joblib import Parallel, delayed
import multiprocessing
import pandas as pd
import time

# Multiprocessing apply
def applyParallel(dfGrouped, func):
    start_time = time.time()
    retLst = Parallel(n_jobs=multiprocessing.cpu_count())(delayed(func)(group) for name, group in dfGrouped)
    print(time.time() - start_time)
    return pd.concat(retLst)

