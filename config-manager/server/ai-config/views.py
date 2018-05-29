from django.shortcuts import render
from pdfapp.models import PDF, Error
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta

def pdfs(request):
    print ("RENDERING ")
    
    filterdate = datetime.now() - timedelta(days=6)
    
    data = PDF.objects.filter(lastDetectedChange__gte=filterdate).order_by('-lastDetectedChange')
    return render(request, 'ai-config/index.html', {'DATA': data})

