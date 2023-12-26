from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if self._meta.model.objects.exclude(pk=self.instance.pk). \
                filter(username__iexact=username).exists():
            self.add_error(
                'username',
                self.instance.unique_error_message(
                    self._meta.model, ['username']
                )
            )

        return username

    class Meta:
        model = get_user_model()
        fields = [
            'first_name',
            'last_name',
            'username',
        ]
