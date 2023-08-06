### Wagtail Reoako

Wagtail plugin for [reoako.nz](https://www.reoako.nz/)

---

Steps To Add wagtail_reoako to wagtail

```python
# settings.py

# Add wagtail_reoako to installed apps
INSTALLED_APPS = [
    'wagtail_reoako',
]

# Add Reoako settings
REOAKO_API_KEY = '<your_api_key>' # Required. And client domains must be whitelisted
REOAKO_API_DOMAIN = 'http://api.reoako.nz'  # optiona. defaults to production: https://api.reoako.nz

# Add Reoako to draftail editor.
WAGTAILADMIN_RICH_TEXT_EDITORS = {
    'default': {
        'WIDGET': 'wagtail.admin.rich_text.DraftailRichTextArea',
        'OPTIONS': {
            'features': [
                # ...       
                'reoako',
            ]
         }
    },
}
```
