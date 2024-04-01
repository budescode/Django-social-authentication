import os
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
import requests
from django.contrib.auth.models import User
from django.http import HttpResponse



def signin_view(request):
    FACEBOOK_APP_ID = os.environ["FACEBOOK_APP_ID"]
    FACEBOOK_SECRET = os.environ["FACEBOOK_SECRET"]
    FACEBOOK_REDIRECT_URL = os.environ["FACEBOOK_REDIRECT_URL"]
    LINKEDIN_CLIENT_ID = os.environ["LINKEDIN_CLIENT_ID"]
    LINKEDIN_REDIRECT_URL = os.environ["LINKEDIN_REDIRECT_URL"]
    GITHUB_CLIENT_ID = os.environ["GITHUB_CLIENT_ID"]
    GOOGLE_REDIRECT_URL = os.environ["GOOGLE_REDIRECT_URL"]
    GOOGLE_CLIENT_ID = os.environ["GOOGLE_CLIENT_ID"]
    context = {
        "GOOGLE_CLIENT_ID":GOOGLE_CLIENT_ID,
        "GOOGLE_REDIRECT_URL":GOOGLE_REDIRECT_URL,
        "GITHUB_CLIENT_ID":GITHUB_CLIENT_ID, "LINKEDIN_CLIENT_ID":LINKEDIN_CLIENT_ID, "LINKEDIN_REDIRECT_URL":LINKEDIN_REDIRECT_URL, "FACEBOOK_APP_ID":FACEBOOK_APP_ID, "FACEBOOK_SECRET":FACEBOOK_SECRET, "FACEBOOK_REDIRECT_URL":FACEBOOK_REDIRECT_URL}
    return render(request, 'signin.html', context)

def google_signin(request):
    access_token = request.GET.get("access_token")
    if access_token:       
        headers1 = {
        'Content-Type': 'application/json',
        'Connection': 'Keep-Alive',
        'Authorization': f'Bearer {access_token}',
        }        
        url='https://people.googleapis.com/v1/people/me?personFields=emailAddresses,names,photos' 
        resp = requests.get(url,headers=headers1) 
        data = resp.json()
        status_code = resp.status_code
        if status_code <400:
            familyName = data['names'][0]['familyName']
            givenName = data['names'][0]['givenName']
            email = data['emailAddresses'][0]['value']
            photo = data['photos'][0]['url']
            user, created = User.objects.get_or_create(email=email, username=email, defaults={'first_name': familyName, 'last_name': givenName})      
            login(request, user)     
            return redirect("/")            
        else:            
            return HttpResponse("error")
    return render(request, 'google_signin.html')

def github_signin(request):
    GITHUB_CLIENT_ID = os.environ['GITHUB_CLIENT_ID']
    GITHUB_CLIENT_SECRET = os.environ['GITHUB_CLIENT_SECRET']
    code = request.GET.get("code")
    url = 'https://github.com/login/oauth/access_token'
    headers1 = {        
        'Accept': 'application/json'
    }
    body = {"client_id":GITHUB_CLIENT_ID, "client_secret":GITHUB_CLIENT_SECRET, "code":code, "accept":"json"}
    resp = requests.post(url, json=body, headers=headers1)  
    status_code = resp.status_code
    data = resp.json()
    if status_code <400:       
        if 'error' in data.keys():            
            error = data['error_description']
            return HttpResponse(error) 
        access_token = data['access_token']        
        headers1 = {        
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}',
        } 
        url = 'https://api.github.com/user'        
        resp = requests.get(url,headers=headers1) 
        data = resp.json()
        
        email = data['email']
        name = data['name']
        firstname, lastname = name.split(' ', 1)
        avatar_url = data['avatar_url']   
        user, created = User.objects.get_or_create(email=email, username=email, defaults={'first_name': firstname, 'last_name': lastname})      
        login(request, user)     
        return redirect("/")     
    else:
        error = data['error_description']
        return HttpResponse(error)   

def linked_in_oauth(request):
    code = request.GET.get("code")
    headers1 = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'Keep-Alive'
    }    
    LINKEDIN_CLIENT_ID=os.environ["LINKEDIN_CLIENT_ID"]
    LINKEDIN_CLIENT_SECRET=os.environ["LINKEDIN_CLIENT_SECRET"]
    LINKEDIN_REDIRECT_URL=os.environ["LINKEDIN_REDIRECT_URL"]
    #############################get access token #########################
    body = {'grant_type':'authorization_code', 'client_secret':LINKEDIN_CLIENT_SECRET, 'client_id':LINKEDIN_CLIENT_ID, 'code':code, 'redirect_uri':LINKEDIN_REDIRECT_URL}
    resp = requests.post("https://www.linkedin.com/oauth/v2/accessToken", data=body, headers=headers1)        
    data = resp.json()
    status_code = resp.status_code
    if status_code <400:
        #############################get user info#########################
        token = data['access_token']
        headers1 = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'Keep-Alive',
        'Authorization': f'Bearer {token}',
        }       
        resp = requests.get("https://api.linkedin.com/v2/userinfo",headers=headers1) 
        data = resp.json()
        status_code = resp.status_code
        if status_code <400:
            name = data['name']
            given_name = data['given_name']
            family_name = data['family_name']
            email = data['email']
            picture = data['picture']
            user, created = User.objects.get_or_create(email=email, username=email, defaults={'first_name': family_name, 'last_name': given_name})      
            login(request, user)     
            return redirect("/")  
        else:
            return HttpResponse("error")
    else:
        return HttpResponse("error")
    
def facebook_signin(request):
    code = request.GET.get("code")
    appId= os.environ['FACEBOOK_APP_ID']
    appSecret = os.environ['FACEBOOK_SECRET']
    redirect_uri = os.environ['FACEBOOK_REDIRECT_URL']
    http_headers = {        
        'Content-Type': 'application/json',
    } 
    url = f'https://graph.facebook.com/v19.0/oauth/access_token?client_id={appId}&redirect_uri={redirect_uri}&client_secret={appSecret}&code={code}'
    resp = requests.get(url,headers=http_headers)    
    data = resp.json()    
    access_token = data['access_token']

    #get user id with access token
    url = f'https://graph.facebook.com/me?access_token={access_token}'
    resp = requests.get(url,headers=http_headers)     
    data = resp.json()
    id = data['id']
    
    #get user details with id and access token
    url = f'https://graph.facebook.com/{id}?fields=id,name,email,picture&access_token={access_token}'
    resp = requests.get(url,headers=http_headers)     
    data = resp.json()
        
    id = data['id']
    name = data['name']
    firstname, lastname = name.split(' ', 1)
    email = data['email']
    picture = data['picture']['data']['url']    
    user, created = User.objects.get_or_create(email=email, username=email, defaults={'first_name': firstname, 'last_name': lastname})      
    login(request, user)     
    return redirect("/")

def logout_view(request):
    logout(request)
    return redirect('/')