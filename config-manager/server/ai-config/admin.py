from django.contrib import admin
from ai-config.models import Config, Source, Destination, Process, InpuType, OutputType

# class CallAdmin(admin.ModelAdmin):
#     list_display = ('ucid', 'state', 'isContactCenterCall', 'history', 'end', 'origin')
#     list_filter = ('end', 'state','current_agent')

# class ErrorInline(admin.TabularInline):
#     model = Error.pdf.through
    
# class SolutionInline(admin.TabularInline):
#     model = Solution


# class PDFAdmin(admin.ModelAdmin):
#     list_display = ('name', 'lastmod')
#     list_filter = ('lastmod','profil')
#     inlines = [
#         ErrorInline,
#     ]

# class ErrorAdmin(admin.ModelAdmin):
#     list_display = ('name', 'page')
#     list_filter = ('page',)
#     inlines = [
#         SolutionInline,
#     ]


#admin.site.register(Call, CallAdmin)
#admin.site.register(Agent, AgentAdmin)
# admin.site.register(Input, PDFAdmin)
# admin.site.register(Error, ErrorAdmin)
admin.site.register(Config)
admin.site.register(Source)

admin.site.register(Destination)
admin.site.register(Process)

admin.site.register(InpuType)
admin.site.register(OutputType)
