import psycopg2


def db_connect():

    # For main bike table
    """
    try:
        db_bike = psycopg2.connect(host="52.76.17.124", user="apps_data_read", \
                                   password="apps123", database="apps_data", port="5432")
        cur_bike = db_bike.cursor()
        print "Bike database connected"
    except:
        print "Bike database not connected"
    """
    try:
        db_user_log = psycopg2.connect(host="52.76.193.246", user="bi_team",
                                       password="bi@team", port="5432", database="apps_data")
        cur_user_log = db_user_log.cursor()
        print "User logging database connected"
    except:
        print "User logging database not connected"
        exit(10)

    try:
        db_local = psycopg2.connect(host="localhost", user="postgres",
                                    password="postgres", port="5432", database="recommended_system")
        cur_local = db_local.cursor()
        print "Local database connected"
    except:
        print "Local database not connected"
        exit(11)

    # return db_bike, cur_bike, db_user_log, cur_user_log, db_local, cur_local

    return db_user_log, cur_user_log, db_local, cur_local


def db_delete_table(cur_local, table_name):
    if_zero = "100000"  # Some large value initially
    cur_local.execute("truncate " + table_name)
    while if_zero[0][0] != 0:
        cur_local.execute("select count(*) from " + table_name)
        if_zero = cur_local.fetchall()

    print "Deleted entries from " + table_name

