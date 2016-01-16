create table sensors (
    id           integer primary key autoincrement not null,
    serial_code  text not null,
    name         text not null,
    location     text,
    deleted      integer not null default 0
);

create table sensor_readings (
    id           integer primary key autoincrement not null,
    sensor_id    integer not null references sensors(id),
    value        real not null,
    timestamp    timestamp not null default CURRENT_TIMESTAMP,
    deleted      integer not null default 0
);

create view monthly_temp_avg as
    SELECT
        a.date,
        a.average as 'Current Year Average',
        b.average as 'Previous Year Average',
        round(a.average - b.average, 1) as 'Difference'
    FROM
    (SELECT
        round(julianday(date(datetime('now', 'localtime')))-julianday(date(datetime(sr.timestamp, 'localtime')))) as id,
        date(datetime(sr.timestamp, 'localtime')) as 'Date',
        round(avg(sr.value),1) as 'Average'
    FROM
        sensor_readings sr
    WHERE
        sr.sensor_id=4
        AND datetime(sr.timestamp, 'localtime') > date(datetime(datetime('now', 'localtime'), '-1 month'))
    GROUP BY
        date(datetime(sr.timestamp, 'localtime'))) a
    JOIN
    (SELECT
        round(julianday(date(datetime(datetime('now', 'localtime'), '-1 year')))-julianday(date(datetime(sr.timestamp, 'localtime')))) as id,
        date(datetime(sr.timestamp, 'localtime')) as 'Date',
        round(avg(sr.value),1) as 'Average'
    FROM
        sensor_readings sr
    WHERE
        sr.sensor_id=4
        AND datetime(sr.timestamp, 'localtime') > date(datetime(datetime('now', 'localtime'), '-13 months'))
        AND datetime(sr.timestamp, 'localtime') < date(datetime(datetime('now', 'localtime'), '-1 year'))
    GROUP BY
        date(datetime(sr.timestamp, 'localtime'))) b ON (a.id = b.id);

create view daily_sensor_metrics as
    SELECT 
        s.name,
        (SELECT
            round(value, 1)
        FROM
            sensor_readings
        WHERE
            sensor_id = s.id
        ORDER BY
            timestamp desc
        LIMIT 1) as current,
        round(avg(sr.value), 1) as 'average',
        round(min(sr.value), 1) as 'min',
        round(max(sr.value), 1) as 'max'
    FROM
        sensor_readings sr
        JOIN sensors s ON (sr.sensor_id = s.id)
    WHERE
        sr.deleted = 0
        AND s.deleted = 0
        AND sr.timestamp > datetime('now', '-24 hour')
    GROUP BY
        s.id
    ORDER BY
        name asc;
