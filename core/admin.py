from django.contrib import admin

# Register your models here.
from .models import Delegate,DelegateUndelegateStatus,AprSave,WeeklyAprAverage



@admin.register(DelegateUndelegateStatus)
class DelegateUndelegateStatusAdmin(admin.ModelAdmin):
    list_display = [field.name for field in DelegateUndelegateStatus._meta.get_fields()]  # Display all fields of the Delegate model
   


@admin.register(AprSave)
class AprSaveAdmin(admin.ModelAdmin):
    list_display = [field.name for field in AprSave._meta.get_fields()]  # Display all fields of the Delegate model
   


@admin.register(Delegate)
class DelegateAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Delegate._meta.get_fields()]  # Display all fields of the Delegate model
   
    

@admin.register(WeeklyAprAverage)
class WeeklyAprAverageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in WeeklyAprAverage._meta.get_fields()]  # Display all fields of the Delegate model
   
    
