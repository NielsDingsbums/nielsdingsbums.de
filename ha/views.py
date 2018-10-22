from django.shortcuts import render, redirect
from .models import haItem
from .forms import AddForm, AddFormAuthed, EditForm

from datetime import datetime

# JSON for JS Data
import json

# gspread synchronizer
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Other
import operator


def index(request):
	entrys = haItem.objects.all ()[::-1]

	# Generate Preview
	preview = ''
	for entry in entrys:
		preview = entry.exercise[:80]

		if len (entry.exercise) >= 80:
			preview += ' ...'

		entry.preview = preview

	# Statistics section
	author_data = {}
	author_data_month = {}

	subject_data = {}
	month_data = {}
	total_entries = len (entrys)

	for entry in entrys:

		# Author
		if entry.author == '':
			entry.author = 'Anonym'

		if entry.date_created_at.month == datetime.now().month:
			if entry.author in author_data_month:
				author_data_month[entry.author] += 1

			elif entry.author not in author_data_month:
				author_data_month[entry.author] = 1


		if entry.author in author_data:
			author_data[entry.author] += 1

		elif entry.author not in author_data:
			author_data[entry.author] = 1

		# Subject
		if entry.subject in subject_data:
			subject_data[entry.subject] += 1

		elif entry.subject not in subject_data:
			subject_data[entry.subject] = 1

		# Month
		month = get_month_name (entry.date_created_at)
		if month in month_data:
			month_data[month] += 1

		elif month not in month_data:
			month_data[month] = 1

	# Prepare data

	# author_data
	most_active_author = sorted (author_data_month.items (), key=operator.itemgetter (1))[-1][0]
	most_active_author_entries = sorted (author_data_month.items (), key=operator.itemgetter (1))[-1][1]

	author_data = list (author_data.items ())
	author_data = json.dumps (author_data)

	# subject_data
	subject_data = list (subject_data.items ())
	subject_data = json.dumps (subject_data)

	# month_data
	month_data = list (month_data.items ())[::-1]
	month_data = json.dumps (month_data)


	context = {
		# Chart stuff
		'author_data': author_data,
		'subject_data': subject_data,
		'month_data': month_data,
		'total_entries': total_entries,

		# Author of the month
		'most_active_author': most_active_author,
		'most_active_author_entries': most_active_author_entries,
		
		# Other
		'entrys': entrys,

	}

	return render (request, 'ha/index.html', context)


def get_month_name(date):
	months = ['Januar', 'Februar', 'März', 'August', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November',
			  'Dezember']

	return months[date.month - 2]


def details(request, id):
	entry = haItem.objects.get (id=id)

	context = {
		'entry': entry
	}

	return render (request, 'ha/details.html', context)


def migrate(request):
	scope = ['https://spreadsheets.google.com/feeds',
			 'https://www.googleapis.com/auth/drive']

	creds = ServiceAccountCredentials.from_json_keyfile_name ('client_secret.json', scope)
	client = gspread.authorize (creds)

	sheet = client.open ('Ha8c').sheet1
	ha_records = sheet.get_all_records ()

	haItems = haItem.objects.all ()
	# print(haItems)

	for entry in ha_records:
		dates = [datetime.strftime (datetime.strptime (entry["Datum von"], '%d.%m.%Y'), '%Y-%m-%d'), \
				 datetime.strftime (datetime.strptime (entry["Datum bis"], '%d.%m.%Y'), '%Y-%m-%d')]

		if entry['Fach'] == '':
			entry['Fach'] = 'keins'

		if entry["Fach"][-1] == ' ':
			entry["Fach"] = entry["Fach"][:-1]

		if entry['Fach'] == '':
			entry['Fach'] = 'keins'

		item = haItem (subject=entry["Fach"], exercise=entry["Aufgabe"],
					   information=entry["Infos"], date_created_at=dates[0],
					   date_until=dates[1], author=entry["Autor"])
		# print (item)
		if item not in haItems:
			print ('--- NOT IN DB --\n')
			item.save ()

		else:
			item.delete ()

	return redirect ('/ha/')


def add(request):
	context = {}
	# print(request.user.last_name)

	if request.user.is_authenticated:

		if request.method == 'POST':
			form = AddFormAuthed (request.POST)

			if form.is_valid ():
				if request.user.first_name and request.user.last_name != '':
					author = request.user.first_name[0].capitalize () + request.user.last_name[0].capitalize ()

				else:
					author = request.user.username[:2].upper ()

				data = haItem (exercise=form.cleaned_data['exercise'], subject=form.cleaned_data['subject'],
							   information=form.cleaned_data['information'],
							   date_created_at=form.cleaned_data['date_created_at'],
							   date_until=form.cleaned_data['date_until'], author=author)

				data.save ()
				return redirect ('/ha/')

		else:
			form = AddFormAuthed ()

	else:
		if request.method == 'POST':
			form = AddForm (request.POST)

			if form.is_valid ():
				# print(haItem)
				data = haItem (exercise=form.cleaned_data['exercise'], subject=form.cleaned_data['subject'],
							   information=form.cleaned_data['information'],
							   date_created_at=form.cleaned_data['date_created_at'],
							   date_until=form.cleaned_data['date_until'], author=form.cleaned_data['author'])

				data.save ()
				return redirect ('/ha')

		else:
			form = AddForm ()

	context["form"] = form
	return render (request, 'ha/add.html', {'form': form})


def edit(request, id):

	entry = haItem.objects.get (id=id)

	if request.method == 'POST':
		form = EditForm(request.POST)

		if form.is_valid():
			entry.subject = form.cleaned_data['subject']
			entry.exercise = form.cleaned_data['exercise']
			entry.information = form.cleaned_data['information']
			entry.date_until = form.cleaned_data['date_until']
			entry.save()


	else:
		form = EditForm (initial={
			'subject': entry.subject,
			'exercise': entry.exercise,
			'information': entry.information,
			'date_until': entry.date_until
		})


	print(form)

	context = {
		'entry': entry,
		'form': form
	}

	return render(request, 'ha/edit.html', context)


def deletion_copmplete(request, id):
	entry = haItem.objects.get (id=id)

	entry.delete()

	return render(request, 'ha/deletion_complete.html')

def delete(request, id):
	entry = haItem.objects.get (id=id)
	context = {
		'entry': entry
	}

	return render(request, 'ha/delete.html', context)


def author(request, name):
	name = name.upper ()
	entrys = haItem.objects.filter (author=name)[::-1]

	for entry in entrys:
		preview = entry.exercise[:80]

		if len (entry.exercise) >= 80:
			preview += ' ...'

		entry.preview = preview
	# print(entry.preview)

	number_of_entries = len (entrys)

	return render (request, 'ha/author.html', {'entrys': entrys, 'author': name, 'number': number_of_entries})
