#!/usr/bin/env python3
"""
Скрипт для исправления ВСЕХ ошибок f-string в проекте
Запусти из корня: python fix_all_fstring_errors.py
"""

import os
import re

def fix_all_fstring_errors(content):
    """Исправляет ВСЕ типы ошибок f-string"""
    
    # Замена 1: f"текст\n\n\n\n"текст -> f"текст\n" "текст"
    # Паттерн: f"...переменная..."\n+spaces"...текст
    pattern1 = r'f"([^"]*\{[^}]*\}[^"]*?)"\s*\n\s*"([^"]*)"'
    content = re.sub(pattern1, r'f"\1\n\2"', content)
    
    # Замена 2: f"эмодзи текст (без закрывающей кавычки в конце строки)
    # Ищем строки вида: f"🏪 Товары в категории:**
    lines = content.split('\n')
    fixed_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Проверяем, если это f-строка, начинающаяся с f" и содержит эмодзи или текст
        # но НЕ заканчивается на кавычку
        if line.strip().startswith('f"') and not line.rstrip().endswith('"'):
            # Это незакрытая f-string
            # Ищем где она закрывается
            full_string = line
            j = i + 1
            
            # Собираем всю многострочную строку
            while j < len(lines):
                full_string += '\n' + lines[j]
                if lines[j].rstrip().endswith('"'):
                    break
                j += 1
            
            # Теперь нужно убедиться что это правильно объединено
            # Заменяем двойные кавычки на тройные если это многострочная строка
            if '\n' in full_string:
                # Замена f" на f""" (тройные кавычки для многострочной строки)
                full_string = full_string.replace('f"', 'f"""', 1)  # Только первый раз
                # Заменяем последнюю закрывающую кавычку на тройную
                if full_string.rstrip().endswith('"'):
                    # Найди последнюю кавычку и замени на тройную
                    full_string = full_string.rstrip()[:-1] + '"""'
            
            fixed_lines.extend(full_string.split('\n'))
            i = j + 1
            continue
        
        fixed_lines.append(line)
        i += 1
    
    content = '\n'.join(fixed_lines)
    
    # Замена 3: Убедиться что все строки корректны
    # Найти и исправить отдельные случаи
    content = re.sub(
        r'f"([^"]*?)"\s*\n\s*"([^"]*?)"',
        lambda m: f'f"{m.group(1)}\n{m.group(2)}"',
        content
    )
    
    return content

def process_file(filepath):
    """Обрабатывает один Python файл"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        content = fix_all_fstring_errors(content)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Исправлен: {filepath}")
            return True
        else:
            print(f"⏭️  Без изменений: {filepath}")
            return False
    except Exception as e:
        print(f"❌ Ошибка в {filepath}: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Основная функция"""
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    # Проверяем структуру проекта
    handlers_dir = os.path.join(project_root, 'src', 'handlers')
    main_py = os.path.join(project_root, 'src', 'main.py')
    
    print("🔍 Сканирую все Python файлы...")
    
    fixed_count = 0
    
    # Исправляем все файлы в handlers
    if os.path.exists(handlers_dir):
        print(f"\n📁 Папка handlers: {handlers_dir}")
        for filename in sorted(os.listdir(handlers_dir)):
            if filename.endswith('.py'):
                filepath = os.path.join(handlers_dir, filename)
                if process_file(filepath):
                    fixed_count += 1
    else:
        print(f"⚠️  Папка {handlers_dir} не найдена")
    
    # Исправляем main.py если есть
    if os.path.exists(main_py):
        print(f"\n📄 Файл main.py: {main_py}")
        if process_file(main_py):
            fixed_count += 1
    
    print(f"\n{'='*60}")
    print(f"✨ Всего файлов исправлено: {fixed_count}")
    print(f"{'='*60}")
    print("\n⚠️  После исправления загрузи изменения на GitHub:")
    print("   git add .")
    print("   git commit -m 'Fix f-string syntax errors'")
    print("   git push")

if __name__ == '__main__':
    main()
