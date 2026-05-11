#!/usr/bin/env python3
"""
Script to add light theme and theme toggle functionality to all template files
"""

import os
import re

# Light theme CSS variables to add
LIGHT_THEME_CSS = """
        /* Light theme variables */
        [data-theme="light"] {
            --bg-dark: #F8FAFC;
            --bg-darker: #F1F5F9;
            --bg-card: #FFFFFF;
            --text-light: #1E293B;
            --text-muted: #64748B;
            --text-dark: #F8FAFC;
            --border-color: #E2E8F0;
            --shadow-glow: 0 0 20px rgba(139, 92, 246, 0.2);
            --shadow-card: 0 10px 25px rgba(0, 0, 0, 0.1);
        }

        [data-theme="light"] body::before {
            background: 
                radial-gradient(circle at 20% 80%, rgba(139, 92, 246, 0.05) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(59, 130, 246, 0.05) 0%, transparent 50%),
                radial-gradient(circle at 40% 40%, rgba(124, 58, 237, 0.03) 0%, transparent 50%);
        }

        [data-theme="light"] .header {
            background: rgba(248, 250, 252, 0.8);
            border-bottom: 1px solid var(--border-color);
        }

        /* Theme Toggle Button */
        .theme-toggle {
            position: relative;
            width: 60px;
            height: 30px;
            background: var(--border-color);
            border-radius: 15px;
            cursor: pointer;
            transition: all 0.3s ease;
            border: none;
            outline: none;
            display: flex;
            align-items: center;
            padding: 0 3px;
        }

        .theme-toggle:hover {
            background: var(--primary-purple);
        }

        .theme-toggle-slider {
            width: 24px;
            height: 24px;
            background: var(--text-light);
            border-radius: 50%;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            color: var(--bg-dark);
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }

        [data-theme="light"] .theme-toggle-slider {
            transform: translateX(30px);
        }

        .theme-toggle-icon {
            transition: all 0.3s ease;
        }

        [data-theme="light"] .theme-toggle-icon {
            transform: rotate(180deg);
        }
"""

# Theme toggle button HTML
THEME_TOGGLE_HTML = """                            <button class="theme-toggle" id="themeToggle" onclick="toggleTheme()" title="Toggle Light/Dark Theme">
                                <div class="theme-toggle-slider">
                                    <i class="fas fa-moon theme-toggle-icon"></i>
                                </div>
                            </button>"""

# Theme toggle JavaScript
THEME_TOGGLE_JS = """
        // Theme Toggle Functionality
        function toggleTheme() {
            const body = document.body;
            const currentTheme = body.getAttribute('data-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            
            body.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            
            // Update toggle button icon
            const icon = document.querySelector('.theme-toggle-icon');
            if (newTheme === 'light') {
                icon.className = 'fas fa-sun theme-toggle-icon';
            } else {
                icon.className = 'fas fa-moon theme-toggle-icon';
            }
        }

        // Initialize theme on page load
        function initializeTheme() {
            const savedTheme = localStorage.getItem('theme') || 'dark';
            const body = document.body;
            const icon = document.querySelector('.theme-toggle-icon');
            
            body.setAttribute('data-theme', savedTheme);
            
            if (savedTheme === 'light') {
                icon.className = 'fas fa-sun theme-toggle-icon';
            } else {
                icon.className = 'fas fa-moon theme-toggle-icon';
            }
        }

        // Initialize theme when page loads
        document.addEventListener('DOMContentLoaded', initializeTheme);"""

def add_light_theme_to_template(file_path):
    """Add light theme CSS to a template file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if light theme is already added
        if '[data-theme="light"]' in content:
            print(f"Light theme already exists in {file_path}")
            return False
        
        # Find the end of the :root CSS block
        root_pattern = r'(\s*--shadow-card: 0 10px 25px rgba\(0, 0, 0, 0\.2\);\s*)(\s*})'
        match = re.search(root_pattern, content)
        
        if match:
            # Insert light theme CSS after the :root block
            new_content = content[:match.end(1)] + LIGHT_THEME_CSS + content[match.start(2):]
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"Added light theme CSS to {file_path}")
            return True
        else:
            print(f"Could not find :root block in {file_path}")
            return False
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def add_theme_toggle_to_header(file_path):
    """Add theme toggle button to the header"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if theme toggle already exists
        if 'theme-toggle' in content:
            print(f"Theme toggle already exists in {file_path}")
            return False
        
        # Find header navigation area and add theme toggle
        # Look for common header patterns
        patterns = [
            r'(<div class="col-md-6 text-end">\s*<a[^>]*>.*?</a>\s*</div>)',
            r'(<div class="col-md-6">\s*<a[^>]*>.*?</a>\s*</div>)',
            r'(<div class="col-md-6">\s*<ul[^>]*>.*?</ul>\s*</div>)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.DOTALL)
            if match:
                # Replace with theme toggle version
                old_div = match.group(1)
                new_div = old_div.replace('text-end', '').replace('</div>', f'\n                            {THEME_TOGGLE_HTML}\n                        </div>')
                new_div = new_div.replace('<div class="col-md-6">', '<div class="col-md-6">\n                        <div class="d-flex align-items-center justify-content-end gap-3">')
                
                content = content.replace(old_div, new_div)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"Added theme toggle to header in {file_path}")
                return True
        
        print(f"Could not find suitable header pattern in {file_path}")
        return False
        
    except Exception as e:
        print(f"Error adding theme toggle to {file_path}: {e}")
        return False

def add_theme_js_to_template(file_path):
    """Add theme toggle JavaScript to a template file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if theme JS already exists
        if 'toggleTheme()' in content:
            print(f"Theme JavaScript already exists in {file_path}")
            return False
        
        # Find the end of existing script or before closing body tag
        script_pattern = r'(\s*</script>\s*</body>)'
        match = re.search(script_pattern, content)
        
        if match:
            # Insert theme JS before closing script tag
            new_content = content[:match.start(1)] + THEME_TOGGLE_JS + content[match.start(1):]
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"Added theme JavaScript to {file_path}")
            return True
        else:
            # Try to add before closing body tag
            body_pattern = r'(\s*</body>)'
            match = re.search(body_pattern, content)
            
            if match:
                new_content = content[:match.start(1)] + f'    <script>{THEME_TOGGLE_JS}\n    </script>\n' + content[match.start(1):]
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"Added theme JavaScript to {file_path}")
                return True
            else:
                print(f"Could not find suitable location for JavaScript in {file_path}")
                return False
                
    except Exception as e:
        print(f"Error adding JavaScript to {file_path}: {e}")
        return False

def main():
    """Main function to process all template files"""
    templates_dir = 'templates'
    template_files = [
        'result.html',
        'reports.html', 
        'doctor_interface.html',
        'debug.html'
    ]
    
    for template_file in template_files:
        file_path = os.path.join(templates_dir, template_file)
        
        if os.path.exists(file_path):
            print(f"\nProcessing {template_file}...")
            
            # Add light theme CSS
            add_light_theme_to_template(file_path)
            
            # Add theme toggle to header
            add_theme_toggle_to_header(file_path)
            
            # Add theme JavaScript
            add_theme_js_to_template(file_path)
        else:
            print(f"Template file {template_file} not found")

if __name__ == '__main__':
    main()

