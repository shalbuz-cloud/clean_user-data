from pathlib import Path
import shutil
from datetime import datetime
import logging

# logger
date = datetime.date(datetime.now()).strftime('%d-%m-%Y')
try:
    new_directory = Path('./logs/')
    if not new_directory.exists():
        new_directory.mkdir()
except OSError as error:
    print('[ERROR] %s' % error)
logging.basicConfig(filename='./logs/%s.log' % date,
                    level=logging.ERROR,
                    format='%(asctime)s %(levelname)s: %(message)s'
                    )

users_dir = Path.home().resolve().parent
exclusions = [
    'Default', 'Default User', 'Public', 'All Users', 'Все пользователи', 'Гость', 'Администратор',
    'USR1CV8', 'Общие'
]

watch_list = [
    'Мои документы', 'Videos', 'Pictures', 'Music', 'Downloads', 'Documents', 'Desktop',
    'Загрузки', 'Рабочий стол', 'Музыка', 'Видео'
]

users = [
    users_dir / i.name for i in Path(users_dir).glob('*')
    if i.name not in exclusions and i.is_dir()
]

data = {}
for user in users:
    dirs = [i for i in Path(user).glob('*') if i.name in watch_list and i.is_dir()]

    delete_count = 0

    for dir_path in dirs:
        for i in Path(dir_path).glob('*'):
            i_name = i.is_dir()
            try:
                if i.is_dir():
                    i_name = 'Каталог'
                    shutil.rmtree(i)
                else:
                    i_name = 'Файл'
                    if i.suffix == '.lnk':
                        continue
                    i.unlink()
            except PermissionError as error:
                logging.warning('%s | %s\n' % (i, error.strerror))
            except OSError as error:
                logging.error('%s | %s\n' % (i, error.strerror))
            else:
                logging.info('%s "%s" успешно удален\n' % (i_name, i))
                delete_count += 1

    data[user.name] = delete_count

try:
    new_directory = Path('./stat/')
    if not new_directory.exists():
        new_directory.mkdir()

    stamp = datetime.time(datetime.now()).strftime('%H:%M')
    with open('./stat/%s.txt' % date, 'a', encoding='utf-8') as file:
        file.write('Количество удаленных файлов [%s]\n' % stamp)
        for k, v in data.items():
            file.write('%s: %s\n' % (k, v))
        file.write('-' * 30 + '\n')
except OSError as error:
    logging.error(error)
