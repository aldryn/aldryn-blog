# -*- coding: utf-8 -*-
from django import forms

import django_select2


class LatestEntriesForm(forms.ModelForm):

    class Meta:
        widgets = {
            'tags': django_select2.Select2MultipleWidget()
        }
