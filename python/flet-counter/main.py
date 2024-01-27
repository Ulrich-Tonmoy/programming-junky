import flet as ft


def main(page: ft.Page):
    page.title = "Counter"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    num_textbox = ft.TextField(
        value="0", text_align=ft.TextAlign.CENTER, width=100)

    def minus_click(e):
        if int(num_textbox.value) > 0:
            num_textbox.value = str(int(num_textbox.value) - 1)
            page.update()

    def plus_click(e):
        num_textbox.value = str(int(num_textbox.value) + 1)
        page.update()

    page.add(ft.Row([
        ft.IconButton(ft.icons.REMOVE, on_click=minus_click),
        num_textbox,
        ft.IconButton(ft.icons.ADD, on_click=plus_click),
    ], alignment=ft.MainAxisAlignment.CENTER))


ft.app(main)
