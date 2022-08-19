CREATE TABLE pnboia_buoy_metadata (
    pnboia_id INT,
    location VARCHAR (255) UNIQUE NOT NULL,
    latitude float NOT NULL,
    longitude float NOT NULL,
    start_date DATE NOT NULL,
    final_date DATE,
    status INT NOT NULL,
    fname VARCHAR,
    PRIMARY KEY(pnboia_id)
);

CREATE TABLE pnboia_buoy (
    obsv_id INT,
    pnboia_id INT,
    datetime DATE NOT NULL,
    wvht FLOAT,
    wvdir FLOAT,
    tp FLOAT
);

-- new table to save the PNBOIA timeseries
CREATE TABLE pnboia (
    obsv_id INT,
    pnboia_id INT,
    datetime DATE NOT NULL,
    wvht FLOAT,
    wvht_flag_pnboia INT,
    wvht_flag_qartod INT,
    tp FLOAT,
    tp_flag_pnboia INT,
    tp_flag_qartod INT,
    wvdir FLOAT,
    wvdir_flag_pnboia INT,
    wvdir_flag_qartod INT
);

INSERT INTO pnboia_buoy_metadata VALUES (27, 'Alcatrazes', -24.129017, -45.676933, '2022-04-07', NULL, 1, 'alcatrazes');

INSERT INTO pnboia_buoy_metadata VALUES (20, 'Abrolhos', -17.98415, -38.717933, '2022-01-04', NULL, 1, 'abrolhos');

INSERT INTO pnboia_buoy_metadata VALUES (28, 'Fernando de Noronha', -3.7981, -32.3717, '2022-06-04', NULL, 1, 'noronha');

INSERT INTO pnboia_buoy_metadata VALUES (29, 'Imbituba', -28.35045, -48.649833, '2022-07-26', NULL, 1, 'imbituba');
