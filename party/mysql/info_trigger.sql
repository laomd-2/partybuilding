drop trigger if exists info_member_all_before_update;
drop trigger if exists info_member_all_before_insert;

DELIMITER //

CREATE TRIGGER info_member_all_before_update
BEFORE UPDATE
   ON info_member_all FOR EACH ROW
BEGIN
  if NEW.second_branch_conference then
      set NEW.phase = 5;
  elseif NEW.first_branch_conference then
      set NEW.phase = 4;
  elseif NEW.key_develop_person_date then
      set NEW.phase = 3;
  elseif NEW.activist_date then
      set NEW.phase = 2;
  elseif NEW.application_date then
      set NEW.phase = 1;
  end if ;
END; //

CREATE TRIGGER info_member_all_before_insert
BEFORE insert
   ON info_member_all FOR EACH ROW
BEGIN
  if NEW.second_branch_conference then
      set NEW.phase = 5;
  elseif NEW.first_branch_conference then
      set NEW.phase = 4;
  elseif NEW.key_develop_person_date then
      set NEW.phase = 3;
  elseif NEW.activist_date then
      set NEW.phase = 2;
  elseif NEW.application_date then
      set NEW.phase = 1;
  end if ;
END; //

DELIMITER ;