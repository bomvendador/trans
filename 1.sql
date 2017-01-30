--
-- Файл сгенерирован с помощью SQLiteStudio v3.0.6 в Вт янв 24 01:06:15 2017
--
-- Использованная кодировка текста: windows-1251
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Таблица: ru_userprofile
CREATE TABLE "ru_userprofile" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "tel" varchar(15) NOT NULL, "role_id" integer NOT NULL REFERENCES "ru_role" ("id"), "user_id" integer NOT NULL UNIQUE REFERENCES "auth_user" ("id"));
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (1, 'False', 3, 18);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (2, '111', 1, 1);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (3, '222', 3, 14);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (4, '44444', 2, 15);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (5, '23424242', 2, 19);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (6, '2342342342', 3, 24);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (7, '12321321', 3, 25);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (8, '678678678', 3, 26);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (9, '65675675', 3, 27);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (10, '23424242', 3, 28);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (11, '323422342', 3, 29);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (12, '442342432', 3, 30);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (13, '68678678', 3, 31);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (14, '79789789', 3, 32);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (15, '23131312312', 5, 34);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (16, '232222323', 3, 35);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (17, '12321321', 3, 36);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (18, '2331123213', 3, 37);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (19, '3123243242', 3, 38);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (20, '123123131', 3, 39);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (21, '3424242', 3, 40);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (22, '8908908', 3, 41);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (23, '', 2, 44);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (24, '', 2, 45);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (25, '', 2, 46);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (26, '12313132', 3, 47);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (27, '242342342', 3, 51);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (28, '4234234234', 3, 52);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (29, '2342423', 3, 53);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (30, '', 4, 54);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (31, '', 4, 55);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (32, '3231332323', 3, 56);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (33, '4324234234', 3, 57);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (34, '', 3, 58);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (35, '', 3, 59);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (36, '3432424223', 3, 60);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (37, '434235433', 3, 61);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (38, '', 2, 65);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (39, '', 2, 66);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (40, '313123123213', 3, 68);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (41, '423423424', 3, 69);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (42, '432424243', 3, 70);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (43, '345345345', 3, 71);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (44, '2132132331', 3, 72);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (45, '43243224', 3, 73);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (46, '6867867897', 3, 74);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (47, '242442342', 3, 75);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (48, '423432343', 3, 76);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (49, '423432343', 3, 77);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (50, '78978978', 3, 78);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (51, '890890890', 3, 79);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (52, '2432432', 3, 83);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (53, '', 3, 84);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (54, '2312313', 3, 85);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (55, '', 3, 86);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (56, '', 3, 87);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (57, '', 3, 88);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (58, '32342432432', 3, 89);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (59, '24324423', 3, 90);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (60, '', 3, 91);
INSERT INTO ru_userprofile (id, tel, role_id, user_id) VALUES (61, '', 3, 92);

-- Индекс: ru_userprofile_84566833
CREATE INDEX "ru_userprofile_84566833" ON "ru_userprofile" ("role_id");

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
