from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# Criando um user model customizado já contendo várias funçoes necessárias importando (AbstractUser) ao invés de
# importar o (AbstractBaseUser) que é bem básico tendo que implementar diversas funçoes na mao.
# Importando também um gerenciador de usuários (BaseUserManager) que será utilizado para gerenciar o custom usuário que
# esta sendo criado

# Criada classe gerenciadora do nosso usuário customizado
class UsuarioManager(BaseUserManager):

    use_in_migrations = True  # Avisando que esse model de user que será utilizado em migrations. Sendo assim utilizado
    # no banco de dados para autenticacao

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Inserçao do e-mail é obrigatória!')  # levantado erro caso nao recebamos o email
        email = self.normalize_email(email)  # Serve para ajeitar o email recebido para os parametros básicos
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)  # Irá criptografar a senha digitada
        user.save(using=self._db)  # Os dados do usuário criado sao salvos no banco
        return user  # Retorna o usuário

    # Funçao para criar usuário comum que retorna a def _create_user que é responsável por salvar no banco de dados
    def create_user(self, email, password=None, **extra_fields):  # Criando usuário comum
        # extra_fields.setdefault('is_staff', True)  # Usuário comum para acessar o admin somente com ('is_staff', True)
        extra_fields.setdefault('is_superuser', False)  # Campos extras setados como padrao (super_user=False)
        return self._create_user(email, password, **extra_fields)  # Retornando a def _create_user

    # Funçao para criar super usuário que retorna a def _create_user que é responsável por salvar no banco de dados
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Condicao para criar super_usuário levantando erro (raise) caso campo extra 'is_superuser' nao seja True
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Necessário que is_superuser=True')

        # Condicao para criar super_usuário levantando erro (raise) caso campo extra 'is_staff' nao seja True
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Necessário que is_staff=True')

        return self._create_user(email, password, **extra_fields)  # Retornando a def _create_user


# Criando nosso usuário customizado contendo seus campos para inserçao de dados
class CustomUsuario(AbstractUser):
    email = models.EmailField('E-mail', unique=True)  # unique=True quer dizer que e-mail será utilizado 1 vez apenas
    fone = models.CharField('Telefone', max_length=15)
    is_staff = models.BooleanField('Membro da Equipe', default=True)

    USERNAME_FIELD = 'email'  # Campo de acesso utilizará o email para login
    REQUIRED_FIELDS = ['first_name', 'last_name', 'fone']  # Campos Requeridos. O email e o password já serao
    # exigidos para autenticaçao o próprio sistema já solicita/exigi

    def __str__(self):
        return self.email

    objects = UsuarioManager()  # Os objetos desse CustomUsuario sao gerenciados pela classe UsuarioManager(). Tem de
    # ser passado senao será utilizado o Manager padrao do Django sem obrigatoriedade do email para login.

