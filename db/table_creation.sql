

CREATE TABLE IF NOT EXISTS users
 (
 	id SERIAL PRIMARY KEY,
 	steam_id TEXT NOT NULL,
 	steam_alias TEXT
 );

CREATE TABLE IF NOT EXISTS games
 (
 	id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 	name TEXT NOT NULL,
 	market_id TEXT UNIQUE
 );

--CREATE TABLE IF NOT EXISTS public.badges
-- (
-- );

--CREATE TABLE IF NOT EXISTS users_badges
--  (
--  );
