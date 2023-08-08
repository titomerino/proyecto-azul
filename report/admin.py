from django.contrib import admin
from django.urls import path
from django import forms
from django.shortcuts import render

from daterange.filters import DateRangeFilter

from .models import Report
    

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    fields = (
        'title',
        ('report_type', 'project'),
        ('start_date', 'end_date'),
        'report_pdf',
    )
    list_display = (
        'title',
        'start_date',
        'end_date',
        'report_type',
        'report_pdf',
        'project',
    )
    search_fields = ('title',)
    readonly_fields = ('report_pdf',)
    list_per_page = 10
    list_filter = [
        ('start_date', DateRangeFilter),
        'project__name',
    ]
    change_list_template = "admin/daterange/change_list.html"
