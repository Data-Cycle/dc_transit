CREATE TABLE "bus_position" (
  "v_id" int PRIMARY KEY,
  "r_id" int,
  "t_id" int,
  "dt" datetime,
  "lat" float,
  "lng" float,
  "blk" str,
  "dev" int,
  "d_num" int,
  "d_txt" int,
  "t_s" datetime,
  "t_e" datetime,
  "headsign" str
);

CREATE TABLE "route" (
  "r_id" int PRIMARY KEY,
  "route_name" str,
  "route_line" str
);

CREATE TABLE "stop" (
  "s_id" int PRIMARY KEY,
  "r_id" int PRIMARY KEY,
  "s_name" str,
  "lat" int,
  "lng" int
);

CREATE TABLE "train_position" (
  "t_id" int PRIMARY KEY,
  "c_id" int,
  "dt" datetime,
  "d_num" int,
  "t_num" int,
  "cars" int,
  "line" int,
  "dest_station" int,
  "sec_loc" int,
  "service" str
);

CREATE TABLE "station" (
  "s_id" int PRIMARY KEY,
  "s_name" str,
  "lat" int,
  "lng" int
);

CREATE TABLE "circuit" (
  "c_id" int,
  "lat" int,
  "lng" int,
  "s_id" int
);

ALTER TABLE "bus_position" ADD FOREIGN KEY ("r_id") REFERENCES "route" ("r_id");

ALTER TABLE "route" ADD FOREIGN KEY ("r_id") REFERENCES "stop" ("r_id");

ALTER TABLE "train_position" ADD FOREIGN KEY ("c_id") REFERENCES "circuit" ("c_id");

ALTER TABLE "circuit" ADD FOREIGN KEY ("s_id") REFERENCES "station" ("s_id");