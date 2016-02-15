from connect_database import db_connect, db_delete_table
from demand_analysis import popular_bikes, time_analysis_bikes
from datetime import datetime
import numpy as np

TEST = False

# connect to user_logging and local database
[db_user_log, cur_user_log, db_local, cur_local] = db_connect()

if not TEST:
    # delete both the table on local everytime
    table_name = "popular_bikes"
    db_delete_table(cur_local, table_name)
    table_name = "time_analysis"
    db_delete_table(cur_local, table_name)
    print "Values in both the table are Deleted!!"

t1 = datetime.now()
# fetch data from user logging table
features_req_user = str(["session_id, bike_id, inserted_timestamp"])
cur_user_log.execute("select " + features_req_user[2:-2] + " from user_recommendation_logging.bike_page_logging")
bike_ids = np.array(cur_user_log.fetchall())
print "\n#### Fetching completed ####\n"
t2 = datetime.now()

# finding popular bikes
pop_bikes = popular_bikes(bike_ids[:, 1])
print "Computation for popular bikes done\n"
t3 = datetime.now()

if not TEST:
    # insert data in local database
    print "Inserting records for popularity. Number:", len(pop_bikes), "\n"
    cur_local.executemany("insert into popular_bikes (bike_id, bike_views) values (%s, %s)", pop_bikes)
    db_local.commit()
t4 = datetime.now()
# perform time analysis
time_analysis = time_analysis_bikes(bike_ids)
print "Computation for time analysis done\n"
t5 = datetime.now()
if not TEST:
    # insert data in local database
    print "Inserting records for time analysis. Number:", len(time_analysis), "\n"
    cur_local.executemany("insert into time_analysis (session_id, bike_id, view_time) values (%s, %s, %s)", time_analysis)
    db_local.commit()
t6 = datetime.now()

print "##### Time required ###### "
print "Total time: ", t6-t1
print "For fetching data: ", t2-t1
print "For computing popular bikes: ", t3-t2
print "For updating database: ", t4-t3
print "For time analysis: ", t5-t4
print "For updating database: ", t6-t5

