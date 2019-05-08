-- update dynamic_info d set telephone=(select phone_number from info_member where netid=d.student_num) where branch_id=85;
-- update dynamic_info d set address=(select family_address from info_member where netid=d.student_num) where branch_id=85;
-- insert into info_oldmember
-- select student_num, name, birth, gender, nation, native_place, telephone, domain, time_party_study_group, time_apply, time_out, time_active, null, time_discuss, time_recommend_league, time_focusing, time_introducer, name_introducer, time_train, time_branch_meeting_1, time_join_talk, name_join_talk, time_probationary, time_oath, time_apply_regular, time_branch_meeting_2, time_regular, branch_id, is_league, is_apply_book, is_autobiog, is_political_check, 1, NULL, 4 from `party_info_affair_system`.dynamic_info where branch_id=85 and student_num=15336142;

create view info_member as select * from info_member_all where netid > (year(curdate()) + (month(curdate()) >= 9) - years - 2000) * 1000000;
create view info_oldmember as select * from info_member_all where netid <= (year(curdate()) + (month(curdate()) >= 9) - years - 2000) * 1000000;
-- select * from info_member_all where netid=12345678;

create view info_branch as select * from info_branch_all where id=6 or id > 100 or exists (select netid from info_member where branch_id=id);
-- create view teaching_takepartin as select * from teaching_takepartin_all where exists (select netid from info_member where netid=member_id and first_branch_conference is not null);
-- create view teaching_takepartin2 as select * from teaching_takepartin_all where exists (select netid from info_member where netid=member_id and first_branch_conference is null);