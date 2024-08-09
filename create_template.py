import sys
import os

if len(sys.argv) != 2:
    print("Usage: python create_template.py <page>")
    sys.exit(1)

page = sys.argv[1]
path = "film_store/templates/" + page

if not os.path.exists(path): os.mkdir(path)

# Create files
f = open(path + "/" + (page+".css"), "w")
f = open(path + "/" + (page+".js"), "w")
f = open(path + "/" + (page+".html"), "w")
f.write("""{% extends "base.html" %}
{% load static %}

{% block style %}<link rel="stylesheet" href="{% static './"""+page+"/"+page+""".css' %}">{% endblock %}

{% block main %} 
<main>
    <h1>Page</h1>  
</main>
{% endblock %}

{% block js %}<script src="{% static './"""+page+"/"+page+""".js' %}"></script>{% endblock %}
""")


# views.py
f = open("film_store/app/views.py", "a")
f.write(f"""

class {page.capitalize()}(TemplateView):
    template_name = '{page}/{page}.html'""")

# urls.py
to_append = f"""
    path('{page}', views.{page.capitalize()}.as_view()),"""
f = open("film_store/app/urls.py", "r")
lines = f.readlines()
f.close()

for i in range(len(lines)):
    if "Views" in lines[i]:
        lines.insert(i+1, to_append)
        break

f = open("film_store/app/urls.py", "w")
f.writelines(lines)
