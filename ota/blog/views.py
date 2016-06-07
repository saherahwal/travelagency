from django.shortcuts import render
from blog.models import *
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

# Create your views here.

def main(request):
    """
        view of all blogs
    """

    blog_id = request.GET.get('id')

    if blog_id == None:
        
        #
        # retrieve all blogs
        #
        blogs = Blog.objects.all()        

        return render(request,
                      "blog.html",
                      { 'blogs': blogs } )

    else:

        try:
            
            blog = Blog.objects.get( id = blog_id )

            return render(request,
                          "blog_single.html",
                          { 'blog' : blog  } )
            
        except ObjectDoesNotExist:

            #
            # TODO:
            # show 404 not found page
            #
            print "blog with id", blog_id, "doesn't exist"

        except Exception as e:

            #
            # TODO:
            # show 404 not found page
            #
            print "Exception thrown while get blog", e
        
        
        
    
