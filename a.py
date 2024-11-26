from bs4 import BeautifulSoup

def split_html(html_content, max_len=4096):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Преобразуем содержимое в строку
    raw_html = str(soup)
    
    # Если длина сообщения меньше или равна max_len, возвращаем его как есть
    if len(raw_html) <= max_len:
        return [raw_html]
    
    fragments = []
    start = 0
    
    while start < len(raw_html):
        end = start + max_len
        
        # Если разрыв не в пределах длины, ищем место для разрыва
        if end < len(raw_html):
            # Ищем ближайший закрывающий тег
            close_tag_pos = raw_html.rfind('>', start, end)
            if close_tag_pos == -1:
                close_tag_pos = end  # В случае если не нашли, просто режем на max_len символов
        else:
            close_tag_pos = len(raw_html)
        
        # Проверяем, что закрывающий тег не является частью атрибута
        if raw_html[close_tag_pos-1] == '=':
            close_tag_pos = raw_html.find('>', close_tag_pos)
        
        # Формируем фрагмент и добавляем его в список
        fragment = raw_html[start:close_tag_pos + 1]  # Включаем закрывающий тег
        fragments.append(fragment)
        
        start = close_tag_pos + 1  # Устанавливаем новую точку начала для следующего фрагмента
    
    # Проверяем, что все фрагменты корректно закрыты
    for i in range(len(fragments)):
        fragments[i] = str(BeautifulSoup(fragments[i], 'html.parser'))  # Перезаписываем с корректно закрытыми тегами
        
        # Убираем пустые теги
        fragment_soup = BeautifulSoup(fragments[i], 'html.parser')
        for tag in fragment_soup.find_all():
            if tag.name == 'a' and not tag.get_text(strip=True):
                tag.decompose()  # Убираем пустые теги <a></a>
        fragments[i] = str(fragment_soup)

    return fragments

# Пример с ограничением на 500 символов
html_message = """<strong>🕒 Some tasks are missing worklogs!</strong>
<mention id="U1024">Justin Kirvin</mention>
Here is the list of tasks that have been in status without worklogs for more than <strong>1h</strong> :arrow_down:

<a href="tg://user?id=3485734953">Talbert Gannaway</a>
<strong>In progress</strong>
<a href="https://mockdata.atlassian.net/browse/ABC-12634"><code>ABC-12634</code></a> Lorem ipsum dolor sit amet, consectetur adipiscing elit.
...
<a href="https://mockdata.atlassian.net/browse/ABC-12408"><code>ABC-12408</code></a> Nullam tincidunt vulputate nibh a placerat."""

# Получаем фрагменты
fragments = split_html(html_message, max_len=500)

# Вывод фрагментов
for i, fragment in enumerate(fragments):
    print(f"Фрагмент {i+1}:\n{fragment}\n")
