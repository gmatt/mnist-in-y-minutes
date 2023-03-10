---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: home
---

Quickly get started with machine learning libraries.

Inspired by [learnxinyminutes.com](https://learnxinyminutes.com).

# Libraries

{% for page in site.pages %}
    {% if page.url contains '/libraries/' %}
## <a href="{{ page.url | relative_url }}">{{ page.title }}</a>
    {% endif %}
{% endfor %}
