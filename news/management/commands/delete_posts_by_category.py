from django.core.management.base import BaseCommand
from news.models import Post, Category


class Command(BaseCommand):
    help = 'Удаляет все посты из указанной категории'
    def add_arguments(self, parser):
        parser.add_argument(
            'category_name',
            type=str,
            help='Название категории, из которой нужно удалить все посты'
        )

    def handle(self, *args, **options):
        category_name = options['category_name']
        try:
            category = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Категория "{category_name}" не найдена!')
            )
            return

        posts_to_delete = Post.objects.filter(categories=category)
        post_count = posts_to_delete.count()

        if post_count == 0:
            self.stdout.write(
                self.style.SUCCESS(f'В категории "{category_name}" нет постов. Удалять нечего.')
            )
            return

        self.stdout.write(
            self.style.WARNING(
                f'Вы уверены, что хотите удалить {post_count} постов '
                f'из категории "{category_name}"? [yes/no]'
            )
        )

        answer = input().lower()

        if answer == 'yes' or answer == 'y':
            posts_to_delete.delete()
            self.stdout.write(
                self.style.SUCCESS(
                    f'Успешно удалено {post_count} постов из категории "{category_name}".'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING('Удаление отменено.')
            )