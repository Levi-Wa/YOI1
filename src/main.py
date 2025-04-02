import flet as ft

def main(page: ft.Page):
    def What_file(e):
        if not Name_file.value:
            Name_file.error_text = "Пожалуйста, введите имя файла"
            page.update()
        else:
            name = Name_file.value
            page.clean()
            try:
                with open(name, 'r', encoding='utf-8') as f:  
                    page.add(ft.Text(value="Файл открыт", color="green"))
                    content = f.read()
                    page.add(ft.Text(value=content, color="white"))
            except FileNotFoundError:
                page.add(ft.Text(value="Файл не найден или его не существует", color="red"))
            except Exception as e:
                page.add(ft.Text(value=f"Произошла ошибка: {e}", color="red"))
            page.update() 
    Name_file = ft.TextField(label="Ссылка на файл")

    page.add(Name_file, ft.ElevatedButton('Открыть файл', on_click=What_file))

ft.app(main)