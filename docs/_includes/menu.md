{% capture my_include %}

[Home]({{ site.baseurl }}/) &nbsp;&nbsp;&nbsp;&nbsp;
[User Guide]({{ site.baseurl }}/user-guide) &nbsp;&nbsp;&nbsp;&nbsp;
[Technical Documentation]({{ site.baseurl }}/internals)

{% endcapture %}
{{ my_include | markdownify }}