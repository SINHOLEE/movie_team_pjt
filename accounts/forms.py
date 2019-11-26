from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
# 현재 활성화된 유저모델 불러온다.

class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields


class CustomUserChangeForm(UserChangeForm):
    
    class Meta:
        model = get_user_model() #커스터마이징 후에는 accounts.User를 반환하게 됨
        fields = ['email', 'first_name', 'last_name',]