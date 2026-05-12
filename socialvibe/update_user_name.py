import os
import glob

html_files = glob.glob(r"c:\Users\yashg\OneDrive\Desktop\CodeAlpha\Social media app\xyz\socialvibe\App\Templates\*.html")

for file in html_files:
    if "login.html" in file:
        continue
    with open(file, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Replace Emma Johnson
    content = content.replace(">Emma Johnson<", ">{{ current_user.fullname }}<")
    content = content.replace("Emma Johnson", "{{ current_user.fullname }}")
    
    # Replace handle
    content = content.replace("@emma.j", "@{{ current_user.fullname|slugify }}")
    
    # Replace placeholder
    content = content.replace("What's on your mind, Emma?", "What's on your mind, {{ current_user.fullname }}?")
    
    with open(file, "w", encoding="utf-8") as f:
        f.write(content)

print("Done updating user details in templates")
