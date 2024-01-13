-- public.alembic_version definition

-- Drop table

-- DROP TABLE public.alembic_version;

CREATE TABLE public.alembic_version (
	version_num varchar(32) NOT NULL,
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);


-- public."user" definition

-- Drop table

-- DROP TABLE public."user";

CREATE TABLE public."user" (
	id serial4 NOT NULL,
	auth_id int4 NOT NULL,
	"name" varchar(50) NOT NULL,
	icon_link text NULL,
	CONSTRAINT user_auth_id_key UNIQUE (auth_id),
	CONSTRAINT user_pkey PRIMARY KEY (id)
);


-- public.player definition

-- Drop table

-- DROP TABLE public.player;

CREATE TABLE public.player (
	id serial4 NOT NULL,
	user_id int4 NULL,
	remaining_moves int4 NOT NULL,
	used_moves int4 NOT NULL,
	CONSTRAINT player_pkey PRIMARY KEY (id),
	CONSTRAINT player_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id)
);


-- public.prize definition

-- Drop table

-- DROP TABLE public.prize;

CREATE TABLE public.prize (
	id serial4 NOT NULL,
	"name" varchar(50) NOT NULL,
	description text NULL,
	icon_link text NULL,
	admin_id int4 NOT NULL,
	dt_won timestamp NULL,
	user_id int4 NULL,
	CONSTRAINT prize_pkey PRIMARY KEY (id),
	CONSTRAINT prize_admin_id_fkey FOREIGN KEY (admin_id) REFERENCES public."user"(id),
	CONSTRAINT prize_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id)
);


-- public.boat definition

-- Drop table

-- DROP TABLE public.boat;

CREATE TABLE public.boat (
	id serial4 NOT NULL,
	prize_id int4 NOT NULL,
	CONSTRAINT boat_pkey PRIMARY KEY (id),
	CONSTRAINT boat_prize_id_fkey FOREIGN KEY (prize_id) REFERENCES public.prize(id)
);


-- public.game definition

-- Drop table

-- DROP TABLE public.game;

CREATE TABLE public.game (
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
	CONSTRAINT game_admin_id_fkey FOREIGN KEY (admin_id) REFERENCES public."user"(id),
	CONSTRAINT game_player1_id_fkey FOREIGN KEY (player1_id) REFERENCES public.player(id),
	CONSTRAINT game_player2_id_fkey FOREIGN KEY (player2_id) REFERENCES public.player(id)
);


-- public.field definition

-- Drop table

-- DROP TABLE public.field;

CREATE TABLE public.field (
	id serial4 NOT NULL,
	game_id int4 NOT NULL,
	x int4 NOT NULL,
	y int4 NOT NULL,
	injured bool NOT NULL,
	boat_id int4 NULL,
	player_id int4 NULL,
	CONSTRAINT field_pkey PRIMARY KEY (id),
	CONSTRAINT field_boat_id_fkey FOREIGN KEY (boat_id) REFERENCES public.boat(id),
	CONSTRAINT field_game_id_fkey FOREIGN KEY (game_id) REFERENCES public.game(id),
	CONSTRAINT field_player_id_fkey FOREIGN KEY (player_id) REFERENCES public.player(id)
);