from django.db import models
# Create your models here.
NULLABLE = {'blank': True, 'null': True}


class Blog(models.Model):
    """
    Модель для статьи Блога
    """
    header = models.CharField(max_length=150, verbose_name='заголовок')
    content = models.TextField(verbose_name='содержимое')
    preview = models.ImageField(upload_to='blog/', verbose_name='превью', **NULLABLE)
    date_when_created = models.DateField(auto_now=False, auto_now_add=False,
                                         verbose_name='дата создания записи')
    views_count = models.IntegerField(default=0, verbose_name='Количество просмотров')
    author = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='автор')

    def __str__(self):
        return self.header

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'
