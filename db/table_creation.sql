

CREATE TABLE IF NOT EXISTS users
 (
 	id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 	steam_id TEXT NOT NULL UNIQUE,
 	steam_alias TEXT
 );

CREATE TABLE IF NOT EXISTS games
 (
 	id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 	name TEXT NOT NULL,
 	market_id TEXT NOT NULL UNIQUE
 );

CREATE TABLE IF NOT EXISTS game_badges
 (
 	id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 	game_id INT REFERENCES games NOT NULL,
 	name TEXT NOT NULL,
 	level INT NOT NULL,
 	foil BOOL NOT NULL,
 	UNIQUE (game_id, level, foil)
 );

CREATE TABLE IF NOT EXISTS pure_badges
 (
 	id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 	page_id INT NOT NULL,
 	name TEXT NOT NULL
 );

--CREATE TABLE IF NOT EXISTS user_badges
--  (
-- 	id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
-- 	steam_user_id INT REFERENCES users NOT NULL,
-- 	game_badge_id INT REFERENCES game_badges,
-- 	pure_badge_id INT REFERENCES pure_badges,
-- 	datetime_unlocked TIMESTAMP,
-- 	experience INT
--  );
