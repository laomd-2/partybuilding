alter table info_branch rename info_branch_all;
alter table info_member rename info_member_all;

create view info_branch as
select *
from info_branch_all
where id = 6
   or id > 72 and id != 106;
create view info_oldmember as
select *
from info_member_all
where branch_id != (select id from info_branch where branch_name='出国留学党支部') and (out_type = 'unknown' or out_type is not null and out_type != '' and
       out_place is not null and out_place != '' and out_type != '延毕');
create view info_member as
select *
from info_member_all
where branch_id = (select id from info_branch where branch_name='出国留学党支部') or (out_type is null or out_type = '') or
  (out_place is null or out_place = '') or out_type = '延毕';