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

<a href="https://github.com/gmatt/mnist-in-y-minutes/new/main/content">➕ Add a new library</a>

<a href="https://github.com/gmatt/mnist-in-y-minutes/blob/main/.github/CONTRIBUTING.md">❔ How to contribute</a>
