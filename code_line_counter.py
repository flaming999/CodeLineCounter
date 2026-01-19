#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path
from collections import defaultdict

# ========================
# Internationalization Support
#  (i18n) 
# ========================

# Current language
_CURRENT_LANG = "chs"

# Translation dictionary: supported languages and their translations
_TRANSLATIONS = {
    "en": {
        "Code Line Counter": "Code Line Counter",
        "Total": "Total",
        "Files": "Files",
        "Total Lines": "Total Lines",
        "Code Lines": "Code Lines",
        "Comment Lines": "Comment Lines",
        "Blank Lines": "Blank Lines",
        "Code Line Ratio": "Code Line Ratio",
        "Comment Line Ratio": "Comment Line Ratio",
        "Blank Line Ratio": "Blank Line Ratio",
        "Failed to read file": "Failed to read file",
        "Code Line Statistics Results": "Code Line Statistics Results",
        "File Count": "File Count",
    },
    "chs": {
        "Code Line Counter": "代码行数统计工具",
        "Total": "总计",
        "Files": "文件数量",
        "Total Lines": "总行数",
        "Code Lines": "代码行",
        "Comment Lines": "注释行",
        "Blank Lines": "空行",
        "Code Line Ratio": "代码行占比",
        "Comment Line Ratio": "注释行占比",
        "Blank Line Ratio": "空行占比",
        "Failed to read file": "读取文件失败",
        "Code Line Statistics Results": "代码行数统计结果",
        "File Count": "文件数量",
    },
    "cht": {
        "Code Line Counter": "程式碼行數統計工具",
        "Total": "總計",
        "Files": "檔案數量",
        "Total Lines": "總行數",
        "Code Lines": "程式碼行",
        "Comment Lines": "註解行",
        "Blank Lines": "空白行",
        "Code Line Ratio": "程式碼行佔比",
        "Comment Line Ratio": "註解行佔比",
        "Blank Line Ratio": "空白行佔比",
        "Failed to read file": "讀取檔案失敗",
        "Code Line Statistics Results": "程式碼行數統計結果",
        "File Count": "檔案數量",
    },
    "ja": {
        "Code Line Counter": "コード行数カウンター",
        "Total": "合計",
        "Files": "ファイル数",
        "Total Lines": "総行数",
        "Code Lines": "コード行",
        "Comment Lines": "コメント行",
        "Blank Lines": "空白行",
        "Code Line Ratio": "コード行の割合",
        "Comment Line Ratio": "コメント行の割合",
        "Blank Line Ratio": "空白行の割合",
        "Failed to read file": "ファイルの読み取りに失敗しました",
        "Code Line Statistics Results": "コード行数統計結果",
        "File Count": "ファイル数",
    }
}

def i18n_setlang(lang_code):
    """lang_code: 'en' 或 'chs'"""
    global _CURRENT_LANG
    if lang_code in _TRANSLATIONS:
        _CURRENT_LANG = lang_code
    else:
        print(f"Warning: Language '{lang_code}' not supported. Using '{_CURRENT_LANG}'.")

def _t(key):
    """translation function"""
    trans_dict = _TRANSLATIONS.get(_CURRENT_LANG, _TRANSLATIONS["en"])
    return trans_dict.get(key, key) 

# ========================
# Code Line Counter Logic
# ========================

class CodeLineCounter:
    def __init__(self):
        self.language_configs = {
            'python': {
                'extensions': ['.py'],
                'line_comment': '#',
                'block_comment_start': None,
                'block_comment_end': None
            },
            'java': {
                'extensions': ['.java'],
                'line_comment': '//',
                'block_comment_start': '/*',
                'block_comment_end': '*/'
            },
            'cpp': {
                'extensions': ['.cpp', '.cc', '.cxx', '.c', '.h', '.hpp', '.hh', '.hxx'],
                'line_comment': '//',
                'block_comment_start': '/*',
                'block_comment_end': '*/'
            },
            'go': {
                'extensions': ['.go'],
                'line_comment': '//',
                'block_comment_start': '/*',
                'block_comment_end': '*/'
            },
            'javascript': {
                'extensions': ['.js', '.jsx', '.ts', '.tsx'],
                'line_comment': '//',
                'block_comment_start': '/*',
                'block_comment_end': '*/'
            },
            'html': {
                'extensions': ['.html', '.htm'],
                'line_comment': None,
                'block_comment_start': '<!--',
                'block_comment_end': '-->'
            },
            'css': {
                'extensions': ['.css'],
                'line_comment': None,
                'block_comment_start': '/*',
                'block_comment_end': '*/'
            }
        }

        self.stats = defaultdict(lambda: {
            'files': 0,
            'total_lines': 0,
            'code_lines': 0,
            'comment_lines': 0,
            'blank_lines': 0
        })

        self.total_stats = {
            'files': 0,
            'total_lines': 0,
            'code_lines': 0,
            'comment_lines': 0,
            'blank_lines': 0
        }

    def get_language_by_extension(self, extension):
        for lang, config in self.language_configs.items():
            if extension.lower() in config['extensions']:
                return lang
        return None

    def is_blank_line(self, line):
        return line.strip() == ''

    def count_lines_in_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"{_t('Failed to read file')} {file_path}: {e}")
            return None

        total_lines = len(lines)
        blank_lines = 0
        comment_lines = 0
        code_lines = 0

        extension = Path(file_path).suffix
        language = self.get_language_by_extension(extension)

        if not language:
            return None

        config = self.language_configs[language]
        in_block_comment = False

        for line in lines:
            stripped_line = line.strip()

            if self.is_blank_line(line):
                blank_lines += 1
                continue

            if config['block_comment_start'] and config['block_comment_end']:
                start = config['block_comment_start']
                end = config['block_comment_end']

                if start in stripped_line and end in stripped_line:
                    comment_lines += 1
                    continue

                if start in stripped_line and not in_block_comment:
                    in_block_comment = True
                    comment_lines += 1
                    continue

                if end in stripped_line and in_block_comment:
                    in_block_comment = False
                    comment_lines += 1
                    continue

                if in_block_comment:
                    comment_lines += 1
                    continue

            line_comment = config['line_comment']
            if line_comment and stripped_line.startswith(line_comment):
                comment_lines += 1
                continue

            code_lines += 1

        return {
            'language': language,
            'total_lines': total_lines,
            'code_lines': code_lines,
            'comment_lines': comment_lines,
            'blank_lines': blank_lines
        }

    def scan_directory(self, directory_path, exclude_dirs=None, include_extensions=None):
        if exclude_dirs is None:
            exclude_dirs = {'.git', '__pycache__', 'node_modules', '.vscode', '.idea'}

        directory = Path(directory_path)

        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            for file in files:
                file_path = Path(root) / file
                extension = file_path.suffix

                if include_extensions and extension.lower() not in include_extensions:
                    continue

                result = self.count_lines_in_file(file_path)
                if result:
                    lang = result['language']
                    self.stats[lang]['files'] += 1
                    self.stats[lang]['total_lines'] += result['total_lines']
                    self.stats[lang]['code_lines'] += result['code_lines']
                    self.stats[lang]['comment_lines'] += result['comment_lines']
                    self.stats[lang]['blank_lines'] += result['blank_lines']

                    self.total_stats['files'] += 1
                    self.total_stats['total_lines'] += result['total_lines']
                    self.total_stats['code_lines'] += result['code_lines']
                    self.total_stats['comment_lines'] += result['comment_lines']
                    self.total_stats['blank_lines'] += result['blank_lines']

    def print_statistics(self):
        print("=" * 80)
        print(_t("Code Line Statistics Results"))
        print("=" * 80)

        for language in sorted(self.stats.keys()):
            stats = self.stats[language]
            if stats['files'] > 0:
                print(f"\n{language.upper()}:")
                print(f"  {_t('File Count')}: {stats['files']}")
                print(f"  {_t('Total Lines')}: {stats['total_lines']}")
                print(f"  {_t('Code Lines')}: {stats['code_lines']}")
                print(f"  {_t('Comment Lines')}: {stats['comment_lines']}")
                print(f"  {_t('Blank Lines')}: {stats['blank_lines']}")

                if stats['total_lines'] > 0:
                    code_percent = (stats['code_lines'] / stats['total_lines']) * 100
                    comment_percent = (stats['comment_lines'] / stats['total_lines']) * 100
                    blank_percent = (stats['blank_lines'] / stats['total_lines']) * 100
                    print(f"  {_t('Code Line Ratio')}: {code_percent:.1f}%")
                    print(f"  {_t('Comment Line Ratio')}: {comment_percent:.1f}%")
                    print(f"  {_t('Blank Line Ratio')}: {blank_percent:.1f}%")

        print("\n" + "=" * 80)
        print(f"{_t('Total')}:")
        print(f"  {_t('Files')}: {self.total_stats['files']}")
        print(f"  {_t('Total Lines')}: {self.total_stats['total_lines']}")
        print(f"  {_t('Code Lines')}: {self.total_stats['code_lines']}")
        print(f"  {_t('Comment Lines')}: {self.total_stats['comment_lines']}")
        print(f"  {_t('Blank Lines')}: {self.total_stats['blank_lines']}")

        if self.total_stats['total_lines'] > 0:
            total_code_percent = (self.total_stats['code_lines'] / self.total_stats['total_lines']) * 100
            total_comment_percent = (self.total_stats['comment_lines'] / self.total_stats['total_lines']) * 100
            total_blank_percent = (self.total_stats['blank_lines'] / self.total_stats['total_lines']) * 100
            print(f"  {_t('Code Line Ratio')}: {total_code_percent:.1f}%")
            print(f"  {_t('Comment Line Ratio')}: {total_comment_percent:.1f}%")
            print(f"  {_t('Blank Line Ratio')}: {total_blank_percent:.1f}%")

def main():
    import argparse

    parser = argparse.ArgumentParser(description=_t("Code Line Counter"))
    parser.add_argument('path', nargs='?', default='.', help='Directory path to analyze (default: current)')
    parser.add_argument('-e', '--exclude', nargs='+', help='Directories to exclude')
    parser.add_argument('-i', '--include', nargs='+', help='Only include these file extensions')
    parser.add_argument('--lang', choices=['en', 'chs', 'cht', 'ja'], default='en', help='Language (en/chs/cht/ja)')

    args = parser.parse_args()

    # Set language for i18n
    i18n_setlang(args.lang)

    include_extensions = None
    if args.include:
        include_extensions = [ext.lower() if ext.startswith('.') else f'.{ext.lower()}' 
                            for ext in args.include]

    counter = CodeLineCounter()
    counter.scan_directory(args.path, args.exclude, include_extensions)
    counter.print_statistics()

if __name__ == '__main__':
    main()
