SET CLIENT_MIN_MESSAGES = WARNING;

CREATE TABLE password_reset (
    verification_id  TEXT                       PRIMARY KEY,
    user_id          TEXT                       NOT NULL,
    reset            TIMESTAMP WITH TIME ZONE   DEFAULT NULL
);
--=mpj17=-- There is no foreign key for user_id... yet

