from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .forms import NewTopicForm
from .models import Board, Post, Topic

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

def new_topic(request, pk):
    # Get board defined by primary key
    board = get_object_or_404(Board, pk=pk)
    user = User.objects.first() # TODO: get current user instead

    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )        
            return redirect('forum_topics', pk=board.pk) # TODO: redirect to created topic
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board':board, 'form':form})
