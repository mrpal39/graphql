from django.urls import path, include, re_path

from django.contrib import admin
from django.urls import path

from graphene_django.views import GraphQLView
urlpatterns = [
    path("graphql", GraphQLView.as_view(graphiql=True)),

    path('admin/', admin.site.urls),
    path('', include('geo.urls')),
    path('account/', include('accounts.api.urls')),

    path('product/', include('products.urls')),
]
