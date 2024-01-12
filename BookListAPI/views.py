from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view #function based view
from rest_framework.views import APIView #class based view
from django.core.paginator import Paginator,EmptyPage#Pagination


# @api_view() # view decorator wrap message
@api_view(['GET','POST']) # add any function you should support
def books(request):
    return Response({"List of the books"},status=status.HTTP_200_OK)


class BookList(APIView):
	def get(self, request):
        #return Response({"Message": "List of the books"},status=status.HTTP_200_OK)
		author = request.GET.get('author')
		if (author):
			return Response({"Message": "List of the books by " + author},status=status.HTTP_200_OK)
			
		return Response({"Message": "List of the books"},status=status.HTTP_200_OK)
	def post(self, request):
		return Response({"title": request.data.get('title')},status=status.HTTP_201_CREATED)


class Book(APIView):
	def get(self, request,pk):
		return Response({"Message": "single book with id " + str(pk)},status=status.HTTP_200_OK)
	def post(self, request,pk):
		return Response({"title": request.data.get('title')},status=status.HTTP_200_OK)



#MenuItem serializer, eaiser and convinience way 
from .serializers import MenuItemSerializerView
from .serializers import MenuItemSerializer #add serializer
from .models import MenuItem
from rest_framework import generics

class MenuItemView(generics.ListCreateAPIView):
	queryset = MenuItem.objects.all() #retrevie all data from model
	serializer_class = MenuItemSerializerView #display and store record properly

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
#class SingleMenuItemView(generics.RetrieveUpdateAPIView,generics.DestroyAPIView): #use this to retrieve and update single record only
#class SingleMenuItemView(generics.RetrieveAPIView): #use this to retrieve single record only
#class SingleMenuItemView(generics.DestroyAPIView): #use this to delete single record only
#class SingleMenuItemView(generics.UpdateAPIView): #use this to update single record only
#class SingleMenuItemView(generics.CreateAPIView): #use this to create single record only
#class SingleMenuItemView(generics.RetrieveAPIView,generics.UpdateAPIView,generics.DestroyAPIView): #use this to retrieve,update and delete single record only
	queryset = MenuItem.objects.all() #retrevie all data from model
	serializer_class = MenuItemSerializerView #display and store record properly


#Function based view serializer
from django.shortcuts import get_object_or_404 #friendly error message
from decimal import Decimal
@api_view(['GET','POST'])
def menu_items(request):
	#items = MenuItem.objects.all()
	if request.method == 'GET':
		items = MenuItem.objects.select_related('category').all() 
		#select_related is used to retrieve related data from another table, in this case, category table
		#In this case, when you are converting a connected model to string,
		#you also need to change your view files to load the related model in a single SQL code. This will make your API more efficient by
		#not running a separate SQL query for every item to load to the relative data.
		
		#filter, search, ordering
		#-------------------
		#http://127.0.0.1:8000/api/menu-items-view/?category=default
		category_name = request.query_params.get('category')
		to_price = request.query_params.get('to_price')#test example: http://127.0.0.1:8000/api/menu-items-view/?to_price=3
		search = request.query_params.get('search')

		ordering = request.query_params.get('ordering')

		perpage = request.query_params.get('perpage',default=2)#test example http://127.0.0.1:8000/api/menu-items-view/?perpage=3&page=1
		page = request.query_params.get('page',default=1)
		#if category item present , filter the items
		if category_name:  
			items = items.filter(category__title=category_name)#You need to use a double underscore between the model and the field to filter a linked model like a category inside the menu item.
		if to_price:  
			items = items.filter(price__lte=to_price) #This is a conditional operator or fields lookup and the price double underscore lte means price is less than or equal to a value. 
		if search:
			items = items.filter(title__icontains=search) #icontains is case insensitive, iexact is case sensitive
			#items = items.filter(title__startswith=search) #startswith is case sensitive
		if ordering:  
			ordering_fields = ordering.split(',')
			items = items.order_by(*ordering_fields) #order_by is used to sort the items by a specific field.
			#http://127.0.0.1:8000/api/menu-items-view/?ordering=-price
			#http://127.0.0.1:8000/api/menu-items-view/?ordering=price,inventory
		#----------------------

		paginator = Paginator(items,per_page=perpage)
		try:
			items = paginator.page(number = page)
		except EmptyPage:
			#items = paginator.page(paginator.num_pages) #if page is not found, return last page
			items = []
		#many=True is essential when you are converting a list to JSON data 
		serialized_item = MenuItemSerializer(items, many=True)  
		return Response(serialized_item.data)
	if request.method == 'POST':
		serialized_item = MenuItemSerializer(data=request.data) 
		serialized_item.is_valid(raise_exception=True)
		serialized_item.save()
		return Response(serialized_item.data,status=status.HTTP_201_CREATED)
@api_view()
def single_item(request, pk):
    #item = MenuItem.objects.get(pk=pk)
	#get_object_or_404 is a shortcut function that returns a 404 error if the object is not found.
	item = get_object_or_404(MenuItem, pk=pk)  
	serialized_item = MenuItemSerializer(item) 
	return Response(serialized_item.data)


from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

# only authenticated user can access this class	
@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
	return Response({"message": "This is a secret message"},status=status.HTTP_200_OK)


@api_view()
@permission_classes([IsAuthenticated])
def me(request):
	return Response(request.user.email)	

# manager group view, only user in manager group can access this class
@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
	if request.user.groups.filter(name='Manager').exists():#if user in manager group
		return Response({"message": "only manage see this"})
	else:
		return Response({"message": "you are  not authorized"},403)


# throttling, call n times API per min
#AnonRateThrottle is a class that implements the rate limiting for anonymous users.
from rest_framework.throttling import AnonRateThrottle 
from rest_framework.throttling import UserRateThrottle 
from rest_framework.decorators import throttle_classes
from .throttles import  TenCallsPerMinute # import file
@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(request):
	return Response({"message": "Successful"},status=status.HTTP_200_OK)

@api_view()
@permission_classes([IsAuthenticated])
#@throttle_classes([UserRateThrottle])
@throttle_classes([TenCallsPerMinute])
def throttle_check_auth(request):
	return Response({"message": "message for the logged user only"},status=status.HTTP_200_OK)

# Djoser manager Group view

from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import Group,User
@api_view(['POST','DELETE']) # ADD DELETE
@permission_classes([IsAdminUser])
def manager(request):
	username = request.data['username']
	if username:
		user = get_object_or_404(User,username=username)
		manager = Group.objects.get(name='Manager')
		if request.method == 'POST':
			manager.user_set.add(user)
		elif request.method == 'DELETE':
			manager.user_set.remove(user)
		return Response({"message":"manager action post/delete performed "})
	return Response({"message":"error"},status=status.HTTP_400_BAD_REQUEST)

# food rating project 
from .models import Rating
from .serializers import RatingSerializer
class RatingsView(generics.ListCreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def get_permissions(self):
        if(self.request.method=='GET'):
            return []

        return [IsAuthenticated()]


#render
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.decorators import api_view, renderer_classes
#https://www.coursera.org/learn/apis/supplement/57qRB/different-types-of-renderers

#Display a related model fields field as a hyperlink 
'''
from .models import Category 
from .serializers import CategorySerializer
@api_view()
def category_detail(request, pk):
	category = get_object_or_404(Category,pk=pk)
	serialized_category = CategorySerializer(category)
	return Response(serialized_category.data) 
'''

