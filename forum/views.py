from django.shortcuts import render, get_object_or_404
from django.http import Http404

from .models import Board

# Create your views here.

def home(request):
    return render(request, 'home.html')

def forum(request):
    #Create variable to hold all board objects
    boards = Board.objects.all()
    return render(request, 'forum.html', {'boards':boards})

def forum_topics(request, pk):
    # Get board defined by primary key
    board = get_object_or_404(Board, pk=pk)
    return render(request, 'forum_topics.html', {'board': board})
