from django.db import models

# Create your models here.


class Member(models.Model):
	"""
	基本信息，包括支部全称、netid、姓名、出生日期、性别、民族、籍贯和专业。
	"""
	branch_name = models.CharField(max_length=50, db_index=True)
	netid = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=30, db_index=True)
	birth_date = models.DateField(max_length=10)
	gender = models.CharField(max_length=1)
	group = models.CharField(max_length=20)
	place_birth = models.CharField(max_length=50)
	major_in = models.CharField(max_length=30)

	class Meta:
		ordering = ('branch_name', 'netid')

	def __str__(self):
		return self.branch_name + ' ' + self.name


class InspectedMember(models.Model):
	"""
	考察对象，包括是否团员、加入党章学习小组时间、入党申请时间、确定为积极分子时间
	"""
	netid = models.OneToOneField(Member, on_delete=models.CASCADE, primary_key=True)
	is_member_CYL = models.BooleanField(default=False)
	constitution_group_date = models.DateField(max_length=10)
	application_date = models.DateField(max_length=10)
	activist_date = models.DateField(max_length=10)
	league_promotion_date = models.DateField(max_length=10)
	democratic_appraisal_date = models.DateField(max_length=10)
	political_check_done = models.BooleanField(default=False)
	key_develop_person_date = models.DateField(max_length=10)
	graduated_party_school_date = models.DateField(max_length=10)


class ProbationaryMember(models.Model):
	netid = models.OneToOneField(InspectedMember, on_delete=models.CASCADE, primary_key=True)
	recommenders_date = models.DateField(max_length=10)
	recommenders = models.CharField(max_length=50)
	autobiography_done = models.BooleanField(default=False)
	application_form_done = models.BooleanField(default=False)
	first_branch_conference = models.DateField(max_length=10)
	pro_conversation_date = models.DateField(max_length=10)
	talker = models.CharField(max_length=50)
	probationary_approval_date = models.DateField(max_length=10)
	oach_date = models.DateField(max_length=10)


class FullMember(models.Model):
	netid = models.OneToOneField(ProbationaryMember, on_delete=models.CASCADE, primary_key=True)
	application_fullmember_date = models.DateField(max_length=10)
	second_branch_conference = models.DateField(max_length=10)
	fullmember_approval_date = models.DateField(max_length=10)
