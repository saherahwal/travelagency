from django.shortcuts import render

def homepage(request):    
    return render( request , "index.html", {})

def hotels(request):    
    return render( request , "hotels.html", {})

def blog(request):    
    return render( request , "blog.html", {})

def activities(request):    
    return render( request , "activities.html", {})

def results(request):    
    return render( request , "results.html", {})
