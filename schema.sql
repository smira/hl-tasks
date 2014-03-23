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

CREATE OR REPLACE FUNCTION upsert_data_f0(key varchar, value varchar) RETURNS VOID AS
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

CREATE OR REPLACE FUNCTION upsert_data_f1(key varchar, value varchar) RETURNS VOID AS
$$
BEGIN
    LOOP
        UPDATE data SET f1 = value WHERE id = key;
        IF found THEN
            RETURN;
        END IF;
        BEGIN
            INSERT INTO data(id,f1) VALUES (key, value);
            RETURN;
        EXCEPTION WHEN unique_violation THEN
        END;
    END LOOP;
END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION upsert_data_f2(key varchar, value varchar) RETURNS VOID AS
$$
BEGIN
    LOOP
        UPDATE data SET f2 = value WHERE id = key;
        IF found THEN
            RETURN;
        END IF;
        BEGIN
            INSERT INTO data(id,f2) VALUES (key, value);
            RETURN;
        EXCEPTION WHEN unique_violation THEN
        END;
    END LOOP;
END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION upsert_data_f3(key varchar, value varchar) RETURNS VOID AS
$$
BEGIN
    LOOP
        UPDATE data SET f3 = value WHERE id = key;
        IF found THEN
            RETURN;
        END IF;
        BEGIN
            INSERT INTO data(id,f3) VALUES (key, value);
            RETURN;
        EXCEPTION WHEN unique_violation THEN
        END;
    END LOOP;
END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION upsert_data_f4(key varchar, value varchar) RETURNS VOID AS
$$
BEGIN
    LOOP
        UPDATE data SET f4 = value WHERE id = key;
        IF found THEN
            RETURN;
        END IF;
        BEGIN
            INSERT INTO data(id,f4) VALUES (key, value);
            RETURN;
        EXCEPTION WHEN unique_violation THEN
        END;
    END LOOP;
END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION upsert_data_f5(key varchar, value varchar) RETURNS VOID AS
$$
BEGIN
    LOOP
        UPDATE data SET f5 = value WHERE id = key;
        IF found THEN
            RETURN;
        END IF;
        BEGIN
            INSERT INTO data(id,f5) VALUES (key, value);
            RETURN;
        EXCEPTION WHEN unique_violation THEN
        END;
    END LOOP;
END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION upsert_data_f6(key varchar, value varchar) RETURNS VOID AS
$$
BEGIN
    LOOP
        UPDATE data SET f6 = value WHERE id = key;
        IF found THEN
            RETURN;
        END IF;
        BEGIN
            INSERT INTO data(id,f6) VALUES (key, value);
            RETURN;
        EXCEPTION WHEN unique_violation THEN
        END;
    END LOOP;
END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION upsert_data_f7(key varchar, value varchar) RETURNS VOID AS
$$
BEGIN
    LOOP
        UPDATE data SET f7 = value WHERE id = key;
        IF found THEN
            RETURN;
        END IF;
        BEGIN
            INSERT INTO data(id,f7) VALUES (key, value);
            RETURN;
        EXCEPTION WHEN unique_violation THEN
        END;
    END LOOP;
END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION upsert_data_f8(key varchar, value varchar) RETURNS VOID AS
$$
BEGIN
    LOOP
        UPDATE data SET f8 = value WHERE id = key;
        IF found THEN
            RETURN;
        END IF;
        BEGIN
            INSERT INTO data(id,f8) VALUES (key, value);
            RETURN;
        EXCEPTION WHEN unique_violation THEN
        END;
    END LOOP;
END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION upsert_data_f9(key varchar, value varchar) RETURNS VOID AS
$$
BEGIN
    LOOP
        UPDATE data SET f9 = value WHERE id = key;
        IF found THEN
            RETURN;
        END IF;
        BEGIN
            INSERT INTO data(id,f9) VALUES (key, value);
            RETURN;
        EXCEPTION WHEN unique_violation THEN
        END;
    END LOOP;
END;
$$
LANGUAGE plpgsql;
