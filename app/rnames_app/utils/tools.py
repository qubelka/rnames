import pandas as pd
import multiprocessing as mp
import time
import pandas as pd
import numpy as np

def get_cron_relations():
    url = "http://karilint.pythonanywhere.com/rnames/api/relations/?format=json"
    start = time.time()
    cron_relations = pd.read_json(url)
    #cron_relations = pd.read_csv("view_cron_relations.csv") # from file
    end = time.time()
    print("Downloaded ", len(cron_relations), "relations. Download time: ", end - start, "seconds")
    cron_relations.to_csv("cron_relations.csv", index = False, header=True)
    return (cron_relations, end - start)

def binning_outputs_equal(a, b):
    fa = pd.read_csv(a)
    fb = pd.read_csv(b)
    cols = list(fa.columns.values)

    def sort_refs(row):
        row = row.split(", ")
        row = map(int, row)
        row = sorted(row)
        row = map(str, row)
        concatenator = ', '
        return concatenator.join(row)
    fa.loc[:,'refs'] = fa['refs'].apply(sort_refs)
    fb.loc[:, 'refs'] = fb['refs'].apply(sort_refs)
    fa.sort_values(by=cols, inplace=True, ignore_index=True)
    fb.sort_values(by=cols, inplace=True, ignore_index=True)

    df = fa.merge(fb, how='outer', indicator=True)
    only2 = df[df['_merge'] == 'right_only']
    if len(only2) > 0:
        print(a)
        print(only2)

    pd.testing.assert_frame_equal(fa, fb)

class Task:
    def func(self):
        self.queue.put(self.target(**self.args))

    def __init__(self, target, args):
        self.target = target
        self.args = args
        self.queue = mp.Queue()
        self.handle = mp.Process(target=self.func)
        self.handle.start()

    def join(self):
        ret = self.queue.get()
        self.handle.join()
        return ret
