import string

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django import forms
from django.template import RequestContext

from xml.etree import ElementTree
import gdata.spreadsheet.service
import gdata.service
import gdata.spreadsheet

import google_spreadsheets
from wordcount import Analyzer

def spreadsheets(request):
  """Lists all of the spreadsheets."""
  ss = get_google_spreadsheets(request)
  
  spreadsheets = []
  for i, entry in enumerate(ss.spreadsheets().entry):
    spreadsheets.append({
      'id':i,
      'title':entry.title.text
    })

  return render_to_response(
    'spreadsheets/spreadsheets.html',
    {'spreadsheets': spreadsheets
  })

def spreadsheet(request, spreadsheet_id):
  """Shows information about a specific spreadsheet."""
  ss = get_google_spreadsheets(request)
  ss.set_spreadsheet(spreadsheet_id)

  worksheets = []
  for i, entry in enumerate(ss.worksheets().entry):
    worksheets.append({'id' : i, 'title' : entry.title.text})

  return render_to_response(
    'spreadsheets/worksheets.html',
    {
      'spreadsheet_id': spreadsheet_id,
      'worksheets': worksheets
  })

def worksheet(request, spreadsheet_id, worksheet_id):
  """Shows information about some worksheet in a spreadsheet."""
  ss = get_google_spreadsheets(request)
  ss.set_spreadsheet(spreadsheet_id)
  ss.set_worksheet(worksheet_id)
  rows = ss.get_rows()
  columns = rows[0].keys()
  return render_to_response('spreadsheets/worksheet.html', {
    'columns' : columns,
    'spreadsheet_id':spreadsheet_id,
    'worksheet_id':worksheet_id
  })

def count(request, spreadsheet_id, worksheet_id, column):
  """Runs word count analysis on the given column."""
  ss = get_google_spreadsheets(request)
  ss.set_spreadsheet(spreadsheet_id)
  ss.set_worksheet(worksheet_id)
  rows = ss.get_rows()
  a = Analyzer(rows)
  word_freqs = a.word_freq(column)
  return render_to_response('spreadsheets/count.html', {
    'spreadsheet_id': spreadsheet_id,
    'word_frequencies': word_freqs.items(),
    'worksheet_id':worksheet_id
  })

def login(request):
  """Set up the Google account information for access to Google Docs."""

  class LoginForm(forms.Form):
    """Form for basic username/password login with Google Docs."""
    email = forms.EmailField()
    password = forms.CharField( widget=forms.PasswordInput, label="Your Password" )

  if request.method == 'POST': 
    form = LoginForm(request.POST)
    if form.is_valid():
      google_spreadsheets_session = google_spreadsheets.Spreadsheets(
            form.cleaned_data['email'], form.cleaned_data['password'])
      request.session.__setitem__('google_spreadsheets_session',
          google_spreadsheets_session)
      return HttpResponseRedirect('/spreadsheets/')
  else:
    form = LoginForm()

  return render_to_response('user.html', {
    'form': form,
  }, context_instance = RequestContext(request))

def get_google_spreadsheets(request):
  """
  Retreive the spreadsheets session attribute,
  which represents the user's Google Spreadsheets session.
  """
  return request.session.__getitem__('google_spreadsheets_session')
