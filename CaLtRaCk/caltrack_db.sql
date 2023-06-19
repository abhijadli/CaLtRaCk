sqlite3 caltrack.db

CREATE TABLE users(
   id INTEGER PRIMARY KEY,
   name TEXT NOT NULL,
   username TEXT NOT NULL UNIQUE,
   hash TEXT NOT NULL
);

CREATE TABLE user_profile(
   user_id INTEGER NOT NULL UNIQUE,
   gender TEXT NOT NULL,
   age INTEGER NOT NULL,
   weight REAL NOT NULL,
   height REAL NOT NULL,
   activity TEXT NOT NULL,
   goal TEXT NOT NULL,
   BMR REAL NOT NULL,
   cal REAL NOT NULL,
   FOREIGN KEY (user_id)
      REFERENCES users (id)
         ON DELETE CASCADE
         ON UPDATE NO ACTION
);

CREATE TABLE workout_logs(
user_id INTEGER NOT NULL,
log_id INTEGER NOT NULL,
logs TEXT NOT NULL,
logged_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
PRIMARY KEY (user_id, log_id)
FOREIGN KEY (user_id)
      REFERENCES users (id)
         ON DELETE CASCADE
         ON UPDATE NO ACTION
);

CREATE TABLE cal_logs(
user_id INTEGER NOT NULL,
log_id INTEGER NOT NULL,
date TEXT NOT NULL,
food TEXT NOT NULL,
calories REAL NOT NULL,
logged_time NUMERIC NOT NULL,
PRIMARY KEY (user_id, log_id)
FOREIGN KEY (user_id)
      REFERENCES users (id)
         ON DELETE CASCADE
         ON UPDATE NO ACTION
);