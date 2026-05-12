import os
import glob

html_files = glob.glob(r"c:\Users\yashg\OneDrive\Desktop\CodeAlpha\Social media app\xyz\socialvibe\App\Templates\*.html")

for file in html_files:
    if "login.html" in file:
        continue
    with open(file, "r", encoding="utf-8") as f:
        content = f.read()
        
    old_text = '<a href="#" class="sidebar-link"><i class="bi bi-gear"></i> Settings</a>'
    new_text = '<a href="{% url \'settings\' %}" class="sidebar-link"><i class="bi bi-gear"></i> Settings</a>'
    content = content.replace(old_text, new_text)
    
    with open(file, "w", encoding="utf-8") as f:
        f.write(content)

print("Done updating settings link")
