#help convert model instance into python data type can be displayed JSON and XML
from rest_framework import serializers
from .models import MenuItem
from .models import Category
from decimal import Decimal #to convert price to decimal
#model serializer
'''
class MenuItemSerializer(serializers.ModelSerializer):
    stock = serializers.IntegerField(source='inventory') #source is the field name in the model
    price_after_tax = serializers.SerializerMethodField(method_name = 'calculate_tax') #to display price after tax
    class Meta:
        model = MenuItem
        #fields = ['id','title','price','inventory'] #display only these fields,delete any if necessary
        fields = ['id','title','price','stock','price_after_tax'] #you can change name from model here, but you need indicate source out of meta class
    def calculate_tax(self,product:MenuItem): 
        #product, which is an instance of the MenuItem model. 
        # he type hint MenuItem indicates that product is expected to be an instance of the MenuItem class
        return product.price * Decimal(1.1)
'''

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','slug','title'] 

#relational model serializer
class MenuItemSerializer(serializers.ModelSerializer):
#class MenuItemSerializer(serializers.HyperlinkedModelSerializer): # HyperlinkedModelSerializer display a category field as a hyperlink.
    stock = serializers.IntegerField(source='inventory') #source is the field name in the model
    price_after_tax = serializers.SerializerMethodField(method_name = 'calculate_tax') #to display price after tax
    #category = serializers.StringRelatedField() #to display category name instead of id
    category = CategorySerializer(read_only=True)  #this line will display all data in category table as Nested fields
    category_id = serializers.IntegerField(write_only=True) # this line will allow user to write category id, but not display it,remove parameter to see difference
    class Meta:
        model = MenuItem
        #fields = ['id','title','price','inventory'] #display only these fields,delete any if necessary
        fields = ['id','title','price','stock','price_after_tax','category','category_id'] #you can change name from model here, but you need indicate source out of meta class
        #depth = 1
        #Instead of declaring the category field as CategorySerializer() 
        #you can specify that depth=1 is in the Meta class in MenuItemSerializer. 
        #This way, all relationships in this serializer will display every field related to that model    

    def calculate_tax(self,product:MenuItem): 
        #product, which is an instance of the MenuItem model. 
        # he type hint MenuItem indicates that product is expected to be an instance of the MenuItem class
        return product.price * Decimal(1.1)

#general serializer 
class MenuItemSerializerView(serializers.Serializer): 
    # if we want display patial data, comment out any line that is not needed
    id = serializers.IntegerField(read_only=True) #auto generate id, read only is to prevent user to change i
    title = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=6, decimal_places=2)
    inventory = serializers.IntegerField()



from .models import Rating
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth.models import User

class RatingSerializer (serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
            queryset=User.objects.all(),
            default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Rating
        fields = ['user', 'menuitem_id', 'rating']

        validators = [
            UniqueTogetherValidator(
                queryset=Rating.objects.all(),
                fields=['user', 'menuitem_id']
            )
        ]

        extra_kwargs = {
            'rating': {'min_value': 0, 'max_value':5},
        }

