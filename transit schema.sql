
DROP TABLE IF EXISTS wmata_bus;
CREATE TABLE "wmata_bus" (
  "v_id" int PRIMARY KEY,
  "r_id" varchar,
  "t_id" int,
  "dt" timestamp,
  "lat" float,
  "lng" float,
  "blk" varchar,
  "dev" int,
  "d_num" int,
  "d_txt" int,
  "t_s" timestamp,
  "t_e" timestamp,
  "headsign" varchar
);

DROP TABLE IF EXISTS wmata_bus_route;
CREATE TABLE "wmata_bus_route" (
  "r_id" int PRIMARY KEY,
  "route_name" varchar,
  "route_line" varchar
);

DROP TABLE IF EXISTS wmata_bus_stop;
CREATE TABLE "wmata_bus_stop" (
  "s_id" int,
  "r_id" int,
  "s_name" varchar,
  "lat" int,
  "lng" int
);


DROP TABLE IF EXISTS wmata_train;
CREATE TABLE "wmata_train" (
  "t_id" int PRIMARY KEY,
  "c_id" int,
  "dt" timestamp,
  "d_num" int,
  "t_num" int,
  "cars" int,
  "line" int,
  "dest_station" int,
  "sec_loc" int,
  "service" varchar
);

DROP TABLE IF EXISTS wmata_train_station;
CREATE TABLE "wmata_train_station" (
  "s_id" int PRIMARY KEY,
  "s_name" varchar,
  "lat" int,
  "lng" int
);

DROP TABLE IF EXISTS wmata_train_circuit;
CREATE TABLE "wmata_train_circuit" (
  "c_id" int,
  "lat" int,
  "lng" int,
  "s_id" int
);

ALTER TABLE "wmata_bus" ADD FOREIGN KEY ("r_id") REFERENCES "wmata_bus_route" ("r_id");

ALTER TABLE "wmata_bus_route" ADD FOREIGN KEY ("r_id") REFERENCES "wmata_bus_stop" ("r_id");

ALTER TABLE "wmata_train" ADD FOREIGN KEY ("c_id") REFERENCES "wmata_train_circuit" ("c_id");

ALTER TABLE "wmata_train_circuit" ADD FOREIGN KEY ("s_id") REFERENCES "wmata_train_station" ("s_id");
