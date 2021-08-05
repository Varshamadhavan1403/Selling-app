from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('sell_app.urls')),
    path('admin/', admin.site.urls),
    # path('accounts/', include('allauth.urls')),
    # path('home/', TemplateView.as_view(template_name = 'sell_app/home.html'), name = 'home'),
    path('', include('social_django.urls', namespace='social'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)