from django.contrib import admin
from django.urls import path, include

from cyber_wallet_application import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index),
    path("accounts/profile/", views.index),
    path("accounts/", include('django.contrib.auth.urls')),

    path("create_operation/", views.create_operation),
    path("delete_operation/<int:pk>", views.delete_operation),
    path("read_operations/", views.read_operations),
    path("update_operation/<int:pk>", views.update_operation),

    path("create_report/", views.create_report),
    path("delete_report/<int:pk>", views.delete_report),
    path("read_report/<int:pk>", views.read_report),
    path("read_reports/", views.read_reports),

    path("create_note/", views.create_note),
    path("delete_note/<int:pk>", views.delete_note),
    path("update_note/<int:pk>", views.update_note),
    path("read_notes/", views.read_notes),

    path("info/", views.info),
    path("settings/", views.settings),
    path("update_configuration/<int:pk>", views.update_configuration),

    path("register/", views.register)
]
