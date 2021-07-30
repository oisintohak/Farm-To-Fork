from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Div,
    HTML,
    Field,
)


class ProductVariantFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_tag = False
        self.label_class = 'col-form-label'
        self.render_required_fields = False
        self.layout = Layout(
            Div(
                HTML('<hr class="mx-auto">'),
                Div(
                    'price',
                    css_class='col-3'
                ),
                Div(
                    'size',
                    css_class='col-3'
                ),
                Div(
                    'unit',
                    css_class='col-4'
                ),
                Div(
                    HTML(
                        '<fieldset>'
                    ),
                    Field(
                        'DELETE'
                    ),
                    HTML(
                        '</fieldset>'
                    ),
                    css_class='d-none',
                    hidden=True,
                ),
                css_class='formset-formgroup row'

            )
        )
