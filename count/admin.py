from count.models import Poll, Choice
from django.contrib import admin

class ChoiceInline(admin.TabularInline):
  model = Choice
  extra = 3

class PollAdmin(admin.ModelAdmin):
  fields = ['pub_date', 'question']
  inlines = [ChoiceInline]
  list_display = ('question', 'pub_date', 'was_published_today')
  list_filter = ['pub_date']
  search_fields = ['question']
  date_hierarchy = 'pub_date'
  
admin.site.register(Poll, PollAdmin)
