from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('admin/', admin.site.urls),
    # path('api/paytm/', include('drf_paytm.urls')),
    path('', include('user.urls'), name = 'home'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
