# Code Line Counter  
*A simple yet powerful tool to count lines of code, comments, and blank lines in your projects.*

## 📊 Overview

Code Line Counter is a lightweight, cross-platform command-line utility written in pure Python. 
It scans your source code directory and provides clear statistics on:
- Total lines
- Code lines
- Comment lines
- Blank lines
  
...along with their respective ratios for quick insight into your codebase.

Supports **multiple languages** via file extensions 

Supports  **internationalization (i18n)** for English, Simplified Chinese, Traditional Chinese, and Japanese.

---

## 🚀 Quick Start

### Simple Usage
```bash
python code_line_counter.py [path]
```
If no path is given, it defaults to the current directory.

### Full Usage
```bash
python code_line_counter.py [-h] [-e EXCLUDE [EXCLUDE ...]] [-i INCLUDE [INCLUDE ...]] [path]
```

#### Positional Arguments
- `path` — Directory to analyze (defaults to current directory)

#### Optional Arguments
- `-h`, `--help` — Show help message and exit  
- `-e EXCLUDE [EXCLUDE ...]`, `--exclude EXCLUDE [EXCLUDE ...]` — Directory names to exclude (e.g., `.git`, `__pycache__`, `node_modules`)  
- `-i INCLUDE [INCLUDE ...]`, `--include INCLUDE [INCLUDE ...]` — Only include files with specified extensions (e.g., `.py .js .ts`)

#### Examples
```bash
# Analyze current directory
python code_line_counter.py

# Analyze a specific project folder
python code_line_counter.py ./my_project

# Exclude virtual environment and cache folders
python code_line_counter.py -e venv __pycache__ .git

# Only count Python and JavaScript files
python code_line_counter.py -i .py .js
```

---

## 🌍 Internationalization (i18n)
- `--lang` [lang_code] 

The output language can be configured in the script by setting `_CURRENT_LANG` to one of:
- `"en"` (English)
- `"chs"` (Simplified Chinese)
- `"cht"` (Traditional Chinese)
- `"ja"` (Japanese)

> 💡 *Note: statistical report adapts to the selected language.*

---

## ✅ Features

- Zero dependencies — runs with standard Python
- Fast recursive scanning with smart file-type detection
- Configurable inclusion/exclusion rules
- Clean, human-readable output
- Ready for automation or CI pipelines

---

## 🛠️ Use Cases

- Monitor codebase size during development  
- Assess documentation/comment coverage  
- Generate reports for code audits  
- Compare implementation styles across teams or projects  

Perfect for developers, tech leads, and open-source maintainers who value clarity and simplicity.

--- 

*No external libraries. Just run it and get results.*
                        
