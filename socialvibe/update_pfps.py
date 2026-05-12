import os
import glob

html_files = glob.glob(r"c:\Users\yashg\OneDrive\Desktop\CodeAlpha\Social media app\xyz\socialvibe\App\Templates\*.html")

pfp_template = """{% if current_user.profile_picture %}{{ current_user.profile_picture.url }}{% else %}https://i.pravatar.cc/150?img=47{% endif %}"""

for file in html_files:
    if "login.html" in file:
        continue
    with open(file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Replace the hardcoded avatar URL
    # Look for src="https://i.pravatar.cc/150?img=47"
    new_content = content.replace('src="https://i.pravatar.cc/150?img=47"', f'src="{pfp_template}"')
    
    with open(file, "w", encoding="utf-8") as f:
        f.write(new_content)

print("Updated all templates with dynamic profile pictures")
