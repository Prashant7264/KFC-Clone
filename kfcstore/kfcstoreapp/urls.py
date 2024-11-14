from django.urls import path
from kfcstoreapp import views
from django.conf.urls.static import static
from kfcstore import settings
from django.conf.urls.static import static

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('main',views.main),
    path('login',views.ulogin),
    path('logout',views.ulogout),
    path('register',views.register),
    path('deal',views.deal),
    path('addtocart/<pid>',views.addtocart),
    path('viewcart',views.viewcart),
    path('range_filter',views.range_filter),
    path('contact',views.contact),
    path('remove/<cid>',views.remove),
    path('order/<pid>',views.order),
    path('updateqty/<qv>/<cid>',views.updateqty),
    path('placeorder',views.placeorder),
    path('makepayment',views.makepayment),
    path('search',views.search),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
