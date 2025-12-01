#!/usr/bin/env python3
"""
Скрипт для исправления всех синтаксических ошибок f-string в проекте
Запусти из корня проекта: python fix_errors.py
"""

import os
import re

def fix_fstring_syntax(content):
    """Исправляет ошибки незакрытых f-string"""
    # Ищет паттерн: f"..."\n"...
    # и заменяет на: f"..."\n"..."
    
    # Паттерн 1: f"текст с переменной\n\n\n\n"текст без переменной
    pattern1 = r'f"([^"]*\{[^}]*\}[^"]*)"\n(\s+)"([^"]*)"'
    content = re.sub(pattern1, r'f"\1"\n\2"\3"', content)
    
    # Паттерн 2: Убедиться что все f-строки заканчиваются правильно
    lines = content.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines):
        # Если строка начинается с f" и содержит переменную, но не закрывается
        if 'f"' in line and '{' in line and line.rstrip().endswith('\\'):
            # Продолжение на следующей строке
            if i + 1 < len(lines) and lines[i + 1].strip().startswith('"'):
                # Это многострочная f-строка - нужна тройная кавычка
                line = line.replace('f"', 'f"""').rstrip('\\').rstrip()
                fixed_lines.append(line)
                continue
        
        fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)

def process_file(filepath):
    """Обрабатывает один Python файл"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        content = fix_fstring_syntax(content)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Исправлен: {filepath}")
            return True
        else:
            print(f"⏭️  Пропущен: {filepath}")
            return False
    except Exception as e:
        print(f"❌ Ошибка в {filepath}: {e}")
        return False

def main():
    """Основная функция"""
    project_root = os.path.dirname(os.path.abspath(__file__))
    handlers_dir = os.path.join(project_root, 'src', 'handlers')
    
    # Проверяем наличие папки handlers
    if not os.path.exists(handlers_dir):
        print(f"❌ Папка {handlers_dir} не найдена!")
        return
    
    print(f"🔍 Сканирую: {handlers_dir}")
    
    fixed_count = 0
    for filename in os.listdir(handlers_dir):
        if filename.endswith('.py'):
            filepath = os.path.join(handlers_dir, filename)
            if process_file(filepath):
                fixed_count += 1
    
    # Также проверяем main.py если он есть
    main_py = os.path.join(project_root, 'src', 'main.py')
    if os.path.exists(main_py):
        if process_file(main_py):
            fixed_count += 1
    
    print(f"\n{'='*50}")
    print(f"✨ Всего исправлено файлов: {fixed_count}")
    print(f"{'='*50}")

if __name__ == '__main__':
    main()
