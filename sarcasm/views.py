from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.core.mail import send_mail
from django.urls import reverse
from .models import Register, Stage, Bonus
from django.views import View
from django.utils import timezone
from .forms import *
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return render(request, 'login.html')

def home(request):
	error_message = ""
	repeatrollnew = []
	context = {'error_message':error_message, 'repeatroll':repeatrollnew}
	if request.method=="POST":
		
		team_name = request.POST.get('team_name')
		leader_first_name = request.POST.get('leader_first_name')
		# leader_last_name = request.POST.get('leader_last_name')
		leader_roll_number = request.POST.get('leader_roll_number')
		leader_whatsapp_number = request.POST.get('leader_whatsapp_number')
		team_logo = request.POST.get('team_logo')
		player2_first_name = request.POST.get('player2_first_name')
		# player2_last_name = request.POST.get('player2_last_name')
		player2_roll_number = request.POST.get('player2_roll_number')
		player3_first_name = request.POST.get('player3_first_name')
		# player3_last_name = request.POST.get('player3_last_name')
		player3_roll_number = request.POST.get('player3_roll_number')
		player4_first_name = request.POST.get('player4_first_name')
		# player4_last_name = request.POST.get('player4_last_name')
		player4_roll_number = request.POST.get('player4_roll_number')
		player5_first_name = request.POST.get('player5_first_name')
		# player5_last_name = request.POST.get('player5_last_name')
		player5_roll_number = request.POST.get('player5_roll_number')


		allowed_roll_numbers = ["22",""]
		league = False
		if (leader_roll_number[:2] in allowed_roll_numbers and player2_roll_number[:2] in allowed_roll_numbers and player3_roll_number[:2] in allowed_roll_numbers and player4_roll_number[:2] in allowed_roll_numbers and player5_roll_number[:2] in allowed_roll_numbers):
			league = True
			# if(leader_roll_number=="200040085" or leader_roll_number=="200010050"):
			# 	league = True
			
		register = Register(team_name = team_name, leader_first_name = leader_first_name,
		leader_roll_number = leader_roll_number, leader_whatsapp_number = leader_whatsapp_number, team_logo = team_logo,
		player2_first_name = player2_first_name, player2_roll_number = player2_roll_number,
		player3_first_name = player3_first_name, player3_roll_number = player3_roll_number,
		player4_first_name = player4_first_name, player4_roll_number = player4_roll_number,
		player5_first_name = player5_first_name, player5_roll_number = player5_roll_number,
		curr_stage = Stage.objects.filter(_id=1).first(),
		league = league)

		repeatroll = []
		if verifyrollnumber(leader_roll_number): repeatroll.append(leader_roll_number)
		if verifyrollnumber(player2_roll_number): repeatroll.append(player2_roll_number)
		if verifyrollnumber(player3_roll_number): repeatroll.append(player3_roll_number)
		if verifyrollnumber(player4_roll_number): repeatroll.append(player4_roll_number)
		if verifyrollnumber(player5_roll_number): repeatroll.append(player5_roll_number)

		if(len(repeatroll)!=0): 
			context = {'error_message':'Some players are already registered in a different team', 'repeatroll':repeatroll}
			return render(request, 'register.html', context)
		if league==False:
			context = {'freshie_error_message':'Only freshies are allowed to register!'}
			return render(request, 'register.html', context)

		register.save()

        # to send login credentials
		teamFetch = Register.objects.filter(leader_roll_number=leader_roll_number).first()
		email=str(leader_roll_number)+'@iitb.ac.in'
		user = User.objects.create(username = leader_roll_number, email = email)
		password = User.objects.make_random_password()	
		user.set_password(password)
		teamFetch.user = user
		user.save()
		teamFetch.save()
		# print(password)
		recipient = [email]
		if(player2_roll_number):
			recipient.append(str(player2_roll_number)+'@iitb.ac.in')
		if(player3_roll_number):
			recipient.append(str(player3_roll_number)+'@iitb.ac.in')
		if(player4_roll_number):
			recipient.append(str(player4_roll_number)+'@iitb.ac.in')
		if(player5_roll_number):
			recipient.append(str(player5_roll_number)+'@iitb.ac.in')
		# recipient = [email, str(player2_roll_number)+'@iitb.ac.in', str(player3_roll_number)+'@iitb.ac.in' , str(player4_roll_number)+'@iitb.ac.in', str(player5_roll_number)+'@iitb.ac.in'  ]
		# send_otp(teamFetch.team_name, recipient, password, leader_roll_number)
		print(password) 

		success = True
		# return render(request, 'success.html')
		return redirect('login')
		context = {'success':success}
	return render(request, 'register.html')
    
def send_otp(teamname, recipient, password, leader_roll_number):
    subject = "SARCASM 2023 Login Credentials"
    message = f'''
	Greetings 
	Welcome to SARCASM 2023! We welcome you to Insti's most awaited crypt hunt. Join the adventure with your friends and conquer the challenge! So put on your thinking caps and get ready to hunt! Good luck and may the best team win!
	
	The login credentials for your team ''' + str(teamname)+ ' are: \nUsername: ' + str(leader_roll_number) + '\nPassword: ' + str(password)+'\nUse these credentials to log into the portal when it goes live on Friday (06-01-2023). \nStay tuned and follow https://www.instagram.com/sarc_iitb/ for updates.\n\nRegards,\nWeb Team @ Student Alumni Relations Cell, IIT Bombay'
    email_from = 'example@gmail.com'
    send_mail(subject, message, email_from, recipient, fail_silently=True)
    return None

def login(request):
	if request.user.is_authenticated:
		return redirect(reverse('play'))
	if request.method == 'POST':
		uname=request.POST.get('username')
		password=request.POST.get('password')
		user = User.objects.filter(username=uname).first()
		if user is None:
			context = {'message': 'Username does not exist!', 'class': 'danger'}
			return render(request, 'login.html', context)
		else:
			# team = Team.objects.filter(user=user).first()
			user2 = authenticate(request, username=uname, password=password)
			if user2 is not None:
				auth_login(request, user2)
				return redirect(reverse('play'))
			else:
				context = {'message': 'Incorrect password!', 'class': 'danger', 'user2': user.password, 'pass': password}
				return render(request, 'login.html', context)
	return render(request, 'login.html')

def validate_username(request):
	username = request.GET.get('username', None)
	ucheck = Register.objects.filter(leader_roll_number=username).exists() or Register.objects.filter(player2_roll_number=username).exists() or Register.objects.filter(player3_roll_number=username).exists() or Register.objects.filter(player4_roll_number=username).exists() or Register.objects.filter(player5_roll_number=username).exists()
	if len(username)==0: ucheck = False
	data = {
        'is_taken': ucheck
    }
	return JsonResponse(data)

def verifyrollnumber(username):
	ucheck =  Register.objects.filter(leader_roll_number=username).exists() or Register.objects.filter(player2_roll_number=username).exists() or Register.objects.filter(player3_roll_number=username).exists() or Register.objects.filter(player4_roll_number=username).exists() or Register.objects.filter(player5_roll_number=username).exists()
	if len(username)==0: ucheck = False
	return ucheck

def success(request):
	return render(request, success.html)

def faqs(request):
	return render(request, 'faq.html')

def support(request):
	return render(request, 'techsupport.html')

def leaderboard(request):
 if request.method == 'POST':
  league = request.POST.get('league')  
  if league == "True":
   top_teams = Register.objects.filter(league = "True").order_by('-score')
   context = {'top_teams': top_teams}
   return render(request,'leaderboard.html', context)
  top_teams = Register.objects.order_by('-score')
  context = {'top_teams': top_teams}
  return render(request,'leaderboard.html', context)
 return render(request,'leaderboard.html')


def skip(request):
	current_team = Register.objects.filter(user=request.user).first()
	if  current_team.skips==1:
		current_team.skips = 0
		current_stage = current_team.curr_stage
		current_stage.no_teams_solving -= 1
		new_stage = Stage.objects.filter(_id = current_stage._id + 1).first() 
		current_team.curr_stage = new_stage
		new_stage.no_teams_solving += 1
		current_team.latest_stage_time = timezone.now()
		current_team.save()
		current_stage.save()
		new_stage.save()
		
	return redirect(reverse('play'))
 
class Play(View) :
	# @login_required(login_url="/login")
	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return redirect('login')
		
		curr_team = Register.objects.filter(user=request.user).first()
		team_logo = "../static/img/register/" + curr_team.team_logo + ".png"
		curr_stage = curr_team.curr_stage

		if curr_team.bonus_type != -1:
			if timezone.now() > Bonus.objects.filter(_id=curr_team.curr_bonus_level).first().exp_time:
				curr_team.score -= [0, 3, 6][curr_team.bonus_type]
				curr_team.bonus_type = -1
				curr_team.save()
			else:
				return redirect(reverse('bonus'))

		context = {
			'stage' : curr_stage,
			'team': curr_team,
			'logo': team_logo,
		}
		bns = curr_team.curr_bonus_level
		if bns == 0:
			nextbonus = bns+1
		else: nextbonus = bns
		nextbonusques = Bonus.objects.filter(_id=nextbonus).first()
		nextstart = nextbonusques.live_time
		delta = nextstart - timezone.now()
		context['timeleft'] = (delta.seconds*10**6 + delta.microseconds)/1000
		
		return render(request, "play.html", context)   #{{form|crispy}} crispy form was removed try to add it back

	# @login_required(login_url="/login")
	def post(self, request, *args, **kwargs):

		if not request.user.is_authenticated:
			return redirect('login')

		current_team = Register.objects.get(user = request.user)
		current_stage = current_team.curr_stage

		response = request.POST.get('answer')
		correct_response = current_stage.answer

		if hash(response) == hash(correct_response):

			current_team.score += 3
			current_stage.no_teams_solved += 1
			current_stage.no_teams_solving -= 1
			new_stage = Stage.objects.filter(_id = current_stage._id + 1).first() 
			current_team.curr_stage = new_stage
			new_stage.no_teams_solving += 1
			current_team.save()
			current_stage.save()
			new_stage.save()

		return redirect('play')


@login_required(login_url="/login")
def bonus(request):
	current_team = Register.objects.filter(user=request.user).first()
	if request.method == "POST":
		bonus_type = current_team.bonus_type
		if bonus_type == -1:
			bonus_type = request.POST.get("bonus_type")
			current_team.bonus_type = bonus_type
			current_team.save()
			print("stealing virginity")
			return redirect(reverse('bonus'))

		current_bonus_id = current_team.curr_bonus_level

		response = request.POST.get('answer')
		correct_response = Bonus.objects.filter(_id=current_bonus_id).first().answer

		if response == correct_response:
			current_team.score += [6, 9, 12][bonus_type]
			current_team.curr_bonus_level += 1
			current_team.bonus_type = -1
			current_team.save()
			print("correct ansewr, redirecting")
			return redirect('play')
		print("Go to bonous!")
		return redirect('bonus')
	else:
		bonus_type = current_team.bonus_type
		if bonus_type == -1:
			print("get the fuck out")
			return redirect(reverse('play'))
		time_pairs = []
		for object in Bonus.objects.all():
			time_pairs.append((object._id, object.live_time, object.exp_time))
		time_idx = -1
		for idx, time_pair in enumerate(time_pairs):
			if timezone.now() >= time_pair[1] and timezone.now() <= time_pair[2]:
				time_idx = time_pair[0]
				break
		if time_idx != -1:
			if current_team.curr_bonus_level <= time_idx:
				current_team.curr_bonus_level = time_idx
			else:
				print("Redirecting to play because time expired")
				return redirect('play')
			current_team.save()
			delta = Bonus.objects.filter(_id=time_idx).first().exp_time - timezone.now()
			return render(request, 'bonus.html', context={'teamname': current_team.team_name, 'teamlogo': current_team.team_logo, 'score': current_team.score, 'question': Bonus.objects.filter(_id=time_idx).first().question, 'time_remaining': (delta.seconds*10**6 + delta.microseconds)/1000, 'exp_time': Bonus.objects.filter(_id=time_idx).first().exp_time, 'now_time': timezone.now(), 'curr_bonus_level': current_team.curr_bonus_level})
		else:
			# print("Why am I here?")
			# if current_team.curr_bonus_level == time_idx:
			# 	current_team.score -= [0, 3, 6][int(request.GET.get("bonus_type"))]
			# 	current_team.save()
			print("Redirecting because idek why")
			current_team.bonus_type = -1
			current_team.save()
			return redirect('play')