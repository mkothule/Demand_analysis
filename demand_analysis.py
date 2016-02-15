import numpy as np
import datetime
from operator import itemgetter


def popular_bikes(bike_ids):
    bike_ids = bike_ids.astype(int)
    hist = np.bincount(bike_ids)
    valid_index = np.array(np.nonzero(hist)).T
    pop_bikes = np.array([valid_index[:, 0], hist[valid_index[:, 0]]]).T
    pop_bikes = sorted(pop_bikes, key=itemgetter(1), reverse=True)
    return pop_bikes


def time_analysis_bikes(bike_ids):
    bike_ids_pro = np.array(sorted(bike_ids, key=itemgetter(0)))  # sorted by session ids
    remove = np.where(bike_ids_pro[:, 0] == '')  # to remove blank values of session ids from array
    bike_ids_pro = np.delete(bike_ids_pro, remove, 0)  # to remove blank values of session ids from array
    unique_sess_ids = np.unique(bike_ids_pro[:, 0])  # find unique session ids
    time_analysis = np.empty([0, 3], dtype='str, int, datetime64')  # define an empty array to save values
    idx = 0
    idx_d = 0
    for i in unique_sess_ids:
        time_1 = datetime.time()
        time_2 = datetime.timedelta()
        first_entry = True
        bike_ids_seen = []
        while bike_ids_pro[idx, 0] == i:
            if first_entry:  # 1st entry in DB... This will not be added in database
                time_1 = bike_ids_pro[idx, 2]
                first_entry = False
                idx_d = idx
            else:
                time_2 += bike_ids_pro[idx, 2] - time_1
                time_1 = bike_ids_pro[idx, 2]
                if bike_ids_pro[idx, 1] in bike_ids_seen:  # case to handle duplicate bike entries
                    for j in range(idx_d+4, len(time_analysis), 3):
                        if time_analysis[j] == bike_ids_pro[idx, 1]:
                            time_analysis[j+1] += time_2
                            break
                else:
                    time_analysis = np.append(time_analysis, np.array([bike_ids_pro[idx, 0], bike_ids_pro[idx, 1],
                                                                       time_2]))
                    bike_ids_seen.append(bike_ids_pro[idx, 1])

            idx += 1
            if idx == len(bike_ids_pro):
                break
        idx_d = len(time_analysis)  # counter is saved to start finding the duplicate baike entries
    time_analysis.resize(time_analysis.size/3, 3)
    assert(idx == len(bike_ids_pro)), "All values are not processed"
    # remove_duplicates(time_analysis)
    return time_analysis

