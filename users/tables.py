import django_tables2 as tables
from django.contrib.auth import get_user_model
from django.utils.html import format_html

User = get_user_model()  # Use custom user model

class UserTable(tables.Table):
    username = tables.Column()
    email = tables.Column()
    phone = tables.Column()  # Add phone column
    occupation = tables.Column()  # Add occupation column

    # Action buttons for edit and delete (summoned column)
    actions = tables.TemplateColumn(
        '<a href="{% url "edit_user" record.id %}" class="btn btn-warning btn-sm">Edit</a> '
        '<button type="button" class="btn btn-danger btn-sm" data-bs-toggle="modal" data-bs-target="#deleteModal{{ record.id }}">Delete</button>',
        orderable=False, 
        verbose_name='Actions'
    )

    class Meta:
        model = User
        template_name = "django_tables2/bootstrap4.html"  # Can be changed to bootstrap5
        fields = ("username", "email", "phone", "occupation", "actions")  # Add phone and occupation columns
