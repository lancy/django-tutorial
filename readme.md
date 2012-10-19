# Django 建站入门简明教程
创建一个简单的投票网站 by lancy
[See Original](https://docs.djangoproject.com/en/1.4/intro/tutorial01/)
## Step 1 安装Django
	$ sudo pip install django
测试

	$ python
	>>> import django
	>>> django.get_version()
	'1.4.1'
	
## Step 2 创建工程
	$ django-admin.py startproject mysite
运行测试
	
	$ python manage.py runserver
	
浏览器测试 http://127.0.0.1:8000	

##### Note:	 可以改变端口
	python manage.py runserver 0.0.0.0:8000
### 数据库设置
Edit mysite/setting.py

	DATABASES = {
	    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'test.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    	}
	}
	
	TIME_ZONE = 'Asia/Shanghai'
	LANGUAGE_CODE = 'en-US'
	
然后同步数据库，第一次新建数据库时，会要求生成superuser

	$ python manage.py syncdb
	
##### Note:无法创建superuser的错误
it is because your environment doesn't have a default locale.
Execute this in your environment:

	$ export LC_ALL=en_US.UTF-8
	$ export LANG=en_US.UTF-8
Then the command will work properly.

## Step 3 创建Models
Django采用MVC设计模式，先创建Models

1.	创建App

		$ python manage.py startapp polls		
2. Edit polls/models.py

		from django.db import models
		
		class Poll(models.Model):
		    question = models.CharField(max_length=200)
		    pub_date = models.DateTimeField('date published')
		
		    def __unicode__(self):
		        return self.question
		
		class Choice(models.Model):
		    poll = models.ForeignKey(Poll)
		    choice = models.CharField(max_length=200)
		    votes = models.IntegerField()
		
		    def __unicode__(self):
		        return self.choice
3. Activating models
	* Edit settings.py
	
			INSTALLED_APPS = (
	    		'django.contrib.auth',
		    	'django.contrib.contenttypes',
			    'django.contrib.sessions',
			    'django.contrib.sites',
			    'django.contrib.messages',
			    'django.contrib.staticfiles',
			    # Uncomment the next line to enable the admin:
			    # 'django.contrib.admin',
			    # Uncomment the next line to enable admin documentation:
			    # 'django.contrib.admindocs',
			    'polls',
			)
	* 现在可以查看SQL语句，这里的语句是自动生成的
	
			$ python manage.py sql polls
			
		你会看到这样的结果，代表着Django从models里自动生成的SQL语言
		
			BEGIN;
			CREATE TABLE "polls_poll" (
			    "id" serial NOT NULL PRIMARY KEY,
			    "question" varchar(200) NOT NULL,
			    "pub_date" timestamp with time zone NOT NULL
			);
			CREATE TABLE "polls_choice" (
			    "id" serial NOT NULL PRIMARY KEY,
			    "poll_id" integer NOT NULL REFERENCES "polls_poll" ("id") DEFERRABLE INITIALLY DEFERRED,
			    "choice" varchar(200) NOT NULL,
			    "votes" integer NOT NULL
			);
			COMMIT;
	* 然后同步数据库
	
			$ python manage.py syncdb
			
## Step 4 启用Django后台管理
* Uncomment "django.contrib.admin" in the INSTALLED_APPS setting.
* Run python manage.py syncdb. 
* Edit your mysite/urls.py file 

		from django.conf.urls import patterns, include, url
		
		# Uncomment the next two lines to enable the admin:
		from django.contrib import admin
		admin.autodiscover()
		
		urlpatterns = patterns('',
		    # Examples:
		    # url(r'^$', '{{ project_name }}.views.home', name='home'),
		    # url(r'^{{ project_name }}/', include('{{ project_name }}.foo.urls')),
		
		    # Uncomment the admin/doc line below to enable admin documentation:
		    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
		
		    # Uncomment the next line to enable the admin:
		    url(r'^admin/', include(admin.site.urls)),
		)

* 测试！http://localhost:8000/admin/
* 注册polls，创建文件polls/admin.py

		from polls.models import Poll, Choice
		from django.contrib import admin
		
		admin.site.register(Choice)
		admin.site.register(Poll)
* Restart Server and Enjoy yourself (创建一些polls的数据，为了之后使用，比如这里我创建了一个polls叫What's up，三个choice关联他，nothing happened, go for work, good day)

## Step 5 创建基本的View和Url
1. 设计URLs
	* 先确保ROOT_URLCONF setting (in setting.py)
	
			ROOT_URLCONF = 'mysite.urls'
	* Edit mysites/urls.py
	
			from django.conf.urls import patterns, include, url
			from django.contrib import admin
			
			admin.autodiscover()
			
			urlpatterns = patterns('',
			                  url(r'^polls/$', 'polls.views.index'),
			                  url(r'^polls/(?P<poll_id>\d+)/$', 'polls.views.detail'),
			                  url(r'^polls/(?P<poll_id>\d+)/results/$', 'polls.views.results'),
			                  url(r'^polls/(?P<poll_id>\d+)/vote/$', 'polls.views.vote'),
			                  url(r'^admin/', include(admin.site.urls)),
			)

		
2. 创建基本的View

	Edit polls/views.py
	
		from django.http import HttpResponse
		
		def index(request):
		    return HttpResponse("Hello, world. You're at the poll index.")
		    
		def detail(request, poll_id):
		    return HttpResponse("You're looking at poll %s." % poll_id)
		
		def results(request, poll_id):
		    return HttpResponse("You're looking at the results of poll %s." % poll_id)
		
		def vote(request, poll_id):
		    return HttpResponse("You're voting on poll %s." % poll_id)

3. runserver！测试！

		http://localhost:8000/polls/
		http://localhost:8000/polls/1/
		http://localhost:8000/polls/1/results/
		http://localhost:8000/polls/1/vote/

## Step 6 创建有实际作用的View和使用模板
### 不使用模板的View

	def index(request):
	    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
	    output = ', '.join([p.question for p in latest_poll_list])
	    return HttpResponse(output)
	    
测试：http://localhost:8000/polls/
### 使用Django's template system
1. 找到Django的默认模块路径，我的是这个['/Library/Python/2.7/site-packages/django']

		python -c "
		import sys
		sys.path = sys.path[1:]
		import django
		print(django.__path__)"
2. 把contrib/admin/templates整个拷贝到一个指定的位置，如下一步这样
3. edit TEMPLATE_DIRS in your settings.py 这里要改成绝对路径
	
		"/Users/lancy/Program/python/django/templates"
Tips: 现在你可以更改admin的模板了

### 更改polls的模板
1. 更改views.py

		from django.template import Context, loader
		from polls.models import Poll
		from django.http import HttpResponse
		
		def index(request):
		    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
		    t = loader.get_template('polls/index.html')
		    c = Context({
		        'latest_poll_list': latest_poll_list,
		    })
		    return HttpResponse(t.render(c))

2. 新建[template_directory]/polls/index.html

		{% if latest_poll_list %}
		    <ul>
		    {% for poll in latest_poll_list %}
		        <li><a href="/polls/{{ poll.id }}/">{{ poll.question }}</a></li>
		    {% endfor %}
		    </ul>
		{% else %}
		    <p>No polls are available.</p>
		{% endif %}
		
Test! http://localhost:8000/polls/

#### Some Shortcut
1. render_to_response()

		from django.shortcuts import render_to_response
		from polls.models import Poll

		def index(request):
		    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
		    return render_to_response('polls/index.html', {'latest_poll_list': latest_poll_list})
		    
2. get_object_or_404()

		from django.shortcuts import render_to_response, get_object_or_404
		# ...
		def detail(request, poll_id):
		    p = get_object_or_404(Poll, pk=poll_id)
		    return render_to_response('polls/detail.html', {'poll': p})

		    
# Step 7 完善所有view和template

### Views.py

	from django.http import HttpResponseRedirect
	from polls.models import Poll, Choice
	from django.shortcuts import render_to_response
	from django.core.urlresolvers import reverse
	from django.shortcuts import get_object_or_404
	from django.template import RequestContext
	
	
	def index(request):
	    latest_poll_list = Poll.objects.all().order_by("-pub_date")[:5]
	    return render_to_response("polls/index.html", {"latest_poll_list": latest_poll_list})
	
	
	def detail(request, poll_id):
	    p = get_object_or_404(Poll, pk=poll_id)
	    return render_to_response("polls/detail.html", {"poll": p}, context_instance=RequestContext(request))
	
	
	def results(request, poll_id):
	    p = get_object_or_404(Poll, pk=poll_id)
	    return render_to_response("polls/result.html", {"poll": p})
	
	
	def vote(request, poll_id):
	    p = get_object_or_404(Poll, pk=poll_id)
	    try:
	        selected_choice = p.choice_set.get(pk=request.POST["choice"])
	    except (KeyError, Choice.DoesNotExist):
	        return render_to_response("polls/detail.html", {
	            "poll": p,
	            "error_message": "You didn't select a choice.",
	            }, context_instance=RequestContext(request))
	    else:
	        selected_choice.votes += 1
	        selected_choice.save()
	    return HttpResponseRedirect(reverse("polls.views.results", args=(p.id,)))
	    
### detail.html
	<h1>{{ poll.question }}</h1>

	{% if error_message %}<p><strong>{{ error_message }}</strong></p>{% endif %}
	
	<form action="/polls/{{ poll.id }}/vote/" method="post">
	{% csrf_token %}
	{% for choice in poll.choice_set.all %}
	    <input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}" />
	    <label for="choice{{ forloop.counter }}">{{ choice.choice }}</label><br />
	{% endfor %}
	<input type="submit" value="Vote" />
	</form>
	
### result.html

	<h1>{{ poll.question }}</h1>
	
	<ul>
	{% for choice in poll.choice_set.all %}
	    <li>{{ choice.choice }} -- {{ choice.votes }} vote{{ choice.votes|pluralize }}</li>
	{% endfor %}
	</ul>
	
	<a href="/polls/{{ poll.id }}/">Vote again?</a>
	
	
### Finished