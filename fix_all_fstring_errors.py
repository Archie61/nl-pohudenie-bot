#!/usr/bin/env python3
"""
Скрипт для исправления ВСЕХ ошибок f-string в проекте
Запусти из корня: python fix_all_fstring_errors.py
"""

import os
import re

def fix_all_fstring_errors(content):
    """Исправляет ВСЕ типы ошибок f-string"""
    
    # Замена 1: f"текст с переменной"
    pattern1 = r'f"([^"]*{[^}]*}[^"]*?)"s*
s*"([^"]*)"'
    content = re.sub(pattern1, r'f"\u0001
\u0002"', content)
    
    # Замена 2: незакрытые f-строки
    lines = content.split('
')
    fixed_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        if line.strip().startswith('f"') and not line.rstrip().endswith('"'):
            full_string = line
            j = i + 1
            
            while j < len(lines):
                full_string += '
' + lines[j]
                if lines[j].rstrip().endswith('"'):
                    break
                j += 1
            
            if '
' in full_string:
                full_string = full_string.replace('f"', 'f"""', 1)
                if full_string.rstrip().endswith('"'):
                    full_string = full_string.rstrip()[:-1] + '"""'
            
            fixed_lines.extend(full_string.split('
'))
            i = j + 1
            continue
        
        fixed_lines.append(line)
        i += 1
    
    content = '
'.join(fixed_lines)
    
    content = re.sub(
        r'f"([^"]*?)"s*
s*"([^"]*?)"',
        lambda m: f'f"{m.group(1)}
{m.group(2)}"',
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
            return False
    except Exception as e:
        print(f"❌ Ошибка в {filepath}: {e}")
        return False

def main():
    """Основная функция"""
    project_root = os.path.dirname(os.path.abspath(__file__))
    handlers_dir = os.path.join(project_root, 'src', 'handlers')
    main_py = os.path.join(project_root, 'src', 'main.py')
    
    fixed_count = 0
    
    if os.path.exists(handlers_dir):
        for filename in sorted(os.listdir(handlers_dir)):
            if filename.endswith('.py'):
                filepath = os.path.join(handlers_dir, filename)
                if process_file(filepath):
                    fixed_count += 1
    
    if os.path.exists(main_py):
        if process_file(main_py):
            fixed_count += 1
    
    print(f"✨ Всего исправлено: {fixed_count}")

if __name__ == '__main__':
    main()
