import flet as ft
import urllib.request
import os
import re

def main(page: ft.Page):
    def is_google_drive_link(url):
        # Проверяем, является ли строка ссылкой на Google Диск
        return re.match(r'https?://drive\.google\.com/', url) is not None

    def download_from_google_drive(url):
        try:
            # Преобразуем ссылку на Google Диск в прямую ссылку для скачивания
            file_id = re.search(r'/file/d/([a-zA-Z0-9_-]+)', url)
            if file_id:
                file_id = file_id.group(1)
                direct_url = f"https://drive.google.com/uc?export=download&id={file_id}"
                
                # Скачиваем файл во временную папку
                temp_file = os.path.join(os.getcwd(), "temp_downloaded_file")
                urllib.request.urlretrieve(direct_url, temp_file)
                return temp_file
            return None
        except Exception as e:
            print(f"Ошибка при загрузке файла: {e}")
            return None

    def What_file(e):
        if not Name_file.value:
            Name_file.error_text = "Пожалуйста, введите имя файла или ссылку"
            page.update()
        else:
            name = Name_file.value
            page.clean()
            
            try:
                # Проверяем, является ли ввод ссылкой на Google Диск
                if is_google_drive_link(name):
                    page.add(ft.Text(value="Обнаружена ссылка на Google Диск. Загружаем...", color="blue"))
                    page.update()
                    
                    temp_file = download_from_google_drive(name)
                    if temp_file:
                        try:
                            with open(temp_file, 'r', encoding='utf-8') as f:  
                                page.add(ft.Text(value="Файл успешно загружен с Google Диска", color="green"))
                                content = f.read()
                                page.add(ft.Text(value=content, color="white"))
                        finally:
                            # Удаляем временный файл после использования
                            os.remove(temp_file)
                    else:
                        page.add(ft.Text(value="Не удалось загрузить файл с Google Диска", color="red"))
                else:
                    # Обрабатываем как локальный файл
                    with open(name, 'r', encoding='utf-8') as f:  
                        page.add(ft.Text(value="Локальный файл открыт", color="green"))
                        content = f.read()
                        page.add(ft.Text(value=content, color="white"))
            except FileNotFoundError:
                page.add(ft.Text(value="Файл не найден или его не существует", color="red"))
            except Exception as e:
                page.add(ft.Text(value=f"Произошла ошибка: {e}", color="red"))
            page.update() 

    Name_file = ft.TextField(label="Имя файла или ссылка на Google Диск")
    page.add(Name_file, ft.ElevatedButton('Открыть файл', on_click=What_file))

ft.app(main)