DROP TABLE IF EXISTS user_account CASCADE; 
CREATE TABLE user_account
(
	user_id SERIAL NOT NULL
		CONSTRAINT users_pk
			PRIMARY KEY,
	name TEXT,
	email TEXT NOT NULL UNIQUE,
	phone TEXT,
	password TEXT,
	major TEXT,
	degree TEXT,
	enable BOOLEAN DEFAULT TRUE,
  	admin BOOLEAN DEFAULT FALSE,
	super_admin BOOLEAN DEFAULT FALSE
);

