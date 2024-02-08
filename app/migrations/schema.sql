-- public.alembic_version definition

-- Drop table

-- DROP TABLE alembic_version;

CREATE TABLE alembic_version (
	version_num varchar(32) NOT NULL,
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- DROP TYPE "roles";

CREATE TYPE "roles" AS ENUM ('user', 'admin');

-- public.auth definition

-- Drop table

-- DROP TABLE auth;

CREATE TABLE auth (
	id serial4 NOT NULL,
	login varchar(50) NOT NULL,
	"password" varchar(128) NOT NULL,
	"role" "roles" NOT NULL,
	CONSTRAINT auth_login_key UNIQUE (login),
	CONSTRAINT auth_pkey PRIMARY KEY (id)
);


-- public."user" definition

-- Drop table

-- DROP TABLE "user";

CREATE TABLE "user" (
	id serial4 NOT NULL,
	auth_id int4 NOT NULL,
	"name" varchar(50) NOT NULL,
	icon_link text NULL,
	CONSTRAINT user_auth_id_key UNIQUE (auth_id),
	CONSTRAINT user_pkey PRIMARY KEY (id),
	CONSTRAINT user_auth_id_fkey FOREIGN KEY (auth_id) REFERENCES auth(id)
);


-- public.player definition

-- Drop table

-- DROP TABLE player;

CREATE TABLE player (
	id serial4 NOT NULL,
	user_id int4 NULL,
	remaining_moves int4 NOT NULL,
	used_moves int4 NOT NULL,
	CONSTRAINT player_pkey PRIMARY KEY (id),
	CONSTRAINT player_user_id_fkey FOREIGN KEY (user_id) REFERENCES "user"(id)
);


-- public.prize definition

-- Drop table

-- DROP TABLE prize;

CREATE TABLE prize (
	id serial4 NOT NULL,
	"name" varchar(50) NOT NULL,
	description text NULL,
	icon_link text NULL,
	admin_id int4 NOT NULL,
	dt_won timestamp NULL,
	user_id int4 NULL,
	CONSTRAINT prize_pkey PRIMARY KEY (id),
	CONSTRAINT prize_admin_id_fkey FOREIGN KEY (admin_id) REFERENCES "user"(id),
	CONSTRAINT prize_user_id_fkey FOREIGN KEY (user_id) REFERENCES "user"(id)
);


-- public.boat definition

-- Drop table

-- DROP TABLE boat;

CREATE TABLE boat (
	id serial4 NOT NULL,
	prize_id int4 NOT NULL,
	CONSTRAINT boat_pkey PRIMARY KEY (id),
	CONSTRAINT boat_prize_id_key UNIQUE (prize_id),
	CONSTRAINT boat_prize_id_fkey FOREIGN KEY (prize_id) REFERENCES prize(id)
);


-- public.game definition

-- Drop table

-- DROP TABLE game;

CREATE TABLE game (
	id serial4 NOT NULL,
	"name" varchar(50) NOT NULL,
	description text NULL,
	board_size int4 NOT NULL,
	"key" varchar(10) NOT NULL,
	admin_id int4 NOT NULL,
	dt_start timestamp NULL,
	player1_id int4 NULL,
	player2_id int4 NULL,
	CONSTRAINT game_key_key UNIQUE (key),
	CONSTRAINT game_pkey PRIMARY KEY (id),
	CONSTRAINT game_admin_id_fkey FOREIGN KEY (admin_id) REFERENCES "user"(id),
	CONSTRAINT game_player1_id_fkey FOREIGN KEY (player1_id) REFERENCES player(id),
	CONSTRAINT game_player2_id_fkey FOREIGN KEY (player2_id) REFERENCES player(id)
);


-- public.field definition

-- Drop table

-- DROP TABLE field;

CREATE TABLE field (
	id serial4 NOT NULL,
	game_id int4 NOT NULL,
	x int4 NOT NULL,
	y int4 NOT NULL,
	injured bool NOT NULL,
	boat_id int4 NULL,
	player_id int4 NULL,
	CONSTRAINT field_boat_id_key UNIQUE (boat_id),
	CONSTRAINT field_pkey PRIMARY KEY (id),
	CONSTRAINT unique_field UNIQUE (game_id, x, y),
	CONSTRAINT field_boat_id_fkey FOREIGN KEY (boat_id) REFERENCES boat(id),
	CONSTRAINT field_game_id_fkey FOREIGN KEY (game_id) REFERENCES game(id),
	CONSTRAINT field_player_id_fkey FOREIGN KEY (player_id) REFERENCES player(id)
);

