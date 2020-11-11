import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "grader.settings")

application = get_wsgi_application()

from datetime import datetime

from django.db.models import Q, Count, Avg
from pytz import UTC

from .models import User, Blog, Topic


def create():
    # Создание

    user1 = User(first_name='u1', last_name='u1').save()
    user2 = User(first_name='u2', last_name='u2').save()
    user3 = User(first_name='u3', last_name='u3').save()

    user1 = User.objects.get(first_name='u1')
    user2 = User.objects.get(first_name='u2')
    user3 = User.objects.get(first_name='u3')

    blog1 = Blog(title='blog1', author=user1).save()
    blog2 = Blog(title='blog2', author=user1).save()

    blog1 = Blog.objects.get(title='blog1')
    blog2 = Blog.objects.get(title='blog2')

    blog1.subscribers.add(user1, user2)
    blog2.subscribers.add(user2)

    topic1 = Topic(title='topic1', blog=blog1, author=user1).save()
    topic2 = Topic(title='topic2_content', blog=blog1, author=user3, created=datetime(2017, 1, 1, tzinfo=UTC)).save()

    topic1 = Topic.objects.get(title='topic1')

    topic1.likes.add(user1, user2, user3)


def edit_all():
    # Редактирование

    users_set = User.objects.all()
    for user in users_set:
        user.first_name = 'uu1'
        user.save()


def edit_u1_u2():
    #  Редактирование

    users_set = User.objects.filter(first_name__in=['u1', 'u2'])
    for user in users_set:
        user.first_name = 'uu1'
        user.save()


def delete_u1():
    # Удаление

    user = User.objects.get(first_name='u1')
    user.delete()


def unsubscribe_u2_from_blogs():
    # Удаление

    user = User.objects.get(first_name='u2')
    user.subscriptions.clear()


def get_topic_created_grated():
    # Найти топики у которых дата создания больше 2018-01-01

    topics_set = Topic.objects.filter(created__gt=datetime(2018, 1, 1, tzinfo=UTC))
    return topics_set


def get_topic_title_ended():
    # Найти топик у которого title заканчивается на content

    topic_set = Topic.objects.filter(title__iendswith='content')
    return topic_set


def get_user_with_limit():
    # Получить 2х первых пользователей (сортировка в обратном порядке по id)

    user_set = User.objects.order_by('-id')[:2]
    return user_set


def get_topic_count():
    # Получить количество топиков в каждом блоге, назвать поле topic_count, отсортировать по topic_count по возрастанию

    result = Blog.objects.all().annotate(topic_count=Count('topic')).order_by('topic_count')
    return result


def get_avg_topic_count():
    # Получить среднее количество топиков в блоге

    result = Blog.objects.annotate(topic_count=Count('topic__blog')).aggregate(avg=Avg('topic_count'))
    return result


def get_blog_that_have_more_than_one_topic():
    # Найти блоги, в которых топиков больше одного

    result = Blog.objects.all().annotate(topic_count=Count('topic__blog')).filter(topic_count__gt=1)
    return result


def get_topic_by_u1():
    # Получить все топики автора с first_name u1

    result = Topic.objects.filter(author__first_name__exact='u1')
    return result


def get_user_that_dont_have_blog():
    # Найти пользователей, у которых нет блогов, отсортировать по возрастанию id

    result = User.objects.annotate(count=Count('blog')).filter(count=0).order_by('id')
    return result


def get_topic_that_like_all_users():
    # Найти топик, который лайкнули все пользователи

    result = Topic.objects.annotate(count=Count('likes')).filter(count=User.objects.aggregate(count=Count('id'))['count'])
    return result


def get_topic_that_dont_have_like():
    # Найти топики, у которы нет лайков

    result = Topic.objects.annotate(count=Count('likes')).filter(count=0)
    return result
