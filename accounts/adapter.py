from allauth.account.adapter import DefaultAccountAdapter


class UserAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super(UserAccountAdapter, self).save_user(
            request, user, form, commit=False)
        user.user_type = form.cleaned_data.get('user_type')
        user.save()
        # For other default validations.
        return DefaultAccountAdapter
