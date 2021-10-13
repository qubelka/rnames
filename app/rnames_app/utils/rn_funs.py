'''
Created on Feb 27, 2019

@author: bkroger
'''
import pandas as pd
import numpy as np
from bisect import (bisect_left, bisect_right)
csv_folder = 'rnames_app/utils/csv/'

rassm_ts = pd.read_csv(csv_folder+"binning_rass.csv", header=None)
cnr = np.arange(0,len(rassm_ts),1)
rassm_ts = pd.DataFrame(rassm_ts, index=cnr)
rassm_ts.columns = ["ts"]
rassm_ts['ts_index'] = rassm_ts.index
rassm_ts = rassm_ts.append({'ts' : 'not specified' , 'ts_index' : len(rassm_ts)} , ignore_index=True)

berg_ts = pd.read_csv(csv_folder+"binning_bergst.csv", header=None)
cnr = np.arange(0,len(berg_ts),1)
berg_ts = pd.DataFrame(berg_ts, index=cnr)
berg_ts.columns = ["ts"]
berg_ts['ts_index'] = berg_ts.index
berg_ts = berg_ts.append({'ts' : 'not specified' , 'index_1' : len(berg_ts)} , ignore_index=True)


webby_ts = pd.read_csv(csv_folder+"binning_webby.csv", header=None)
cnr = np.arange(0,len(webby_ts),1)
webby_ts = pd.DataFrame(webby_ts, index=cnr)
webby_ts.columns = ["ts"]
webby_ts['ts_index'] = webby_ts.index
webby_ts = webby_ts.append({'ts' : 'not specified' , 'ts_index' : len(webby_ts)} , ignore_index=True)


stages_ts = pd.read_csv(csv_folder+"binning_stages.csv", header=None)
cnr = np.arange(0,len(stages_ts),1)
stages_ts = pd.DataFrame(stages_ts, index=cnr)
stages_ts.columns = ["ts"]
stages_ts['ts_index'] = stages_ts.index
stages_ts = stages_ts.append({'ts' : 'not specified' , 'ts_index' : len(stages_ts)} , ignore_index=True)

periods_ts = pd.read_csv(csv_folder+"binning_periods.csv", header=None)
cnr = np.arange(0,len(periods_ts),1)
periods_ts = pd.DataFrame(periods_ts, index=cnr)
periods_ts.columns = ["ts"]
periods_ts['ts_index'] = periods_ts.index
periods_ts = periods_ts.append({'ts' : 'not specified' , 'ts_index' : len(periods_ts)} , ignore_index=True)


epochs_ts = pd.read_csv(csv_folder+"binning_epoch.csv", header=None)
cnr = np.arange(0,len(epochs_ts),1)
epochs_ts = pd.DataFrame(epochs_ts, index=cnr)
epochs_ts.columns = ["ts"]
epochs_ts['ts_index'] = epochs_ts.index
epochs_ts = epochs_ts.append({'ts' : 'not specified' , 'ts_index' : len(epochs_ts)} , ignore_index=True)


eras_ts = pd.read_csv(csv_folder+"binning_era.csv", header=None)
cnr = np.arange(0,len(eras_ts),1)
eras_ts = pd.DataFrame(eras_ts, index=cnr)
eras_ts.columns = ["ts"]
eras_ts['ts_index'] = eras_ts.index
eras_ts = eras_ts.append({'ts' : 'not specified' , 'ts_index' : len(eras_ts)} , ignore_index=True)

eons_ts = pd.read_csv(csv_folder+"binning_eon.csv", header=None)
cnr = np.arange(0,len(eons_ts),1)
eons_ts = pd.DataFrame(eons_ts, index=cnr)
eons_ts.columns = ["ts"]
eons_ts['ts_index'] = eons_ts.index
eons_ts = eons_ts.append({'ts' : 'not specified' , 'ts_index' : len(eons_ts)} , ignore_index=True)

################################################################
# strictly searches for maximum compromise between all binnings
def bifu_c  (ntts, used_ts, xnames_raw):
    ele = ntts["name_1"]
    ele = ele.drop_duplicates()
    ele = pd.DataFrame(ele)
    i_name = ele.iloc[0,0]
    xnames_set = xnames_raw.loc[xnames_raw["name"]== i_name]
    var_exists = 'xnames_set' in locals()
    # if name also relates to "not specified"
    if var_exists == True:
        bio_sel =pd.DataFrame([] * 5, index=["name", "oldest", "youngest", "ts_count", "refs"])
        bio_set = ntts.loc[ntts["name_1"]== i_name,
                       ["reference_id","name_1","name_2", "ts", "ts_index"]]
        # filter for references with "not specified"
        bio_set = bio_set[~bio_set["reference_id"].isin(xnames_set["ref"])]
    isempty = bio_set.empty
    if isempty == False:
        cpts = bio_set
        # select all references
        u_ref = cpts["reference_id"]
        u_ref = u_ref.drop_duplicates()
        refs_f = pd.unique(cpts['reference_id'])
        refs_f = pd.DataFrame(refs_f)
        refs_f = refs_f[0].apply(str)
        refs_f = refs_f.str.cat(sep=', ')# and collect the references which have that opinions
        # youngest, oldest and ts_count
        cpts_youngest =  cpts.loc[(cpts["ts_index"]== max(cpts["ts_index"])), ['ts']]
        cpts_oldest = cpts.loc[(cpts["ts_index"]== min(cpts["ts_index"])), ['ts']]
        ts_c = max(cpts["ts_index"])-min(cpts["ts_index"])
        bio_sel = pd.DataFrame([[i_name, cpts_oldest.iloc[0,0], cpts_youngest.iloc[0,0], ts_c, refs_f]],
                               columns=["name", "oldest", "youngest", "ts_count", "refs"])
    return(bio_sel)

def bifu_c2  (ntts, used_ts, xnames_raw):
    ele = ntts["name_1"]
    ele = ele.drop_duplicates()
    ele = pd.DataFrame(ele)
    i_name = ele.iloc[0,0]
    xnames_set = xnames_raw
    var_exists = 'xnames_set' in locals()
    # if name also relates to "not specified"
    if var_exists == True:
        # filter for references with "not specified"
        bio_set = ntts.loc[~ntts["reference_id"].isin(xnames_set["ref"]),
                       ['name_1', 'name_2', 'oldest', "oldest_index", 'youngest', 'youngest_index', 'ts_count',
                        'refs', 'rule', 'reference_id', "reference_year"]]
    isempty = bio_set.empty
    if isempty == False:
        cpts = bio_set
        # select all references
        u_ref = cpts["reference_id"]
        u_ref = u_ref.drop_duplicates()

        # and collect the references which have that opinions
        refs_f = ', '.join(cpts['reference_id'].apply(str).unique())

        # youngest, oldest and ts_count
        youngest_idx = cpts["youngest_index"].idxmax()
        oldest_idx = cpts["oldest_index"].idxmin()
        ts_c = max(cpts["youngest_index"])-min(cpts["oldest_index"])
        return (i_name, cpts.at[oldest_idx, 'oldest'], cpts.at[youngest_idx, 'youngest'], ts_c, refs_f)

    return (None, None, None, None, None)

################################################################
# strictly searches for youngest binnings
def bifu_y  (ntts, used_ts, xnames_raw):
    ele = ntts["name_1"]
    ele = ele.drop_duplicates()
    ele = pd.DataFrame(ele)
    i_name = ele.iloc[0,0]
    xnames_set = xnames_raw.loc[xnames_raw["name"]== i_name]
    var_exists = 'xnames_set' in locals()
    # if name also relates to "not specified"
    if var_exists == True:
        bio_sel =pd.DataFrame([] * 5, index=["name", "oldest", "youngest", "ts_count", "refs"])
        bio_set = ntts.loc[ntts["name_1"]== i_name,
                       ["reference_id","name_1","name_2", "ts", "ts_index", "reference_year"]]
        # filter for references with "not specified"
        bio_set = bio_set[~bio_set["reference_id"].isin(xnames_set["ref"])]
    isempty = bio_set.empty
    if isempty == False:
        # select all references
        u_ref = bio_set["reference_id"]
        u_ref = u_ref.drop_duplicates()
        max_y = max(bio_set["reference_year"])
        cpts = bio_set.loc[bio_set["reference_year"]==max_y,
                        ["reference_id","name_1","name_2", "ts", "ts_index"]]
        refs_f = pd.unique(cpts['reference_id'])
        refs_f = pd.DataFrame(refs_f)
        refs_f = refs_f[0].apply(str)
        refs_f = refs_f.str.cat(sep=', ')# and collect the references which have that opinions
        # youngest, oldest and ts_count
        cpts_youngest =  cpts.loc[(cpts["ts_index"]== max(cpts["ts_index"])), ['ts']]
        cpts_oldest = cpts.loc[(cpts["ts_index"]== min(cpts["ts_index"])), ['ts']]
        ts_c = max(cpts["ts_index"])-min(cpts["ts_index"])
        bio_sel = pd.DataFrame([[i_name, cpts_oldest.iloc[0,0], cpts_youngest.iloc[0,0], ts_c, refs_f]],
                               columns=["name", "oldest", "youngest", "ts_count", "refs"])
    return(bio_sel)

def bifu_y2  (ntts, used_ts, xnames_raw):
    ele = ntts["name_1"]
    ele = ele.drop_duplicates()
    ele = pd.DataFrame(ele)
    i_name = ele.iloc[0,0]
    xnames_set = xnames_raw
    var_exists = 'xnames_set' in locals()
    # if name also relates to "not specified"
    if var_exists == True:
        # filter for references with "not specified"
        bio_set = ntts.loc[~ntts["reference_id"].isin(xnames_set["ref"]),
                       ['name_1', 'name_2', 'oldest', "oldest_index", 'youngest', 'youngest_index', 'ts_count',
                        'refs', 'rule', 'reference_id', "reference_year"]]
    isempty = bio_set.empty
    if isempty == False:
        # select all references
        u_ref = bio_set["reference_id"]
        u_ref = u_ref.drop_duplicates()
        max_y = max(bio_set["reference_year"])
        cpts = bio_set.loc[bio_set["reference_year"]==max_y,
                        ['name_1', 'name_2', 'oldest', "oldest_index", 'youngest', 'youngest_index', 'ts_count',
                        'refs', 'rule', 'reference_id', "reference_year"]]

        # and collect the references which have that opinions
        refs_f = ', '.join(cpts['reference_id'].apply(str).unique())

       # youngest, oldest and ts_count
        youngest_idx = cpts["youngest_index"].idxmax()
        oldest_idx = cpts["oldest_index"].idxmin()
        ts_c = max(cpts["youngest_index"])-min(cpts["oldest_index"])
        return (i_name, cpts.at[oldest_idx, 'oldest'], cpts.at[youngest_idx, 'youngest'], ts_c, refs_f)
    return (None, None, None, None, None)

################################################################
# strictly searches for shortest binnings
def bifu_s  (ntts, used_ts, xnames_raw):
    ele = ntts["name_1"]
    ele = ele.drop_duplicates()
    ele = pd.DataFrame(ele)
    i_name = ele.iloc[0,0]
    xnames_set = xnames_raw.loc[xnames_raw["name"]== i_name]
    var_exists = 'xnames_set' in locals()
    # if name also relates to "not specified"
    if var_exists == True:
        bio_sel = pd.DataFrame([] * 5, index=["name", "oldest", "youngest", "ts_count", "refs"])
        bio_set = ntts.loc[ntts["name_1"]== i_name,
                       ["reference_id","name_1","name_2", "ts", "ts_index", "reference_year"]]
        # filter for references with "not specified"
        bio_set = bio_set[~bio_set["reference_id"].isin(xnames_set["ref"])]
    isempty = bio_set.empty
    if isempty == False:
        # select all references
        u_ref = bio_set.loc[:, ["reference_id"]]
        u_ref = u_ref.drop_duplicates()
        cp_coll = pd.DataFrame([], columns=["reference_id","tsx"])
        # search for shortest range
        for kk in np.arange(0,len(u_ref),1):
            r_yx = u_ref["reference_id"].iloc[kk]
            cptx = bio_set.loc[bio_set["reference_id"]== r_yx,
                        ["reference_id","name_1","name_2", "ts", "ts_index"]]
            cptx_youngest =  cptx.loc[(cptx["ts_index"]== max(cptx["ts_index"])), ['ts']]
            cptx_oldest = cptx.loc[(cptx["ts_index"]== min(cptx["ts_index"])), ['ts']]
            ts_x = max(cptx["ts_index"])-min(cptx["ts_index"])
            cp_colla = pd.DataFrame([], index=["reference_id","tsx"])
            cp_colla['reference_id'] = r_yx
            cp_colla['tsx'] = ts_x
            cp_coll = np.concatenate((cp_coll, cp_colla), axis=0)
            cp_coll = pd.DataFrame(data=cp_coll, columns=['reference_id', 'tsx'])
        min_ts = min(cp_coll["tsx"])
        short_ref = cp_coll.loc[(cp_coll["tsx"]== min_ts), ['reference_id']]
        bio_setb = bio_set[bio_set["reference_id"].isin(short_ref["reference_id"])]
        # search for youngest reference among those
        u_ref = bio_setb["reference_id"]
        u_ref = u_ref.drop_duplicates()
        max_y = max(bio_setb["reference_year"])
        cpts = bio_setb.loc[bio_setb["reference_year"]==max_y,
                        ["reference_id","name_1","name_2", "ts", "ts_index"]]
        refs_f = pd.unique(cpts['reference_id'])
        refs_f = pd.DataFrame(refs_f)
        refs_f = refs_f[0].apply(str)
        refs_f = refs_f.str.cat(sep=', ')# and collect the references which have that opinions
        # youngest, oldest and ts_count
        u_ts = pd.unique(cpts["ts"])
        cpts_youngest =  cpts.loc[(cpts["ts_index"]== max(cpts["ts_index"])), ['ts']]
        cpts_oldest = cpts.loc[(cpts["ts_index"]== min(cpts["ts_index"])), ['ts']]
        ts_c = max(cpts["ts_index"])-min(cpts["ts_index"])
        bio_sel = pd.DataFrame([[i_name, cpts_oldest.iloc[0,0], cpts_youngest.iloc[0,0], ts_c, refs_f]],
                               columns=["name", "oldest", "youngest", "ts_count", "refs"])
    return(bio_sel)

def bifu_s2  (ntts, used_ts, xnames_raw):
    i_name = ntts.iloc[0].at["name_1"]

    xnames_set = xnames_raw
    var_exists = 'xnames_set' in locals()
    # if name also relates to "not specified"
    if var_exists == True:
        # filter for references with "not specified"
        bio_set = ntts.loc[~ntts["reference_id"].isin(xnames_set["ref"]),
                       ['oldest', "oldest_index", 'youngest', 'youngest_index', 'reference_id', "reference_year"]]
    isempty = bio_set.empty
    if isempty == False:
        # select all references
        bio_set = bio_set.sort_values(by='reference_id')
        rid_list = list(bio_set['reference_id'])
        rows = []
        min_delta = np.inf
        # search for shortest range
        for r_yx in bio_set["reference_id"].unique():
            cptx = bio_set.iloc[bisect_left(rid_list, r_yx):bisect_right(rid_list, r_yx)]
            ts_x = cptx["youngest_index"].max()-cptx["oldest_index"].min()
            if ts_x == min_delta:
                rows.append(r_yx)
            if ts_x < min_delta:
                del rows[:]
                min_delta = ts_x
                rows.append(r_yx)

        short_ref = set(rows)
        bio_setb = bio_set[bio_set["reference_id"].isin(short_ref)]
        # search for youngest reference among those
        max_y = max(bio_setb["reference_year"])
        cpts = bio_setb.loc[bio_setb["reference_year"]==max_y,
                        ['name_1', 'name_2', 'oldest', "oldest_index", 'youngest', 'youngest_index', 'ts_count',
                        'refs', 'rule', 'reference_id', "reference_year"]]
 
        # and collect the references which have that opinions
        refs_f = ', '.join(cpts['reference_id'].apply(str).unique())

        # youngest, oldest and ts_count
        ts_c = max(cpts["youngest_index"])-min(cpts["oldest_index"])
        youngest_idx = cpts["youngest_index"].idxmax()
        oldest_idx = cpts["oldest_index"].idxmin()

        return (i_name, cpts.at[oldest_idx, 'oldest'], cpts.at[youngest_idx, 'youngest'], ts_c, refs_f)

    return (None, None, None, None, None)
