CREATE TABLE user_session
(
	session_id UUID NOT NULL
		CONSTRAINT sessions_pk
			PRIMARY KEY,
	user_id INTEGER NOT NULL,
	start_time TIMESTAMP WITH TIME ZONE,
	end_time TIMESTAMP WITH TIME ZONE
);