from django.shortcuts import render
from flixx.forms import  SignUp
from flixx.forms import  LogIn,reviewing
from flixx.models import user,movie,Genre,like,review
from django.http import HttpResponse
import numpy
import random
from sklearn.tree import DecisionTreeClassifier
movies=movie.objects.all()
def home(request):
    message=''
    url='/FliXx/'
    a="LogIn"
    us=user()
    if 'Username' in request.session:
        a="LogOut"
        for i in user.objects.all():
            if i.Username==request.session['Username']:
                us=i
                break
    if request.method=="POST":
        form=SignUp(request.POST,request.FILES)
        if form.is_valid()==True:
            n=user()
            n.Username=form.cleaned_data['Username']
            n.Name=form.cleaned_data['Name']
            n.Password=form.cleaned_data['Password']
            n.save()
            return login(request)
        else:
            message="Something went wrong, Please fill the form again ."
            form = SignUp()
            return render(request, 'flixx/home.html', {'user':us,'movies':movie.objects.order_by('-dateofrelease')[:20],'s':a,'url':url,'message':message,'form': form,'action':"SignUp"})
    else:
        form=SignUp()
        return render(request,'flixx/home.html',{'user':us,'movies':movie.objects.order_by('-dateofrelease')[:20],'s':a,'message':message,'url':url,'form':form,'action':"SignUp"})
# Create your views here.
def login(request):
    message="Welcome back, please fill your credential ."
    url = '/FliXx/login/'
    a = "LogIn"

    us=user()
    if 'Username' in request.session:
        del request.session['Username']
        return home(request)
    else:
        if request.method=="POST":
            form = LogIn(request.POST,request.FILES)
            if form.is_valid():
                us=user.objects.all()
                un=form.cleaned_data['Username']
                p=form.cleaned_data['Password']
                for i in us:
                    if i.Username==un:
                        if i.Password==p:
                            request.session['Username']=un
                            us=i
                            a='LogOut'
                            message="Successful login. Welcome to FliXx "+str(i)+"."
                            return render(request, 'flixx/home.html',{'user':us,'movies':movie.objects.order_by('-dateofrelease')[:20],'s':a,'message': message, 'url': url, 'form': form, 'action': "LogIn"})
                            break
                else:
                    message="Your Credentials did not match any existing user please try again."
                    return render(request, 'flixx/login.html',{'s':a,'message': message, 'url': url, 'form': form, 'action': "LogIn"})
            else:
                message = "Your messed up please try again."
                return render(request, 'flixx/login.html',{'s':a,'message': message, 'url': url, 'form': form, 'action': "LogIn"})

        else:
            form = LogIn()
            return render(request,'flixx/login.html',{'s':a,'message':message,'url':url,'form':form,'action':"LogIn"})
def detailedview(request ,id):
    m=movie()
    message=''
    a = "LogIn"
    re=[]
    form=''
    reviewed = False
    l='/FliXx/'+str(id)
    if request.method=="POST":
        form=reviewing(request.POST,request.FILES)
        if form.is_valid():
            s=form.cleaned_data['review']
            rew=review()
            rew.l=s
            rew.user=user.objects.get(Username=request.session['Username'])
            rew.movie=movie.objects.get(id=id)
            rew.save()
            return detailedview(request,id)
    if 'Username' in request.session:
        a = 'LogOut'

        re=review.objects.filter(movie=movie.objects.get(id=id))
        for i in re:
            if i.user==user.objects.get(Username=request.session['Username']):
                reviewed=True
                break
        else:
            form=reviewing()
    for i in movies:
        if int(id)==int(i.id):
            s=set()
            g=[]
            for j in i.genres.all():
                if j.Name not in s:
                    if j not in g:
                        g.append(j)
            print (form)
            return render(request, 'flixx/Detailedview.html', {'reviewed':reviewed,'url':l,'action':'review','form':form,'reviews':re,'g':g,'s':a,'movie': i, 'message': message})
    message = "Your Credentials did not match any existing movie data please try again."

    form = SignUp()
    url = '/FliXx/login/'

    return render(request, 'flixx/login.html',
                  {'s': a, 'message': message, 'url': url, 'form': form, 'action': "LogIn"})
def lik(request,mi,uid):
    j=like()
    if int(uid)==0 or int(uid)==1:
        if "Username" in request.session:
            j.l=int(uid)
            j.movie=movie.objects.get(id=int(mi))
            j.user=user.objects.get(Username=str(request.session['Username']))
            try:
                try:
                    q=like.objects.get(user=j.user,movie=j.movie)
                    print(q)
                    q.delete()
                    j.save()
                    return detailedview(request,mi)
                except DoesNotExist:
                    j.save()
                    return detailedview(request,mi)
            except NameError:
                j.save()
                return detailedview(request,mi)
        return login(request)
    return detailedview(request,mi)
def recommend(request):
    if 'Username' not in request.session:
        return login(request)
    state='LogOut'
    us=request.session['Username']
    m='Hey '+str(user.objects.get(Username=str(us)))+' Here are some movies we recommend based on your likes and dislikes  .'
    print(m)
    x=[]
    Y=[]
    for i in like.objects.filter(user=user.objects.get(Username=us)):
        x.append(i.movie)
        Y.append(i.l)
    x1=[i.getData() for i in x]
    X=[]
    for i in x1:
        t=numpy.asarray(i,dtype=float)
        X.append(t)
    print (len(X))
    Y=numpy.asarray(Y,dtype=float)
    c = DecisionTreeClassifier()
    c.fit(X, Y)
    T=[]
    t=[]
    for i in movie.objects.all():
        if i not in x:
            T.append(numpy.asarray(i.getData()))
            t.append(i)
    L=c.predict(T)
    print (len(movie.objects.all()))
    li=[]
    print(len(T))
    for i in range(len(T)):
        if L[i]==1:
            li.append(t[i])
    print (len([i for i in L if i ==0]))
    random.shuffle(li)
    li.reverse()
    return render(request, 'flixx/recommendations.html', {'s':state,'message': m, 'li': li[:20]})



def watchedmovies(request):
    if 'Username' not in request.session:
        return login(request)
    state='LogOut'
    us=request.session['Username']
    m=''
    try:
        try:
            l=like.objects.get(user=user.objects.get(Username=str(us))).order_by('id')
        except dfsa:
            asd
    except NameError:
        m="Please Like/Dislike some more movies ."
    li=[]
    di=[]
    X=[]
    Y=[]
    for i in like.objects.filter(user=user.objects.get(Username=us)):
        X.append(i.movie)
        Y.append(i.l)
        if i.l==0:
            di.append(i.movie)
        else:
            li.append(i.movie)
    print(li)
    print(di)
    return render(request,'flixx/watchedmovies.html' ,{'s':state,'message':m,'li':li,'di':di})
def about_us(request):
    a='LogIn'
    message=''
    if 'Username' in request.session:
        a='LogOut'
        message='Hey '+str(user.objects.get(Username=request.session['Username']))
    return render(request,'flixx/about us.html',{'s':a,'message':message})
