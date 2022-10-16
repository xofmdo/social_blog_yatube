from django.contrib import admin
from django.urls import include, path
from django.conf import settings

urlpatterns = [
    path('', include('posts.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls', namespace='auth_personal')),
    path('auth/', include('django.contrib.auth.urls')),
    path('about/', include('about.urls', namespace='about')),
]

handler404 = 'core.views.page_not_found'
handler500 = 'core.views.server_error'
handler403 = 'core.views.permission_denied'


if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
