import string

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django import forms
from django.template import RequestContext

from xml.etree import ElementTree
import gdata.spreadsheet.service
import gdata.service
import gdata.spreadsheet

from count.models import Poll

from support import google_spreadsheets
from wordcount import Analyzer

def spreadsheets(request):
  """Lists all of the spreadsheets."""
  ss = get_ss(request)
  
  spreadsheets = []
  for i, entry in enumerate(ss.spreadsheets().entry):
    spreadsheets.append({
      'id':i,
      'title':entry.title.text
    })

  return render_to_response('count/spreadsheets.html',
      {'spreadsheets': spreadsheets})

def spreadsheet(request, spreadsheet_id):
  """Shows information about a specific spreadsheet."""
  ss = get_ss(request)
  ss.set_spreadsheet(spreadsheet_id)

  worksheets = []
  for i, entry in enumerate(ss.worksheets().entry):
    worksheets.append({'id' : i, 'title' : entry.title.text})

  return render_to_response('count/worksheets.html', {
    'spreadsheet_id': spreadsheet_id,
    'worksheets': worksheets
  })

def worksheet(request, spreadsheet_id, worksheet_id):
  """Shows information about some worksheet in a spreadsheet."""
  ss = get_ss(request)
  ss.set_spreadsheet(spreadsheet_id)
  ss.set_worksheet(worksheet_id)
  rows = ss.get_rows()
  columns = rows[0].keys()
  return render_to_response('count/worksheet.html', {
    'columns' : columns,
    'rows'    : rows})

def count(request, spreadsheet_id, worksheet_id, column):
  """Runs word count analysis on the given column."""
  ss = get_ss(request)
  ss.set_spreadsheet(spreadsheet_id)
  ss.set_worksheet(worksheet_id)
  rows = ss.get_rows()
  a = Analyzer(rows)
  word_freqs = a.word_freq(column)
  return render_to_response('count/count.html', {
    'word_frequencies': word_freqs.items()
  })

def user(request):
  """Set up the Google account information for later access to Google Docs."""
  if request.method == 'POST': 
    form = UserForm(request.POST)
    if form.is_valid():
      request.session.__setitem__('ss',
          google_spreadsheets.Spreadsheets(
            form.cleaned_data['email'], form.cleaned_data['password']))
      return HttpResponseRedirect('/spreadsheets/')
  else:
    form = UserForm()

  return render_to_response('user.html', {
    'form': form,
  }, context_instance = RequestContext(request))


# Support

def get_ss(request):
  """Retreive the spreadsheet session object."""
  return request.session.__getitem__('ss')

class UserForm(forms.Form):
  email = forms.EmailField()
  password = forms.CharField( widget=forms.PasswordInput, label="Your Password" )

