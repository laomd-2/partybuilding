drop view if exists info_branch;
drop view if exists info_member;
drop view if exists info_oldmember;

alter table info_branch_all rename info_branch;
alter table info_member_all rename info_member;
