import random
from datetime import date
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from app.models import Author, Category, Book, Post, Comment  # Замени 'blog' на имя своего приложения, если отличается

User = get_user_model()


class Command(BaseCommand):
    help = "Заполняет базу данных тестовыми данными для проекта DRF Blog"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Очистить существующие данные перед заполнением",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write(self.style.WARNING("Очистка базы данных..."))
            Comment.objects.all().delete()
            Post.objects.all().delete()
            Book.objects.all().delete()
            Author.objects.all().delete()
            Category.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
            self.stdout.write(self.style.SUCCESS("База данных очищена."))

        self.stdout.write(self.style.HTTP_INFO("Начало заполнения тестовыми данными..."))

        # 1. Создание пользователей
        users = []
        usernames = ["alex_reader", "bookworm_kate", "john_critic", "lisa_editor", "mark_writer"]
        for username in usernames:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={"is_staff": False}
            )
            if created:
                user.set_password("pass12345")
                user.save()
            users.append(user)
        self.stdout.write(f"Создано пользователей: {len(users)}")

        # 2. Создание категорий (жанров)
        categories_data = [
            ("Science Fiction", "Книги о будущем, космосе и технологиях"),
            ("Fantasy", "Магия, драконы и вымышленные миры"),
            ("Detective", "Загадки, расследования и интригующие сюжеты"),
            ("Classics", "Проверенная временем мировая литература"),
            ("Biography", "Реальные истории жизни выдающихся людей"),
        ]
        categories = []
        for title, desc in categories_data:
            cat, _ = Category.objects.get_or_create(
                title=title,
                defaults={
                    "slug": slugify(title),
                    "description": desc,
                }
            )
            categories.append(cat)
        self.stdout.write(f"Создано категорий: {len(categories)}")

        # 3. Создание авторов книг
        authors_data = [
            ("George", "Orwell", "British writer and journalist", date(1903, 6, 25), date(1950, 1, 21), "British"),
            ("J.K.", "Rowling", "British author, best known for Harry Potter", date(1965, 7, 31), None, "British"),
            ("Arthur", "Conan Doyle", "Creator of Sherlock Holmes", date(1859, 5, 22), date(1930, 7, 7), "Scottish"),
            ("Stephen", "King", "Master of horror and suspense", date(1947, 9, 21), None, "American"),
            ("Agatha", "Christie", "Queen of mystery novels", date(1890, 9, 15), date(1976, 1, 12), "British"),
        ]
        authors = []
        for first_name, last_name, bio, dob, dod, nat in authors_data:
            slug = slugify(f"{first_name}-{last_name}")
            author, _ = Author.objects.get_or_create(
                slug=slug,
                defaults={
                    "first_name": first_name,
                    "last_name": last_name,
                    "date_of_birth": dob,
                    "date_of_death": dod,
                    "nationality": nat,
                }
            )
            authors.append(author)
        self.stdout.write(f"Создано авторов: {len(authors)}")

        # 4. Создание книг
        books_data = [
            ("1984", 1949, "978-0451524935", [authors[0]], [categories[0], categories[3]]),
            ("Harry Potter and the Philosopher's Stone", 1997, "978-0747532699", [authors[1]], [categories[1]]),
            ("The Adventures of Sherlock Holmes", 1892, "978-0140437713", [authors[2]], [categories[2], categories[3]]),
            ("The Shining", 1977, "978-0307743657", [authors[3]], [categories[2]]),
            ("Murder on the Orient Express", 1934, "978-0007119319", [authors[4]], [categories[2]]),
        ]
        books = []
        for title, year, isbn, b_authors, b_cats in books_data:
            book, _ = Book.objects.get_or_create(
                title=title,
                defaults={
                    "slug": slugify(title),
                    "publication_year": year,
                    "isbn": isbn,
                }
            )
            book.authors.set(b_authors)
            book.categories.set(b_cats)
            books.append(book)
        self.stdout.write(f"Создано книг: {len(books)}")

        # 5. Создание постов (обзоров книг)
        post_titles = [
            "Why 1984 is More Relevant Today Than Ever",
            "Magic and Childhood: A Review of Harry Potter",
            "The Genius of Sherlock Holmes Deductive Method",
            "Spooky Atmosphere and Psychological Depth in The Shining",
            "Unraveling the Mystery of Orient Express",
        ]
        posts = []
        for i, title in enumerate(post_titles):
            post, _ = Post.objects.get_or_create(
                slug=slugify(title),
                defaults={
                    "title": title,
                    "author_user": random.choice(users),
                    "book": books[i],
                    "content": f"This is a detailed review and analysis of '{books[i].title}'. " * 5,
                    "status": Post.STATUS_CHOICES.PUBLISHED,
                    "rating": random.randint(3, 5),
                }
            )
            posts.append(post)
        self.stdout.write(f"Создано постов: {len(posts)}")

        # 6. Создание комментариев к постам
        comment_texts = [
            "Great review! I totally agree with your points.",
            "Interesting perspective, though I think the ending was a bit rushed.",
            "This is one of my all-time favorite books!",
            "Thanks for sharing this, adding it to my reading list.",
            "I have a slightly different view on the main character's choices.",
        ]
        comment_count = 0
        for post in posts:
            for _ in range(random.randint(2, 4)):
                Comment.objects.create(
                    post=post,
                    user=random.choice(users),
                    text=random.choice(comment_texts),
                )
                comment_count += 1

        self.stdout.write(f"Создано комментариев: {comment_count}")
        self.stdout.write(self.style.SUCCESS("✅ Заполнение базы данных успешно завершено!"))