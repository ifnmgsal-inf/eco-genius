from django.contrib.auth.decorators import login_required
from django.urls import path, include

from lifetable.views.views import Home

urlpatterns = [
    path('', login_required(Home.as_view()), name='ecogenius'),
    path('', include('lifetable.urls')),
    path('', include('system.urls')),
]
