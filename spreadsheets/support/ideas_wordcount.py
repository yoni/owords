import google_spreadsheet_wordcounts
from csv_wordcount_analyzer import Analyzer

crud.set_spreadsheet('23') # TODO: pass a spreadsheet name instead
crud.set_worksheet('0')
rows = crud.get_rows()
a = Analyzer(rows)
top_words = a.top_words('skillzwantedneeded',10)
print top_words
