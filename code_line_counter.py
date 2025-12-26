#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path
from collections import defaultdict

class CodeLineCounter:
    def __init__(self):
        # 定义不同语言的文件扩展名和注释符号
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
        
        # 统计结果
        self.stats = defaultdict(lambda: {
            'files': 0,
            'total_lines': 0,
            'code_lines': 0,
            'comment_lines': 0,
            'blank_lines': 0
        })
        
        # 总体统计
        self.total_stats = {
            'files': 0,
            'total_lines': 0,
            'code_lines': 0,
            'comment_lines': 0,
            'blank_lines': 0
        }

    def get_language_by_extension(self, extension):
        """根据文件扩展名判断编程语言"""
        for lang, config in self.language_configs.items():
            if extension.lower() in config['extensions']:
                return lang
        return None

    def is_blank_line(self, line):
        """判断是否为空行"""
        return line.strip() == ''

    def count_lines_in_file(self, file_path):
        """统计单个文件的行数"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"读取文件 {file_path} 失败: {e}")
            return None

        total_lines = len(lines)
        blank_lines = 0
        comment_lines = 0
        code_lines = 0
        
        # 获取文件语言类型
        extension = Path(file_path).suffix
        language = self.get_language_by_extension(extension)
        
        if not language:
            return None
            
        config = self.language_configs[language]
        
        # 简化的行统计（不处理复杂的嵌套注释）
        in_block_comment = False
        
        for line in lines:
            stripped_line = line.strip()
            
            # 空行
            if self.is_blank_line(line):
                blank_lines += 1
                continue
            
            # 检查块注释开始和结束
            if config['block_comment_start'] and config['block_comment_end']:
                # 检查是否有完整的块注释 /* ... */
                if config['block_comment_start'] in stripped_line and \
                   config['block_comment_end'] in stripped_line:
                    comment_lines += 1
                    continue
                
                # 块注释开始
                if config['block_comment_start'] in stripped_line and not in_block_comment:
                    in_block_comment = True
                    comment_lines += 1
                    continue
                
                # 块注释结束
                if config['block_comment_end'] in stripped_line and in_block_comment:
                    in_block_comment = False
                    comment_lines += 1
                    continue
                
                # 在块注释中
                if in_block_comment:
                    comment_lines += 1
                    continue
            
            # 行注释
            line_comment = config['line_comment']
            if line_comment and stripped_line.startswith(line_comment):
                comment_lines += 1
                continue
            
            # 代码行
            code_lines += 1
        
        return {
            'language': language,
            'total_lines': total_lines,
            'code_lines': code_lines,
            'comment_lines': comment_lines,
            'blank_lines': blank_lines
        }

    def scan_directory(self, directory_path, exclude_dirs=None, include_extensions=None):
        """扫描目录中的所有文件"""
        if exclude_dirs is None:
            exclude_dirs = {'.git', '__pycache__', 'node_modules', '.vscode', '.idea'}
        
        directory = Path(directory_path)
        
        for root, dirs, files in os.walk(directory):
            # 排除指定目录
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                file_path = Path(root) / file
                extension = file_path.suffix
                
                # 如果指定了包含的扩展名，则只处理这些扩展名
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
                    
                    # 更新总体统计
                    self.total_stats['files'] += 1
                    self.total_stats['total_lines'] += result['total_lines']
                    self.total_stats['code_lines'] += result['code_lines']
                    self.total_stats['comment_lines'] += result['comment_lines']
                    self.total_stats['blank_lines'] += result['blank_lines']

    def print_statistics(self):
        """打印统计结果"""
        print("=" * 80)
        print("代码行数统计结果")
        print("=" * 80)
        
        # 按语言显示统计
        for language in sorted(self.stats.keys()):
            stats = self.stats[language]
            if stats['files'] > 0:
                print(f"\n{language.upper()}:")
                print(f"  文件数量: {stats['files']}")
                print(f"  总行数: {stats['total_lines']}")
                print(f"  代码行: {stats['code_lines']}")
                print(f"  注释行: {stats['comment_lines']}")
                print(f"  空行: {stats['blank_lines']}")
                
                if stats['total_lines'] > 0:
                    code_percent = (stats['code_lines'] / stats['total_lines']) * 100
                    comment_percent = (stats['comment_lines'] / stats['total_lines']) * 100
                    blank_percent = (stats['blank_lines'] / stats['total_lines']) * 100
                    print(f"  代码行占比: {code_percent:.1f}%")
                    print(f"  注释行占比: {comment_percent:.1f}%")
                    print(f"  空行占比: {blank_percent:.1f}%")
        
        # 显示总计
        print("\n" + "=" * 80)
        print("总计:")
        print(f"  文件总数: {self.total_stats['files']}")
        print(f"  总行数: {self.total_stats['total_lines']}")
        print(f"  代码行总数: {self.total_stats['code_lines']}")
        print(f"  注释行总数: {self.total_stats['comment_lines']}")
        print(f"  空行总数: {self.total_stats['blank_lines']}")
        
        if self.total_stats['total_lines'] > 0:
            total_code_percent = (self.total_stats['code_lines'] / self.total_stats['total_lines']) * 100
            total_comment_percent = (self.total_stats['comment_lines'] / self.total_stats['total_lines']) * 100
            total_blank_percent = (self.total_stats['blank_lines'] / self.total_stats['total_lines']) * 100
            print(f"  代码行总占比: {total_code_percent:.1f}%")
            print(f"  注释行总占比: {total_comment_percent:.1f}%")
            print(f"  空行总占比: {total_blank_percent:.1f}%")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='代码行数统计工具')
    parser.add_argument('path', nargs='?', default='.', help='要统计的目录路径，默认为当前目录')
    parser.add_argument('-e', '--exclude', nargs='+', help='排除的目录名称')
    parser.add_argument('-i', '--include', nargs='+', help='只包含指定的文件扩展名')
    
    args = parser.parse_args()
    
    # 转换包含的扩展名为小写
    include_extensions = None
    if args.include:
        include_extensions = [ext.lower() if ext.startswith('.') else f'.{ext.lower()}' 
                            for ext in args.include]
    
    counter = CodeLineCounter()
    counter.scan_directory(args.path, args.exclude, include_extensions)
    counter.print_statistics()

if __name__ == '__main__':
    main()
