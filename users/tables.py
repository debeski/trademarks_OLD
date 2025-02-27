import django_tables2 as tables
from django.contrib.auth import get_user_model
from django.utils.html import format_html
from .models import UserActivityLog

User = get_user_model()  # Use custom user model

class UserTable(tables.Table):
    username = tables.Column()
    email = tables.Column()
    phone = tables.Column()  # Add phone column
    occupation = tables.Column()  # Add occupation column

    # Action buttons for edit and delete (summoned column)
    actions = tables.TemplateColumn(
        '<a href="{% url "edit_user" record.id %}" class="btn btn-info btn-sm">Edit</a> '
        ' {% if user.is_superuser %} <button type="button" class="btn btn-danger btn-sm" data-bs-toggle="modal" data-bs-target="#deleteModal{{ record.id }}">Delete</button>{% endif %}',
        orderable=False, 
        verbose_name='Actions'
    )

    class Meta:
        model = User
        template_name = "django_tables2/bootstrap5.html"  # Can be changed to bootstrap5
        fields = ("username", "email", "phone", "occupation", "actions")  # Add phone and occupation columns

class UserActivityLogTable(tables.Table):
    class Meta:
        model = UserActivityLog
        template_name = "django_tables2/bootstrap5.html"
        fields = ("timestamp", "user", "action", "model_name", "object_id", "number", "ip_address")

