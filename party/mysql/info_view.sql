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
where (out_type = 'unknown' or
       out_place is not null and out_place != '' and (out_type = 'D.就业' or out_type = 'G.境内升学'));
create view info_member as
select *
from info_member_all
where out_type is null
   or not (out_type = 'unknown' or
           out_place is not null and out_place != '' and (out_type = 'D.就业' or out_type = 'G.境内升学'));