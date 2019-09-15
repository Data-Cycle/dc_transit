
DROP TABLE IF EXISTS wmata_bus;
CREATE TABLE "wmata_bus" (
  "v_id" int,
  "r_id" varchar,
  "t_id" int,
  "retrieved" timestamp,
  "dt" timestamp,
  "lat" float,
  "lng" float,
  "blk" varchar,
  "dev" int,
  "d_num" int,
  "d_txt" int,
  "t_s" timestamp,
  "t_e" timestamp,
  "headsign" varchar,
  CONSTRAINT PK_wmata_bus PRIMARY KEY (v_id, retrieved)
);

DROP TABLE IF EXISTS wmata_bus_route;
CREATE TABLE "wmata_bus_route" (
  "r_id" int PRIMARY KEY,
  "route_name" varchar,
  "route_line" varchar
);

DROP TABLE IF EXISTS wmata_bus_stop;
CREATE TABLE "wmata_bus_stop" (
  "s_id" int PRIMARY KEY,
  "s_name" varchar,
  "lat" int,
  "lng" int
);

DROP TABLE IF EXISTS wmata_bus_sr;
CREATE TABLE "wmata_bus_sr" (
  "s_id" int,
  "r_id" int,
  CONSTRAINT PK_wmata_bus_sr PRIMARY KEY (s_id, r_id)
);

DROP TABLE IF EXISTS wmata_bus_pred;
CREATE TABLE "wmata_bus_pred" (
  "s_id" int,
  "retrieved" timestamp,
  "bus_seq" int,
  "r_id" varchar,
  "d_txt" int,
  "d_num" int,
  "min" int,
  "v_id" int,
  "t_id" int,
  CONSTRAINT PK_wmata_bus_pred PRIMARY KEY (s_id, retrieved, bus_seq)
);


DROP TABLE IF EXISTS wmata_train;
CREATE TABLE "wmata_train" (
  "t_id" int,
  "c_id" int,
  "dt" timestamp,
  "d_num" int,
  "t_num" int,
  "cars" int,
  "line" varchar,
  "dest_station" int,
  "sec_loc" int,
  "service" varchar,
  CONSTRAINT PK_wmata_train PRIMARY KEY (t_id, dt)
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

/*
ALTER TABLE "wmata_bus" ADD FOREIGN KEY ("r_id") REFERENCES "wmata_bus_route" ("r_id");

ALTER TABLE "wmata_bus_route" ADD FOREIGN KEY ("r_id") REFERENCES "wmata_bus_stop" ("r_id");

ALTER TABLE "wmata_train" ADD FOREIGN KEY ("c_id") REFERENCES "wmata_train_circuit" ("c_id");

ALTER TABLE "wmata_train_circuit" ADD FOREIGN KEY ("s_id") REFERENCES "wmata_train_station" ("s_id");
*/
