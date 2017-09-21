from django.contrib import admin

from .models import Team
from .models import Criteria
from .models import Sprint
from .models import Ranking

admin.site.register(Team)
admin.site.register(Criteria)
admin.site.register(Sprint)
admin.site.register(Ranking)
