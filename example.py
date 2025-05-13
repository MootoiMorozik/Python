def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS # Указывает на папку в Temp где и должны лежать ресурсы.
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, "files", relative_path) # Нужно указать папку с ресурсами
# Тоесть если ты хочешь чтобы были ресурсы в папке - нужно указать это в самом Pyinstaller
# команда для конвертации:
# pyinstaller --noconfirm --onefile --windowed --add-data "C:\FOLDER;FOLDER/" -(это путь к папке где лежат ресурсы)  "C:\Users\Noortle\Desktop\script.py" - (скрипт)
# Проще всего использовать auto-py-to-exe (pip install auto-py-to-exe, в cmd/powershell после установки введите auto-py-to-exe
# Там будет Additional Files, выбираете "Add Folder" и у вас изменится команда для pyinstaller
#
#
# Рассмотрим пример
# background = pygame.image.load(resource_path("yourimage.png")) Я использовал пример pygame, по желанию можете поменять. resource_path - отсылает
# на def resource_path(relative_path).
#
#
#
# Туториал написан @MootoiMoroz1k
# github.com/mootoimorozik