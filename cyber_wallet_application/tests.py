import pytest
from django.contrib.auth.models import User, AnonymousUser
from pytest_django.fixtures import rf, admin_user

from cyber_wallet_application.views import index


def test_admin_index_view(rf, admin_user):
    request = rf.get("/")
    request.user = admin_user
    response = index(request)
    assert response.status_code == 200


def test_anonymous_index_view(rf):
    request = rf.get("/")
    request.user = AnonymousUser()
    response = index(request)
    assert response.status_code == 302


def test_admin_operations_view(rf, admin_user):
    request = rf.get("/read_operations")
    request.user = admin_user
    response = index(request)
    assert response.status_code == 200


def test_anonymous_operations_view(rf):
    request = rf.get("/read_operations")
    request.user = AnonymousUser()
    response = index(request)
    assert response.status_code == 302


def test_admin_reports_view(rf, admin_user):
    request = rf.get("/read_reports")
    request.user = admin_user
    response = index(request)
    assert response.status_code == 200


def test_anonymous_reports_view(rf):
    request = rf.get("/read_reports")
    request.user = AnonymousUser()
    response = index(request)
    assert response.status_code == 302


def test_admin_note_view(rf, admin_user):
    request = rf.get("/read_note")
    request.user = admin_user
    response = index(request)
    assert response.status_code == 200


def test_anonymous_note_view(rf):
    request = rf.get("/read_note")
    request.user = AnonymousUser()
    response = index(request)
    assert response.status_code == 302


def test_admin_settings_view(rf, admin_user):
    request = rf.get("/settings")
    request.user = admin_user
    response = index(request)
    assert response.status_code == 200


def test_anonymous_settings_view(rf):
    request = rf.get("/settings")
    request.user = AnonymousUser()
    response = index(request)
    assert response.status_code == 302


def test_admin_info_view(rf, admin_user):
    request = rf.get("/info")
    request.user = admin_user
    response = index(request)
    assert response.status_code == 200


def test_anonymous_info_view(rf):
    request = rf.get("/info")
    request.user = AnonymousUser()
    response = index(request)
    assert response.status_code == 302
