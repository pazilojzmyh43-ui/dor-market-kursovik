import os
import shutil
from datetime import datetime
from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from app.models import Blog, Category, Comment, Order, OrderLine, Product


class Command(BaseCommand):
    help = "Заполняет базу салона DoorMarket учебными данными."

    def handle(self, *args, **options):
        self._users()
        if not Category.objects.exists():
            self._catalog()
        if not Blog.objects.exists():
            self._news()
        if not Order.objects.exists():
            self._orders()
        self.stdout.write(self.style.SUCCESS("База DoorMarket заполнена."))

    def _users(self):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@mail.ru", "admin123")
        if not User.objects.filter(username="client").exists():
            User.objects.create_user(
                "client",
                "client@doormarket.ru",
                "client123",
                first_name="Анна",
                last_name="Соколова",
            )
        if not User.objects.filter(username="manager").exists():
            manager = User.objects.create_user(
                "manager",
                "manager@doormarket.ru",
                "manager123",
                first_name="Игорь",
                last_name="Лебедев",
            )
            manager.is_staff = True
            manager.is_superuser = False
            manager.save()

    def _copy(self, src_name, dest_rel):
        src = os.path.join(settings.MEDIA_ROOT, "products", src_name)
        dest = os.path.join(settings.MEDIA_ROOT, dest_rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        if os.path.exists(src) and not os.path.exists(dest):
            shutil.copyfile(src, dest)
        return dest_rel.replace("\\", "/")

    def _catalog(self):
        categories = [
            ("Межкомнатные двери", "Полотна для комнат, кабинета и кухни: глухие, остеклённые и с цветной эмалью."),
            ("Входные двери", "Утеплённые двери в квартиру и дом: сталь, два контура уплотнения и надёжные замки."),
            ("Раздвижные двери", "Купе, пеналы и перегородки, когда нужно оставить проход свободным."),
        ]
        created = []
        for name, description in categories:
            created.append(Category.objects.create(name=name, description=description))
        items = [
            (0, "Межкомнатная дверь «Лайн»", "Белое полотно с горизонтальными фрезерованными линиями.",
             "Спокойная модель для кухни и спальни. Горизонтальные линии собирают свет и не спорят с мебелью. Эмаль матовая, кромка закрыта по периметру, петли скрытые.\n\nПокрытие: эмаль. Размер полотна: 2000×800 мм.",
             "12800", "1.jpg"),
            (0, "Межкомнатная дверь «Витраж»", "Белая дверь с решёткой из матового стекла в верхней части.",
             "Стекло пропускает свет в коридор и закрывает обзор. Нижняя филёнка глухая, поэтому дверь выглядит собранно даже рядом с тёмной стеной.",
             "14600", "2.jpg"),
            (0, "Межкомнатная дверь «Лазурь»", "Цветная эмаль и три вставки рифлёного стекла.",
             "Пыльный голубой оттенок хорошо стоит в сером интерьере. Рифлёное стекло рассеивает свет. Чёрная ручка идёт в комплекте.",
             "16900", "3.jpg"),
            (0, "Межкомнатная дверь «Дуб»", "Глухое полотно под дуб со скрытой коробкой.",
             "Ровная плоскость без лишнего декора. Шпон дуба и скрытая коробка делают проём тихим акцентом.",
             "18400", "4.jpg"),
            (0, "Межкомнатная дверь «Сканди»", "Светлое полотно с восемью стёклами.",
             "Классическая решётка, но без тёмной морени. Матовое стекло не режет глаз у окна.",
             "15200", "5.jpg"),
            (1, "Входная дверь «Форт»", "Графитовая стальная дверь с глазком и двумя замками.",
             "Квартирная дверь с листом 1,5 мм, минеральной ватой и двумя контурами уплотнения.",
             "24900", "e1.jpg"),
            (1, "Входная дверь «Орех»", "Тёплая накладка под орех и стальной каркас.",
             "Со стороны лестницы дверь выглядит деревянной, внутри — стальной короб. Накладка МДФ с покрытием под орех.",
             "28900", "e2.jpg"),
            (1, "Входная дверь «Бастион»", "Высокая чёрная дверь с вертикальным рифлением.",
             "Модель для частного дома: лист толще, броненакладки на замках, терморазрыв снижает промерзание.",
             "34900", "e3.jpg"),
            (1, "Входная дверь «Страж»", "Светлая утеплённая дверь с длинной ручкой.",
             "Светлый порошковый окрас, два контура уплотнения и широкий порог с терморазрывом.",
             "27500", "e4.jpg"),
            (1, "Входная дверь «Цитадель»", "Филёнчатая дверь глубокого зелёного цвета.",
             "Классические филёнки и латунная фурнитура. Под отделкой — стальной лист и два замка.",
             "42900", "e5.jpg"),
            (2, "Раздвижная дверь «Слайдер»", "Дубовое полотно на чёрной направляющей вдоль стены.",
             "Одна створка уезжает вдоль стены и не занимает место распахиванием. Ролики на подшипнике, ход тихий.",
             "15600", "s1.jpg"),
            (2, "Перегородка «Купе Лайт»", "Матовое стекло в алюминиевой раме между кухней и гостиной.",
             "Лёгкая перегородка закрывает запахи и оставляет свет. Ставится в готовый проём.",
             "19800", "s2.jpg"),
            (2, "Раздвижная дверь «Пенал»", "Белое полотно уходит внутрь стены.",
             "Кассета монтируется до чистовой отделки. В открытом виде дверь не висит у стены.",
             "21400", "s3.jpg"),
            (2, "Портал «Горизонт»", "Две тёмные створки на всю стену между комнатами.",
             "Проём между кухней и гостиной закрывается двумя полотнами. Шпон тёмного ореха.",
             "26800", "s4.jpg"),
            (2, "Раздвижная дверь «Сёдзи»", "Светлая рама и полупрозрачные панели.",
             "Тонкая рама из ясеня и рассеивающие панели. Ход по верхней направляющей, порога нет.",
             "18700", "s5.jpg"),
        ]
        for index, name, short, full, price, image in items:
            Product.objects.create(
                category=created[index],
                name=name,
                short_description=short,
                full_description=full,
                price=Decimal(price),
                image="products/%s" % image,
            )

    def _news(self):
        admin = User.objects.get(username="admin")
        client = User.objects.get(username="client")
        posts = [
            ("Салон открылся на Советской",
             "DoorMarket принимает в зале на улице Советской: можно открыть образцы и сравнить покрытия.",
             "Зал работает каждый день. На стендах стоят межкомнатные полотна, входной блок и раздвижная система.\n\nЗамер по Пскову записываем на ресепшен или по телефону с сайта.",
             datetime(2026, 9, 2, 10, 0, 0), "4.jpg"),
            ("Коллекция «Сканди» уже в зале",
             "Светлые полотна с матовым стеклом привезли к началу учебного года.",
             "Восемь стёкол, эмаль без морени и спокойный рисунок. Модель берут в столовую и детскую.\n\nОбразец стоит у окна, цвет при дневном свете не желтит.",
             datetime(2026, 9, 18, 12, 0, 0), "5.jpg"),
            ("Замер и доставка по Пскову",
             "Выезд замерщика по городу бесплатный, если заказ оформлен в течение недели.",
             "Размеры снимаем до запуска полотна в работу. Доставка до подъезда входит в заказ по городу.\n\nПодъём без лифта оговаривается в комментарии к заказу.",
             datetime(2026, 10, 1, 9, 30, 0), "1.jpg"),
            ("Скидка на входные двери",
             "До конца месяца модели «Форт» и «Страж» отдаём с установкой коробки.",
             "В стоимость входят полотно, коробка и два контура уплотнения. Замки ставим те, что уже в комплекте.\n\nЗаписаться на замер можно через заказ на сайте: положите модель в корзину и оставьте комментарий.",
             datetime(2026, 10, 8, 11, 0, 0), "e1.jpg"),
        ]
        saved = []
        for title, description, content, posted, image in posts:
            rel = self._copy(image, "posts/%s" % image)
            saved.append(Blog.objects.create(
                title=title,
                description=description,
                content=content,
                posted=posted,
                image=rel,
                author=admin,
            ))
        Comment.objects.create(
            text="Были в зале в субботу. «Сканди» у окна выглядит светлее, чем на фото.",
            date=datetime(2026, 10, 3, 15, 20, 0),
            author=client,
            post=saved[1],
        )

    def _orders(self):
        client = User.objects.get(username="client")
        line = Product.objects.get(name__contains="Лайн")
        fort = Product.objects.get(name__contains="Форт")
        first = Order.objects.create(
            client=client,
            created=datetime(2026, 10, 4, 16, 0, 0),
            status="processing",
            comment="Подъём на 4 этаж, лифта нет.",
        )
        OrderLine.objects.create(order=first, product=line, name=line.name, price=line.price, quantity=1)
        second = Order.objects.create(
            client=client,
            created=datetime(2026, 10, 9, 13, 10, 0),
            status="new",
            comment="Нужен замер в субботу.",
        )
        OrderLine.objects.create(order=second, product=fort, name=fort.name, price=fort.price, quantity=1)
