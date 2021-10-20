'''
Created on Feb 27, 2019

@author: bkroger
'''
import pandas as pd
import numpy as np
from bisect import (bisect_left, bisect_right)

################################################################
# strictly searches for maximum compromise between all binnings
def bifu_c(col, ntts, xnames_raw):
    return ntts

def bifu_c2  (col, ntts, used_ts, xnames_raw):
    i_name = ntts[0, 0]

    xnames_set = xnames_raw
    var_exists = 'xnames_set' in locals()
    # if name also relates to "not specified"
    if var_exists == True:
        # filter for references with "not specified"
        bio_set = ntts[~np.isin(ntts[:, col.ntts.reference_id], xnames_set[:, col.xnames.ref])]

    if bio_set.size > 0:
        cpts = bio_set
        # select all references

        # and collect the references which have that opinions
        refs_f = ', '.join(map(str, np.unique(cpts[:, col.ntts.reference_id])))

        # youngest, oldest and ts_count
        youngest_value = np.max(cpts[:, col.ntts.youngest_index])
        oldest_value = np.min(cpts[:, col.ntts.oldest_index])
        ts_c = oldest_value - youngest_value

        youngest = np.argmax(cpts[:, col.ntts.youngest_index])
        oldest = np.argmin(cpts[:, col.ntts.oldest_index])

        return (i_name, cpts[oldest, col.ntts.oldest], cpts[youngest, col.ntts.youngest], ts_c, refs_f)

    return (None, None, None, None, None)

################################################################
# strictly searches for youngest binnings
def bifu_y(col, ntts, xnames_raw):
    max_y = max(ntts[:, col.ntts.reference_year])
    return ntts[ntts[:, col.ntts.reference_year] == max_y]

def bifu_y2  (col, ntts, used_ts, xnames_raw):
    i_name = ntts[0, 0]

    xnames_set = xnames_raw
    var_exists = 'xnames_set' in locals()
    # if name also relates to "not specified"
    if var_exists == True:
        # filter for references with "not specified"
        bio_set = ntts[~np.isin(ntts[:, col.ntts.reference_id], xnames_set[:, col.xnames.ref])]

    if bio_set.size > 0:
        # select all references
        max_y = np.max(bio_set[:, col.ntts.reference_year])
        cpts = bio_set[bisect_left(bio_set[:, col.ntts.reference_year], max_y):bisect_right(bio_set[:, col.ntts.reference_year], max_y)]

        # and collect the references which have that opinions
        refs_f = ', '.join(map(str, np.unique(cpts[:, col.ntts.reference_id])))

        # youngest, oldest and ts_count
        youngest_value = np.max(cpts[:, col.ntts.youngest_index])
        oldest_value = np.min(cpts[:, col.ntts.oldest_index])
        ts_c = oldest_value - youngest_value

        youngest = np.argmax(cpts[:, col.ntts.youngest_index])
        oldest = np.argmin(cpts[:, col.ntts.oldest_index])

        return (i_name, cpts[oldest, col.ntts.oldest], cpts[youngest, col.ntts.youngest], ts_c, refs_f)

    return (None, None, None, None, None)

################################################################
# strictly searches for shortest binnings
def bifu_s(col, ntts, xnames_raw):
    rows = []

    for ref in pd.unique(ntts[:, col.ntts.reference_id]):
        cptx = ntts[ntts[:, col.ntts.reference_id]== ref]
        ts_min = cptx[0, col.ntts.ts_index]
        ts_max = cptx[np.size(cptx, 0) - 1, col.ntts.ts_index]

        ts_x = ts_max - ts_min
        rows.append((ref, ts_x))

    rows = np.array(rows)
    min_ts = np.min(rows[:, 1])
    short_ref = rows[rows[:, 1] == min_ts]
    bio_setb = ntts[np.isin(ntts[:, col.ntts.reference_id], short_ref[:, 0])]
    # search for youngest reference among those
    max_y = np.max(bio_setb[:, col.ntts.reference_year])
    return bio_setb[bio_setb[:, col.ntts.reference_year] == max_y]

def bifu_s2(col, ntts, used_ts, xnames_raw):
    i_name = ntts[0, 0]

    xnames_set = xnames_raw
    var_exists = 'xnames_set' in locals()
    # if name also relates to "not specified"
    if var_exists == True:
        # filter for references with "not specified"
        bio_set = ntts[~np.isin(ntts[:, col.ntts.reference_id], xnames_set[:, col.xnames.ref])]

    if bio_set.size > 0:
        # select all references
        sorted_refs = bio_set[bio_set[:, col.ntts.reference_id].argsort()]
        rows = []
        min_delta = np.inf
        # search for shortest range
        for r_yx in np.unique(bio_set[:, col.ntts.reference_id]):
            cptx = sorted_refs[bisect_left(sorted_refs[:, col.ntts.reference_id], r_yx):bisect_right(sorted_refs[:, col.ntts.reference_id], r_yx)]
            ts_x = np.max(cptx[:, col.ntts.youngest_index]) - np.min(cptx[:, col.ntts.oldest_index])
            if ts_x == min_delta:
                rows.append(r_yx)
            if ts_x < min_delta:
                del rows[:]
                min_delta = ts_x
                rows.append(r_yx)

        bio_setb = bio_set[np.isin(bio_set[:, col.ntts.reference_id], rows)]
        # search for youngest reference among those
        max_y = max(bio_setb[:, col.ntts.reference_year])
        cpts = bio_setb[bisect_left(bio_setb[:, col.ntts.reference_year], max_y):bisect_right(bio_setb[:, col.ntts.reference_year], max_y)]
 
        # and collect the references which have that opinions
        refs_f = ', '.join(map(str, np.unique(cpts[:, col.ntts.reference_id])))

        # youngest, oldest and ts_count
        youngest_value = np.max(cpts[:, col.ntts.youngest_index])
        oldest_value = np.min(cpts[:, col.ntts.oldest_index])
        ts_c = oldest_value - youngest_value

        youngest = np.argmax(cpts[:, col.ntts.youngest_index])
        oldest = np.argmin(cpts[:, col.ntts.oldest_index])

        return (i_name, cpts[oldest, col.ntts.oldest], cpts[youngest, col.ntts.youngest], ts_c, refs_f)

    return (None, None, None, None, None)
