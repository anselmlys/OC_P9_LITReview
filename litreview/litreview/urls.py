"""
URL configuration for litreview project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

import authentication.views
import flux.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', authentication.views.login_page, name='login'),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('home/', flux.views.home, name='home'),
    path('logout/', authentication.views.logout_user, name='logout'),
    path('tickets/', flux.views.tickets, name='tickets'),
    path('tickets/create/', flux.views.create_ticket, name='create_ticket'),
    path('tickets/create-with-review/', flux.views.create_ticket_and_review, name='create-ticket-review'),
    path('tickets/<int:ticket_id>/modify/', flux.views.modify_ticket, name='modify_ticket'),
    path('tickets/<int:ticket_id>/delete/', flux.views.delete_ticket, name='delete_ticket'),
    path('tickets/<int:ticket_id>/create-review/', flux.views.create_review, name='create_review'),
    path('tickets/<int:ticket_id>/reviews/<int:review_id>/', flux.views.modify_review, name='modify_review'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
