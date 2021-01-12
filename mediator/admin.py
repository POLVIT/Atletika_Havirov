from django.contrib import admin
from .models import PrispevekProMediatora, PrispevekFiles, createPost

admin.site.register(PrispevekProMediatora)
admin.site.register(PrispevekFiles)
admin.site.register(createPost)
