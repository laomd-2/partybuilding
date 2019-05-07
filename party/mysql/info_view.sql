create view notice_firsttalk as select branch_id, netid, name, application_date from info_member
    where activist_date is null and date_sub(CURDATE(), INTERVAL 1 month) <= application_date;

create view notice_activist as select branch_id, netid, name, application_date from info_member
    where activist_date is null and application_date is not null date_sub(CURDATE(), INTERVAL 1 month) > application_date;

create view notice_keydevelop as select branch_id, netid, name, activist_date from info_member
    where key_develop_person_date is null and activist_date is not null
    and date_sub(CURDATE(), INTERVAL 1 year) > date_sub(activist_date, interval 1 month);

create view notice_premember as select branch_id, netid, name, key_develop_person_date from info_member
    where first_branch_conference is null and key_develop_person_date is not null
    and date_sub(CURDATE(), INTERVAL 1 month) > key_develop_person_date;

create view notice_fullmember as
    select branch_id, netid, name, application_date, first_branch_conference, application_fullmember_date
    from info_member
    where second_branch_conference is null and first_branch_conference is not null and application_fullmember_date is not null
    and date_sub(CURDATE(), INTERVAL 1 year) > date_sub(first_branch_conference, interval 1 month);