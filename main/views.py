from django.shortcuts import render, redirect
from main.models import *
from datetime import datetime

def login(request):
	return render(request, 'main/login.html')

def logout(request):
	request.session['loggedIn?'] = 'false'
	return redirect('/login')

def auth(request):
	inputedPassword = request.GET.get('password', '')
	password = Password.objects.filter()[0]
	if inputedPassword == password.password:
		request.session['loggedIn?'] = 'true'
		return redirect('/')
	return redirect('/login')

def checkLoggedIn(request):
	if request.session.get('loggedIn?', None) == "true":
		return 'true'
	else:
		return 'false'

def index(request):
	if checkLoggedIn(request) == 'false':
		return redirect('/login')

	persons = Person.objects.filter().order_by('name')
	updateInvestments()
	return render(request, 'main/index.html', {'curr_path': request.get_full_path(), 'persons': persons})

def data(request):
	if checkLoggedIn(request) == 'false':
		return redirect('/login')

	companies = Company.objects.filter().order_by('id')
	return render(request, 'main/data.html', {'curr_path': request.get_full_path(), 'companies': companies})

def all(request):
	if checkLoggedIn(request) == 'false':
		return redirect('/login')

	companies = Company.objects.filter().order_by('id')
	everything = []
	for company in companies:
		entries = []
		moreEntries = Entry.objects.filter(company=company)
		for entry in moreEntries:
			entries.append(entry)
		everything.append([company, entries])

	return render(request, 'main/all.html', {'curr_path': request.get_full_path(), 'companies': companies, 'everything': everything})

def newperson(request):
	if checkLoggedIn(request) == 'false':
		return redirect('/login')

	return render(request, 'main/newperson.html', {'curr_path': request.get_full_path()})

def createperson(request):
	if checkLoggedIn(request) == 'false':
		return redirect('/login')

	name = request.GET.get('name', '')
	personQuery = Person.objects.filter(name=name)
	if not not personQuery:
		return redirect('/newperson')
	person = Person(name=name)
	person.save()
	return redirect('/')

def editperson(request, self):
	if checkLoggedIn(request) == 'false':
		return redirect('/login')

	updateInvestments()
	iden = request.get_full_path()[12:]
	person = Person.objects.filter(id=iden)[0]
	companies = Company.objects.filter()
	arr = []
	entrys = []
	for company in companies:
		moreEntrys = Entry.objects.filter(company=company)
		for entry in moreEntrys:
			entrys.append(entry)
	
		votesQuery = Vote.objects.filter(person=person, company=company)
		if not not votesQuery:
			arr.append([company, votesQuery[0]])
		else:
			arr.append([company, ''])

	return render(request, 'main/editperson.html', {
			'curr_path': request.get_full_path(), 
			'person': person,
			'arr': arr,
			'entrys': entrys
		})

def vote(request, self):
	if checkLoggedIn(request) == 'false':
		return redirect('/login')

	iden = request.get_full_path()[6:]
	person = Person.objects.filter(id=iden)[0]
	companies = Company.objects.filter().order_by('id')
	arr = []
	for company in companies:
	
		votesQuery = Vote.objects.filter(person=person, company=company)
		if not not votesQuery:
			arr.append([company, votesQuery[0]])
		else:
			arr.append([company, ''])

	return render(request, 'main/vote.html', {
			'curr_path': request.get_full_path(), 
			'person': person,
			'arr': arr
		})

def newcompany(request):
	if checkLoggedIn(request) == 'false':
		return redirect('/login')

	return render(request, 'main/newcompany.html', {'curr_path': request.get_full_path()})

def createcompany(request):
	name = request.GET.get('name', '')
	companyQuery = Company.objects.filter(name=name)
	if not not companyQuery:
		return redirect('/newcompany')
	company = Company(name=name)
	company.save()
	return redirect('/data')

def editcompany(request, self):
	if checkLoggedIn(request) == 'false':
		return redirect('/login')

	iden = request.get_full_path()[13:]
	company = Company.objects.filter(id=iden)[0]
	entrys = Entry.objects.filter(company=company).order_by('date')
	return render(request, 'main/editcompany.html', {
			'curr_path': request.get_full_path(), 
			'company': company,
			'entrys': entrys
		})

def newvote(request):
	if checkLoggedIn(request) == 'false':
		return redirect('/login')

	person = request.GET.get('person', '')
	company = request.GET.get('company', '')
	return render(request, 'main/newvote.html', {
			'curr_path': request.get_full_path(),
			'person': person,
			'company': company
		})

def createvote(request):
	if checkLoggedIn(request) == 'false':
		return redirect('/login')

	yes_or_no = request.GET.get('yes_or_no', '')
	company = Company.objects.filter(name=request.GET.get('company', ''))
	person = Person.objects.filter(name=request.GET.get('person', ''))

	if not person or not company:
		return redirect('/newvote')

	vote = Vote(yes_or_no=yes_or_no, company=company[0], person=person[0])
	vote.save()

	return redirect('vote/' + str(person[0].id))

def newentry(request):
	if checkLoggedIn(request) == 'false':
		return redirect('/login')

	company = request.GET.get('company', '')
	return render(request, 'main/newentry.html', {
			'curr_path': request.get_full_path(),
			'company': company
		})

def createentry(request):
	if checkLoggedIn(request) == 'false':
		return redirect('/login')

	company = Company.objects.filter(name=request.GET.get('company', ''))[0]

	if getMostRecentNav(company):
		if getMostRecentNav(company).TYPE == 'exit':
			return redirect('editcompany/' + str(company.id))
	
	date = request.GET.get('date', '')
	amount = request.GET.get('amount', '')
	TYPE = request.GET.get('type', '')
	notes = request.GET.get('notes', '')

	entry = Entry(company=company, date=date, amount=amount, TYPE=TYPE, notes=notes)
	entry.save()

	return redirect('editcompany/' + str(company.id))

def updateInvestments():

	persons = Person.objects.filter()
	for person in persons:
		invested = 0
		anti_invested = 0
		nav = 0
		anti_nav = 0
		cashflowArr = []
		anti_cashflowArr = []
		votes = Vote.objects.filter(person=person)
		for vote in votes:
			entrys = Entry.objects.filter(company=vote.company)
			mostRecentNav = getMostRecentNav(vote.company)
			if vote.yes_or_no == 'yes':
				for entry in entrys:
					if entry.TYPE == 'contribution':
						invested += entry.amount
						cashflowArr.append((entry.date, int(entry.amount) * -1))
					elif entry.TYPE == 'distribution':
						nav += entry.amount
						cashflowArr.append((entry.date, int(entry.amount)))
				if mostRecentNav:
					nav += mostRecentNav.amount
			else:
				for entry in entrys:
					if entry.TYPE == 'contribution':
						anti_invested += entry.amount
						anti_cashflowArr.append((entry.date, int(entry.amount) * -1))
					elif entry.TYPE == 'distribution':
						anti_nav += entry.amount
						anti_cashflowArr.append((entry.date, int(entry.amount)))
				if mostRecentNav:
					anti_nav += mostRecentNav.amount

			if mostRecentNav:
				if vote.yes_or_no == 'yes':
					cashflowArr.append((mostRecentNav.date, mostRecentNav.amount))
				else:
					anti_cashflowArr.append((mostRecentNav.date, mostRecentNav.amount))

		person.invested = invested
		person.anti_invested = anti_invested
		person.nav = nav
		person.anti_nav = anti_nav
		if not invested == 0:
			person.tvpi = round(nav/invested, 2)
		else:
			person.tvpi = 0
		if not anti_invested == 0:
			person.anti_tvpi = anti_nav/anti_invested
		else:
			person.anti_tvpi = 0
		person.xirr = round(100*xirr(cashflowArr), 2)
		person.anti_xirr = round(100*xirr(anti_cashflowArr), 2)
		person.save()

def getMostRecentNav(company):
	entrys = Entry.objects.filter(company=company).order_by('date').reverse()
	for entry in entrys:
		if entry.TYPE == 'nav' or entry.TYPE == 'exit':
			return entry
	return False

def xirr(transactions):
	sumofcashflows = 0
	for x in transactions:
		sumofcashflows += x[1]
	if sumofcashflows == 0:
		return 0
	years = [(ta[0] - transactions[0][0]).days / 365.0 for ta in transactions]
	residual = 1
	step = 0.05
	guess = 0.05
	epsilon = 0.0001
	limit = 10000
	while abs(residual) > epsilon and limit > 0:
		limit -= 1
		residual = 0.0
		for i, ta in enumerate(transactions):
			if not (guess == 0):
				residual += ta[1]/pow(guess, years[i])

		if abs(residual) > epsilon:
			if residual > 0:
				guess += step
			else:
				guess -= step
				step /= 2.0

	return guess-1

