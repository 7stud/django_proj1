from django.contrib import admin
from pollsapp.models import Poll
from pollsapp.models import Choice

# Register your models here.
#admin.site.register(Poll)

class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3

class PollAppAdmin(admin.ModelAdmin):
    #fields = ['pub_date', 'question']
    fieldsets = [
        (None, {'fields': ["question"]}),
        ('Date Info', {'fields': ['pub_date'], 
                       'classes': ['collapse']
                      }
        ),
    ]

    #List the choices in the poll admin page:
    inlines = [ChoiceInLine]
    list_display = ('question', 'pub_date', 'was_published_recently')
    #Add a sidebar for searching polls(what you see depends
    #on field type):
    list_filter = ['pub_date']
    #Add search box, which will search the specified column:
    search_fields = ['question']

admin.site.register(Poll, PollAppAdmin)
#Don't have a separate page for choices(comment out the following):
#admin.site.register(Choice)





