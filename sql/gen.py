import sqlite3

database = "ships.db"
create_queries = {
        "engines": "CREATE TABLE IF NOT EXISTS ENGINES("
                        "engine text PRIMARY KEY,"
                        "power int,"
                        "type int"
                        ")",
          "hulls": "CREATE TABLE IF NOT EXISTS HULLS("
                      "hull text PRIMARY KEY,"
                      "armor int,"
                      "type int,"
                      "capacity int"
                      ")",
          "weapons": "CREATE TABLE IF NOT EXISTS WEAPONS("
                        "weapon text PRIMARY KEY,"
                        "reload_speed int,"
                        "rotation_speed int,"
                        "diameter int,"
                        "power_volley int,"
                        "count int"
                        ")",
          "ships": "CREATE TABLE IF NOT EXISTS SHIPS("
                      "ship text PRIMARY KEY,"
                      "weapon text,"
                      "hull text,"
                      "engine text,"
                      "FOREIGN KEY (weapon) REFERENCES weapons(weapon),"
                      "FOREIGN KEY (engine) REFERENCES engines(engine),"
                      "FOREIGN KEY (hull) REFERENCES hulls(hull)"
                      ")"
          }


def create_table(model):
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute(model)
    except Exception:
        raise Exception("Try to execute %s" % model)


def insert(name, value):
    pass


if __name__ == "__main__":
    for create_query in create_queries:
        create_table(create_queries.get(create_query))
