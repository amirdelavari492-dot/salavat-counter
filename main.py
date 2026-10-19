import flet as ft
import sqlite3
import os


def main(page: ft.Page):

    # اتصال به دیتابیس
    db = sqlite3.connect("salavat.db")

    print("مسیر دیتابیس:")
    print(os.path.abspath("salavat.db"))


    # ساخت جدول
    db.execute("""
        CREATE TABLE IF NOT EXISTS counter (
            id INTEGER PRIMARY KEY,
            count INTEGER
        )
    """)

    # اگر شمارنده وجود ندارد، آن را بساز
    db.execute("""
        INSERT OR IGNORE INTO counter (id, count)
        VALUES (1, 0)
    """)

    db.commit()

    # خواندن عدد ذخیره شده
    result = db.execute(
        "SELECT count FROM counter WHERE id = 1"
    ).fetchone()

    count = result[0]

    # تنظیمات صفحه
    page.title = "صلوات شمار"
    page.bgcolor = "#07111F"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # رنگ ها
    gold = "#FFD580"
    white = "#F8FAFC"
    gray = "#9CA3AF"

    # نمایش عدد
    number = ft.Text(
        str(count),
        size=75,
        weight=ft.FontWeight.BOLD,
        color=white,
    )

    # ذخیره عدد در دیتابیس
    def save_count():
        db.execute(
            "UPDATE counter SET count = ? WHERE id = 1",
            (count,)
        )
        db.commit()

    # افزایش شمارنده
    def add_salavat(e):
        nonlocal count

        count += 1
        number.value = str(count)

        save_count()
        page.update()

    # کاهش شمارنده
    def remove_salavat(e):
        nonlocal count

        if count > 0:
            count -= 1

        number.value = str(count)

        save_count()
        page.update()

    # صفر کردن شمارنده
    def reset_counter(e):
        nonlocal count

        count = 0
        number.value = "0"

        save_count()
        page.update()

    # دکمه افزایش
    add_button = ft.Container(
        content=ft.Icon(
            ft.Icons.ADD,
            size=55,
            color="#07111F",
        ),
        width=125,
        height=125,
        bgcolor=gold,
        border_radius=100,
        alignment=ft.Alignment.CENTER,
        shadow=ft.BoxShadow(
            blur_radius=30,
            color="#806B3E",
            offset=ft.Offset(0, 0),
        ),
        on_click=add_salavat,
        ink=True,
    )

    # دایره شمارنده
    counter_circle = ft.Container(
        content=ft.Column(
            controls=[
                ft.Icon(
                    ft.Icons.AUTO_AWESOME,
                    size=32,
                    color=gold,
                ),
                number,
                ft.Text(
                    "تعداد صلوات",
                    size=18,
                    color=gray,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
        ),
        width=290,
        height=290,
        alignment=ft.Alignment.CENTER,
        bgcolor="#0D1B2A",
        border=ft.Border.all(3, "#344256"),
        border_radius=200,
    )

    # دکمه بازنشانی
    reset_button = ft.OutlinedButton(
        content="بازنشانی",
        icon=ft.Icons.REFRESH,
        on_click=reset_counter,
    )

    # دکمه کاهش
    minus_button = ft.OutlinedButton(
        content="کاهش",
        icon=ft.Icons.REMOVE,
        on_click=remove_salavat,
    )

    # کارت پایین صفحه
    message_card = ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(
                    ft.Icons.WB_TWILIGHT,
                    color=gold,
                    size=30,
                ),
                ft.Column(
                    controls=[
                        ft.Text(
                            "یک صلوات دیگر...",
                            size=17,
                            color=white,
                        ),
                        ft.Text(
                            "برای آرامش دل خودت",size=14,
                            color=gray,
                        ),
                    ],
                    spacing=6,
                    expand=True,
                    horizontal_alignment=ft.CrossAxisAlignment.END,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        bgcolor="#122033",
        padding=18,
        border_radius=22,
        border=ft.Border.all(1, "#29394D"),
        width=350,
    )

    # عنوان
    header = ft.Column(
        controls=[
            ft.Text(
                "صلوات شمار",
                size=30,
                weight=ft.FontWeight.BOLD,
                color=white,
            ),
            ft.Text(
                "هر صلوات، یک قدم به سمت آرامش...",
                size=14,
                color=gray,
                text_align=ft.TextAlign.CENTER,
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=12,
    )

    # نمایش اجزا
    page.add(
        ft.SafeArea(
            expand=True,
            content=ft.Column(
                controls=[
                    header,
                    ft.Container(height=25),
                    counter_circle,
                    ft.Container(height=10),
                    add_button,
                    ft.Row(
                        controls=[
                            reset_button,
                            minus_button,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20,
                    ),
                    ft.Container(height=10),
                    message_card,
                    ft.Text(
                        "صلوات، نور در مسیر زندگی",
                        size=13,
                        color="#718096",
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            ),
        )
    )


ft.run(main)