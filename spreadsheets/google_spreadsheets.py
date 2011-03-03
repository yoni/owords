from xml.etree import ElementTree
import gdata.spreadsheet.service
import gdata.service
import atom.service
import gdata.spreadsheet
import atom
import getopt
import sys
import string

class Spreadsheets:
  """
  A wrapper for some simple operations on Google Docs Spreadsheets.
  See http://code.google.com/apis/spreadsheets/data/1.0/developers_guide_python.html for 
  a comprehensive Python developer's guide to using Google Data and Google Spreadsheets.
  """

  def __init__(self, email, password):
    self.gd_client = gdata.spreadsheet.service.SpreadsheetsService()
    self.gd_client.email = email
    self.gd_client.password = password
    self.gd_client.source = 'Spreadsheet Linguistic Analysis'
    self.gd_client.ProgrammaticLogin()
    self.curr_key = ''
    self.curr_wksht_id = ''
    self.list_feed = None
    
  def _PrintFeed(self, feed):
    """
    Prints out the feed, with separate handling for SpreadsheetsListFeed
    and other feeds.
    """
    for i, entry in enumerate(feed.entry):
      if isinstance(feed, gdata.spreadsheet.SpreadsheetsListFeed):
        print '%s %s %s' % (i, entry.title.text, entry.content.text)
        # Print this row's value for each column (the custom dictionary is
        # built using the gsx: elements in the entry.)
        print 'Contents:'
        for key in entry.custom:  
          print '  %s: %s' % (key, entry.custom[key].text) 
        print '\n',
      else:
        print '%s %s\n' % (i, entry.title.text)
        
  def get_rows(self):
    """Get all of the rows in the worksheet."""
    feed = self.get_worksheet_feed()
    rows = []
    for i, entry in enumerate(feed.entry):
      if isinstance(feed, gdata.spreadsheet.SpreadsheetsListFeed):
        # Print this row's value for each column (the custom dictionary is
        # built using the gsx: elements in the entry.)
        row = {}
        for key in entry.custom:  
          row[key] = entry.custom[key].text

        rows.append(row)
    return rows

  def get_worksheet_feed(self):
    """The current worksheet's feed"""
    return self.gd_client.GetListFeed(self.curr_key, self.curr_wksht_id)

  def spreadsheets(self):
    """Get the list of spreadsheets"""
    feed = self.gd_client.GetSpreadsheetsFeed()
    return feed

  def set_spreadsheet(self, index):
    """Select the spreadsheet to use, by index."""
    feed = self.gd_client.GetSpreadsheetsFeed()
    id_parts = feed.entry[int(index)].id.text.split('/')
    self.curr_key = id_parts[len(id_parts) - 1]
  
  def worksheets(self):
    """Get the list of worksheets in the current spreadsheet."""
    feed = self.gd_client.GetWorksheetsFeed(self.curr_key)
    return feed
    
  def set_worksheet(self, input):
    """
    Select the worksheet to use.
    To retrieve a list of worksheets, see worksheets.
    """
    feed = self.gd_client.GetWorksheetsFeed(self.curr_key)
    id_parts = feed.entry[int(input)].id.text.split('/')
    self.curr_wksht_id = id_parts[len(id_parts) - 1]

