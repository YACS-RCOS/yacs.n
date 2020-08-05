DROP TABLE IF EXISTS user_event;
DROP TABLE IF EXISTS event;

CREATE TABLE user_event
(
	event_id INTEGER,
	user_id UUID,
	content VARCHAR(255),
	created_at BIGINT
);

CREATE TABLE event
(
	event_id INTEGER NOT NULL
		CONSTRAINT events_pkey
			PRIMARY KEY,
	description VARCHAR(255)
);
