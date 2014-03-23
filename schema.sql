DROP TABLE IF EXISTS data ;

CREATE TABLE data (
    id varchar NOT NULL,
    f0 varchar,
    f1 varchar,
    f2 varchar,
    f3 varchar,
    f4 varchar,
    f5 varchar,
    f6 varchar,
    f7 varchar,
    f8 varchar,
    f9 varchar,
    PRIMARY KEY (id)
);

CREATE FUNCTION upsert_data_f0(key varchar, value varchar) RETURNS VOID AS
$$
BEGIN
    LOOP
        UPDATE data SET f0 = value WHERE id = key;
        IF found THEN
            RETURN;
        END IF;
        BEGIN
            INSERT INTO data(id,f0) VALUES (key, value);
            RETURN;
        EXCEPTION WHEN unique_violation THEN
        END;
    END LOOP;
END;
$$
LANGUAGE plpgsql;
