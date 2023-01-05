from django.db import models
from datetime import datetime,timedelta
import uuid

class Students(models.Model):
    roll_number = models.CharField(max_length=100,unique=True)
    fullname = models.CharField(max_length=100)
    program = models.CharField(max_length=100)
    Email=models.EmailField(max_length=100)
    def _str_(self):
        return self.fullname

class Book(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,help_text="Book unique id across the Library")
    book = models.ForeignKey('Book', on_delete=models.CASCADE, null=True)
    book_genre = models.CharField(max_length=100,unique=True)
    # Is_borrowed = models.BooleanField(default=False)
    def _str_(self):
        return f"{self.id} {self.book}"

class BookName(models.Model):
    book_title = models.CharField(max_length=200)
    book_author = models.CharField(max_length=100)
    book_ISBN = models.PositiveIntegerField()
    # summary=models.TextField(max_length=500, help_text="Summary about the book",null=True,blank=True)
    def _str_(self):
        return self.book_title

class Condition (models.Model):
    book_Condition = models.CharField(max_length=20)

class Fine(models.Model):
    fine = models.IntegerField()

def calculate_fine(self):
    if not self.return_date:
        return 0
    due_date = self.due_date
    return_date = self.return_date
    if return_date > due_date:
        fine_amount = (return_date - due_date).days *  10 #self.fine_per_day
        return fine_amount
    else:
        return 0

def save(self, *args, **kwargs):
    self.fine = self.calculate_fine()
    super(Book, self).save(*args, **kwargs)

def get_returndate():
    return datetime.today() + timedelta(days=16)

class Book_Issue(models.Model):
    student = models.ForeignKey('Students', on_delete=models.CASCADE)
    book_Name = models.ForeignKey('BookName', on_delete=models.CASCADE)
    issue_date = models.DateTimeField(auto_now=True, help_text="Date the book is issued")
    due_date = models.DateTimeField(default=get_returndate(), help_text="Date the book is due to")
    return_date = models.DateField(null=True, blank=True, help_text="Date the book is returned")
    # remarks_on_issue = models.CharField(max_length=100, default="Book in good condition", help_text="Book remarks/condition during issue")
    # remarks_on_return = models.CharField(max_length=100, default="Book in good condition", help_text="Book remarks/condition during return")
    def _str_(self):
        return self.student.fullname + " borrowed " + self.BookName.book_title
