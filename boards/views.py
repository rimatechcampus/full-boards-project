from django.shortcuts import render, get_object_or_404, redirect
from .models import Board, Topic, Post
from django.contrib.auth.models import User
from .forms import NewTopicForm, PostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import UpdateView, ListView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


# def home(request):
#     boards = Board.objects.all()
#     context = {
#         'boards': boards
#     }
#     return render(request, 'home.html', context)


class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'home.html'


def boards_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    queryset = board.topics.order_by(
        '-created_dt').annotate(comments=Count('posts'))
    # * paginator
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 20)
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        # fallback to the first page
        topics = paginator.page(1)
    except EmptyPage:
        # probably the user tried to add a page number
        # in the url, so we fallback to the last page
        topics = paginator.page(paginator.num_pages)

    return render(request, 'boards_topic.html', {'board': board, 'topics': topics})


@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    # user = User.objects.first()      # get the first nmme of user

    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.created_by = request.user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('boards_topic', pk=board.pk)

    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})


def topic_posts(request, pk, topic_id):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_id)

    session_key = 'view_topic_{}'.format(topic.pk)
    if not request.session.get(session_key, False):
        topic.views += 1
        topic.save()
        request.session[session_key] = True
    return render(request, 'topic_posts.html', {'topic': topic})


@login_required
def topic_reply(request,  pk, topic_id):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            topic.updated_by = request.user
            topic.updated_dt = timezone.now()
            topic.save()
            return redirect('topic_posts', pk=pk, topic_id=topic.pk)
    else:
        form = PostForm()
    return render(request, 'topic_reply.html', {'topic': topic, 'form': form})

# ! class genetic cbg


@method_decorator(login_required, name="dispatch")
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message',)
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_dt = timezone.now()
        post.save()
        return redirect('topic_posts', pk=post.topic.board.pk, topic_id=post.topic.pk)
