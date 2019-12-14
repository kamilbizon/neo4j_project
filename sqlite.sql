create table pomiar (urzadzenie TEXT, dane BLOB, data TEXT, id INTEGER PRIMARY KEY);
insert into notatki (urzadzenie, dane, data) values
("jedzenie", "smaczny obiad", datetime('now'));
insert into notatki (urzadzenie, dane, data) values
("praca", "zadanie", datetime('now'));
select * from notatki;