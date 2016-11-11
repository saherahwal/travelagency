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
        # retrieve all blogs that are public
        #
        blogs = Blog.objects.filter( public = True ).extra( order_by=('-created',))
        
        #
        # Admin user gets all blogs
        #
        if request.user != None:
            if  request.user.is_superuser:
                blogs = Blog.objects.all( ).extra( order_by=('-created',))

        return render(request,
                      "blog.html",
                      { 'blogs': blogs } )

    else:

        try:

            #
            # Admin user gets his blog
            #
            if request.user != None:
                if  request.user.is_superuser:

                    blog = Blog.objects.get( id = blog_id )

                    return render(request,
                                  "blog_single.html",
                                  { 'blog' : blog  } )

            
            blog = Blog.objects.get( id = blog_id, public = True )
            return render(request,
                          "blog_single.html",
                          { 'blog' : blog  } )
            
        except ObjectDoesNotExist:

            #
            # TODO:
            # show 404 not found page
            #
            print "blog with id", blog_id, "doesn't exist or is not public"

            return render( request,
                           'error.html',
                           { })

        except Exception as e:

            #
            # TODO:
            # show 404 not found page
            #
            print "Exception thrown while get blog", e
            return render( request,
                           'error.html',
                           { })

