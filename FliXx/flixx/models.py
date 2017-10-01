from django.db import models

class Genre(models.Model):
    Name=models.CharField(max_length=100)
    n=models.IntegerField()
    def __str__(self):
        return self.Name
class movie(models.Model):
    #revenue,runtime,spoken_languages,status,tagline,title,vote_average,vote_count
    Budget=models.IntegerField()
    genres=models.ManyToManyField(Genre)
    url=models.URLField()
    title=models.CharField(max_length=200)
    overview=models.CharField(max_length=1000)
    dateofrelease=models.DateField()
    popularity=models.DecimalField(decimal_places=4,max_digits=100)
    revenue=models.IntegerField()
    runtime=models.IntegerField()
    status=models.CharField(max_length=30)
    tag=models.CharField(max_length=500)
    averagerating=models.DecimalField(decimal_places=1,max_digits=2)
    nutr=models.IntegerField()
    def __str__(self):
        return self.title+'\n'+str(self.dateofrelease)+'\n'+str(self.averagerating)
    def getData(self):
        g=[]
        for i in self.genres.all():
            g.append(i.n)
        return [self.Budget,self.dateofrelease.year,self.popularity,self.revenue,self.runtime,self.averagerating,self.nutr]
class user(models.Model):
    Username=models.CharField(max_length=10,unique=True)
    Name=models.CharField(max_length=100)
    Password=models.CharField(max_length=15)
    def __str__(self):
        return self.Name+'\n (@'+str(self.Username)+')'
class like(models.Model):
    user=models.ForeignKey(user)
    movie=models.ForeignKey(movie)
    l=models.IntegerField()
    def __str__(self):
        if self.l==1:
            return self.user.Name+" likes "+self.movie.title
        return self.user.Name + " dislikes " + self.movie.title
class review(models.Model):
    user=models.ForeignKey(user)
    movie=models.ForeignKey(movie)
    l=models.CharField(max_length=500)
    def __str__(self):
        return self.user.Name + " has "+str(self.l)+' to say about '+self.movie.title