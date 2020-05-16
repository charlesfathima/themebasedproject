from django.shortcuts import render, redirect
from .models import Destination
from .forms import ImageUploadForm
from accounts.models import CustomPreferences
from django.http import HttpResponse
from opencage.geocoder import OpenCageGeocode
from django.contrib import messages
from django.contrib.auth.models import User, auth
from textblob import TextBlob
# Create your views here.
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask_sqlalchemy import sqlalchemy
from sqlalchemy import create_engine

df=pd.DataFrame()

def get_title_from_index(index,df):
    return df[df.index==index].values[0]

def get_index_from_title(typeofplace,df):
    return df[df.typeofplace==typeofplace].index.values[0]

def get_name_from_index(index,df):
    return df[df.index==index]['name'].values[0]

def get_state_from_index(index,df):
    return df[df.index==index]['state'].values[0]

def get_city_from_index(index,df):
    return df[df.index==index]['city'].values[0]

def get_lattitude_from_name(name,df):
    print('dfffffdfffdddd',df)
    return df[df.name==name]['lat'].values[0]

def get_longitude_from_name(name,df):
    return df[df.name==name]['lon'].values[0]

def combine_features(row):
    return row['desc']+" "+row['state']+" "+row['typeofplace']

def destination(request,pk):
    imagePk = Destination.objects.get(pk=pk)
    df
    lattitude=get_lattitude_from_name(imagePk.name,df)
    longitude=get_longitude_from_name(imagePk.name,df)
    
    
    google_api_key='pk.eyJ1IjoiY2hhcmxlc2ZhdGhpbWEiLCJhIjoiY2thN3J4M2dsMDYxYzJzcGNhcHRramFtdyJ9.duQHBma3JxuJKji23dn2mw'
    return render(request,"destination.html",{'image_details':imagePk,'google_api_key':google_api_key,'lattitude':lattitude,'longitude':longitude})

def changepreferences(request):
    custom=CustomPreferences.objects.all()
    for c in custom:
        if str(c.user)==str(request.user):
            c.preferences=request.POST.get('preferences')
            c.save()
    return redirect("/")


def index(request):

    dests = Destination.objects.all()
    if request.user.is_authenticated:
        global df
        engine=create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/telusko')
        df_d=pd.read_sql_table("travello_destination",con=engine,schema='public',coerce_float=True,columns=[ 'name','img','desc','state','city','typeofplace'])
        df = pd.DataFrame(df_d)
        geocoder = OpenCageGeocode('ea7fd5e689b149c38ef13cbed352bff5') 
        list_lat = []
        list_long = []
        for index,row in df.iterrows():
            
           
            name=get_name_from_index(index,df)
            
            state=get_state_from_index(index,df) 
            city=get_city_from_index(index,df)    
            query = str(name)+','+str(city)+','+str(state)
            print("hi")
            results = geocoder.geocode(query)
            print('$$$$$$',results)
            if len(results) !=0:
                lat = results[0]['geometry']['lat']
                longi = results[0]['geometry']['lng']
            else:
                print("results is empty")
                
            print("hello",index,name,state)
            list_lat.append(lat)
            list_long.append(longi)
        df['lat']=list_lat
        df['lon']=list_long
        print(df)
        features=['desc','state','typeofplace']
        for feature in features:
            df[feature]=df[feature].fillna('')
    
        df['combined_features']=df.apply(combine_features,axis=1)
        cv=CountVectorizer()
        count_matrix=cv.fit_transform(df['combined_features'])
        cosine_sim=cosine_similarity(count_matrix)
        custom=CustomPreferences.objects.all()
        for c in custom:
            if str(c.user)==str(request.user):
                user_prefer=c.preferences 
                user_prefer=user_prefer.split(",") 
                rows_data=[]
                for up in user_prefer: 
                    place_index=get_index_from_title(up,df)
                    similar_places=list(enumerate(cosine_sim[place_index]))
                    sorted_similar_places=sorted(similar_places,key = lambda x:x[1], reverse=True)
                    i=0
                    for place in sorted_similar_places:
                        row_data=get_title_from_index(place[0],df)
                        rows_data.append(row_data)
                        i=i+1
                        if i>3:
                             break
                final_data=[]
                for dest in dests:
                    for lists in rows_data:
                        if dest.name in lists:
                            result=TextBlob(dest.desc)
                            polar=result.sentiment.polarity
                            if polar>0.0:
                                final_data.append(dest)

    else:
        user_prefer=[]
        final_data=[]
    
    
    return render(request, "index.html", {'dests': dests,'recommendations':final_data})

def search(request):
    if request.user.is_authenticated:
        try:
            state=request.GET.get('state')
            
            state=state.lower()
    
        except:
            state=None
    
        if state:
            context={'query':state}
            entry_list = Destination.objects.filter(state = state)
            
        else :
            context={}
        return render(request,'search.html',{'context': state,'lists':entry_list})

    else:
        return render(request,'login.html')


def upload(request):
    if request.method=='POST':
        form = ImageUploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            dest=Destination()
            dest.name=request.POST.get('nameofplace')
            dest.img=form.cleaned_data['image']
            dest.desc=request.POST.get('description')
            dest.city=request.POST.get('city')
            dest.state=request.POST.get('state')
            dest.typeofplace=request.POST.get('typeofplace')
            dest.save()
            dests=Destination.objects.all()
            return redirect("/")
            #return render(request,'index.html',{'dests':dests})

        else:
             return HttpResponse('invalid')

    else:
         return HttpResponse('only post allowed')
    
    