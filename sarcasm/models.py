from django.db import models
from django.contrib.auth.models import User

class Stage(models.Model):
    _id = models.IntegerField(primary_key=True) 
    title = models.TextField()
    question = models.TextField()
    # image = models.ImageField(upload_to="static/questions/", null=True, blank=True)
    answer = models.TextField()
    no_teams_solving = models.IntegerField(default=0)
    no_teams_solved = models.IntegerField(default=0)

class Register(models.Model):
    team_name = models.CharField(max_length=100, blank=False)
    leader_first_name = models.CharField(max_length=100, blank=False)
    # leader_last_name = models.CharField(max_length=100, blank=False)
    leader_roll_number = models.CharField(max_length=100, blank=False, primary_key=True)
    leader_whatsapp_number = models.CharField(max_length=100, blank=False)	
    team_logo = models.CharField(max_length=100, null=True, blank=False)
    player2_first_name = models.CharField(max_length=100, blank = True)
    # player2_last_name = models.CharField(max_length=100, blank = True)
    player2_roll_number = models.CharField(max_length=100, blank = True)
    player3_first_name = models.CharField(max_length=100, blank = True)
    # player3_last_name = models.CharField(max_length=100, blank = True)
    player3_roll_number = models.CharField(max_length=100, blank = True)
    player4_first_name = models.CharField(max_length=100, blank = True)
    # player4_last_name = models.CharField(max_length=100, blank = True)
    player4_roll_number = models.CharField(max_length=100, blank = True)
    player5_first_name = models.CharField(max_length=100, blank = True)
    # player5_last_name = models.CharField(max_length=100, blank = True)
    player5_roll_number = models.CharField(max_length=100, blank = True)
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    league = models.BooleanField( blank=False, default=False)
    curr_stage_id = models.IntegerField(default=0)
    curr_bonus_level = models.IntegerField(default=0)
    bonus_type = models.IntegerField(default=-1)
    score = models.IntegerField(default=0)
    skips = models.IntegerField(default=1)
    no_bonus_solved = models.IntegerField(default=0)
    no_negative_score = models.IntegerField(default=0)

class Bonus(models.Model):
    _id = models.IntegerField(primary_key=True) 
    title = models.TextField()
    question = models.TextField()
    # image = models.ImageField(upload_to="static/bonus/", null=True, blank=True)
    answer = models.TextField()
    no_teams_solving = models.IntegerField(default=0)
    no_teams_solved = models.IntegerField(default=0)
    live_time = models.DateTimeField()
    exp_time = models.DateTimeField()