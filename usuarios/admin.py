from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUsuarioCreateForm, CustomUsuarioChangeForm
from .models import CustomUsuario


@admin.register(CustomUsuario)
class CustomUsuarioAdmin(UserAdmin):  # Criada uma classe que herda de (UserAdmin)
    add_form = CustomUsuarioCreateForm  # variavel recebe a classe de criaçao de usuários do Form
    form = CustomUsuarioChangeForm  # variavel recebe a classe de alteraçao de dados de usuários do Form
    model = CustomUsuario  # variavel recebe classe do Model
    list_display = ('first_name', 'last_name', 'email', 'fone', 'is_staff')  # Quais informaçoes serao apresentadas
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informaçoes Pessoais', {'fields': ('first_name', 'last_name', 'fone')}),
        ('Permissoes', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )

    # Os fieldsets sao para quando acessarmos a área administrativa, veremos os dados de cadastro do usuário
    # (campos que poderemos cadastrar)

