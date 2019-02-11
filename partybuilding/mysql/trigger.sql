-- delete from django_migrations where app='teaching';
-- create view teaching_takepartin as 
-- select T.id, T.member_id, T.activity_id, A.credit 
-- from takepartin T, info_member M, teaching_activity A
-- where T.member_id=M.netid and T.activity_id=A.id with check option;


DELIMITER //
CREATE TRIGGER TRI_Credit_INSERT 
BEFORE INSERT ON teaching_takepartin
FOR EACH ROW 
BEGIN 
	DECLARE L_date datetime;
	DECLARE L_date2 datetime;
	DECLARE L_credit real;
	SELECT date, end_time, credit INTO L_date, L_date2, L_credit FROM teaching_activity WHERE id=NEW.activity_id;
	SET NEW.date = L_date;
	SET NEW.end_time = L_date2;
  SET NEW.credit = L_credit;
END//