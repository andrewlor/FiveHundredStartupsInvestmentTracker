from django.db import models

# Create your models here.
class Entry(models.Model):
	date = models.DateField()
	amount = models.FloatField(default=0)
	company = models.ForeignKey('Company')
	TYPE = models.CharField(max_length=100)
	notes = models.TextField()

	def __str__(self):
		return self.company.__str__() + ", " + self.TYPE + ", " + self.date.__str__() + ", " + str(self.amount)

class Company(models.Model):
	name = models.CharField(max_length=100)
	
	def __str__(self):
		return self.name

class Vote(models.Model):
	yes_or_no = models.CharField(max_length=3)
	person = models.ForeignKey('Person')
	company = models.ForeignKey('Company')
	

	def __str__(self):
		return self.yes_or_no

class Person(models.Model):
	name = models.CharField(max_length=100)
	invested = models.FloatField(default=0)
	nav = models.FloatField(default=0)
	tvpi = models.FloatField(default=0)
	xirr = models.FloatField(default=0)
	anti_invested = models.FloatField(default=0)
	anti_nav = models.FloatField(default=0)
	anti_tvpi = models.FloatField(default=0)
	anti_xirr = models.FloatField(default=0)


	def __str__(self):
		return self.name

class Password(models.Model):
	password = models.CharField(max_length=100)

	def __str__(self):
		return self.password



