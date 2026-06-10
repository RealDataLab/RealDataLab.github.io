#!/usr/bin/env python3
import os
import re
import sys

def find_project_directories():
    """Finds the base directory containing index.html and pages/."""
    # Check current directory
    if os.path.exists("index.html") and os.path.exists("pages"):
        return "."
    # Check parent directory
    if os.path.exists("../index.html") and os.path.exists("../pages"):
        return ".."
    # Check if we are in the workspace root and RealDataHub.github.io exists
    if os.path.exists("RealDataHub.github.io/index.html") and os.path.exists("RealDataHub.github.io/pages"):
        return "RealDataHub.github.io"
    
    print("Error: Could not locate index.html or pages/ directory.")
    print("Please run this script from the website root directory.")
    sys.exit(1)

def get_next_project_id(base_dir):
    """Finds the highest number XX.html in the pages directory and returns XX + 1."""
    pages_dir = os.path.join(base_dir, "pages")
    max_id = -1
    for filename in os.listdir(pages_dir):
        match = re.match(r"^(\d+)\.html$", filename)
        if match:
            val = int(match.group(1))
            if val > max_id:
                max_id = val
    return max_id + 1

def create_project_pages(base_dir, proj_id, title, desc_paragraphs, app_url, img_filename):
    """Creates the descriptive page (pages/XX.html) and iframe page (pages/XX_app.html)."""
    # 1. Create XX_app.html
    app_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} App</title>
    <style>
        body, html {{
            margin: 0;
            padding: 0;
            height: 100%;
            overflow: hidden;
            background-color: #fff;
        }}
        iframe {{
            width: 100%;
            height: 100%;
            border: none;
            display: block;
        }}
    </style>
</head>
<body>
    <iframe src="{app_url}" title="{title} App" allowfullscreen></iframe>
</body>
</html>
"""
    app_filename = f"{proj_id:02d}_app.html" if proj_id < 100 else f"{proj_id}_app.html"
    app_path = os.path.join(base_dir, "pages", app_filename)
    with open(app_path, "w", encoding="utf-8") as f:
        f.write(app_template)
    print(f"Created: {app_path}")

    # 2. Create XX.html
    desc_html = "\n            ".join(f"<p>{p}</p>" for p in desc_paragraphs)
    
    meta_desc = desc_paragraphs[0][:150] + "..." if len(desc_paragraphs[0]) > 150 else desc_paragraphs[0]
    meta_desc = meta_desc.replace('"', '&quot;')
    
    main_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{meta_desc}">
    <link rel="canonical" href="{app_filename}">
    <link rel="stylesheet" href="../assets/css/styles.css">
    <title>{title}</title>
    <style>
        body {{
            margin: 0;
            padding: 2rem;
            background-color: #fff;
        }}
        .container {{
            max-width: 1024px;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            gap: 2rem;
        }}
        .image-section {{
            width: 100%;
            overflow: hidden;
            border-radius: 0.5rem;
            box-shadow: 0px 4px 25px rgba(14, 36, 49, 0.15);
        }}
        .image-section img {{
            width: 100%;
            height: auto;
            display: block;
            cursor: pointer;
        }}
        .text-section {{
            padding: 2rem;
            line-height: 1.8;
            color: hsl(224, 56%, 12%);
            font-size: 1rem;
        }}
        .text-section p {{
            margin-bottom: 1rem;
        }}
        .text-section p:last-child {{
            margin-bottom: 0;
        }}
        .redirect-notice {{
            text-align: center;
            margin-top: 2rem;
            color: hsl(224, 89%, 60%);
            font-weight: 600;
        }}
        @media screen and (min-width: 768px) {{
            .container {{
                padding: 2rem 0;
            }}
            .text-section {{
                font-size: 1.1rem;
                padding: 2.5rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="text-section">
            {desc_html}
        </div>
        <div class="image-section">
            <img src="../assets/img/{img_filename}" alt="redirect now!" title="do not wait, redirect now to app - {title}" onclick="window.location.href='{app_filename}';">
        </div>
        <div class="redirect-notice" id="notice">
            <p>Click the image above to open the application in full screen.</p>
        </div>
    </div>

    <script>
        // the app is loaded on click
    </script>
</body>
</html>
"""
    main_filename = f"{proj_id:02d}.html" if proj_id < 100 else f"{proj_id}.html"
    main_path = os.path.join(base_dir, "pages", main_filename)
    with open(main_path, "w", encoding="utf-8") as f:
        f.write(main_template)
    print(f"Created: {main_path}")

    return main_filename

def add_card_to_index(base_dir, section_type, page_filename, title, img_filename):
    """Inserts the new card link into index.html inside the specified section."""
    index_path = os.path.join(base_dir, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Determine targets based on section
    if section_type == "analytics":
        section_pattern = r'(<section\s+class="analytic"\s+id="analytics">)'
    else:
        section_pattern = r'(<section\s+class="datascientist"\s+id="datascience">)'

    # Locate the section
    sec_match = re.search(section_pattern, content)
    if not sec_match:
        print(f"Error: Could not find section for '{section_type}' in index.html.")
        sys.exit(1)

    sec_start = sec_match.start()
    
    # Locate the work__container bd-grid inside this section
    container_pattern = r'<div\s+class="work__container\s+bd-grid">'
    container_match = re.search(container_pattern, content[sec_start:])
    if not container_match:
        print(f"Error: Could not find work__container in section '{section_type}'.")
        sys.exit(1)
        
    container_start = sec_start + container_match.start()
    
    # Locate the next closing </div> for this container
    closing_div_match = re.search(r'</div>', content[container_start:])
    if not closing_div_match:
        print("Error: Could not find closing div for work__container.")
        sys.exit(1)
        
    insert_pos = container_start + closing_div_match.start()

    # Generate the card HTML
    card_html = f"""                    <a href="pages/{page_filename}" target="_blank" rel="noopener" class="work__img">
                        <img src="assets/img/{img_filename}" alt="{title}" title="{title}" loading="lazy">
                    </a>\n"""

    # Insert card_html right before the closing </div> of the container
    new_content = content[:insert_pos] + card_html + content[insert_pos:]

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Updated index.html: Added project card to the {section_type.upper()} section.")

def main():
    print("=== RealDataLab Project Add Utility ===")
    base_dir = find_project_directories()
    
    next_id = get_next_project_id(base_dir)
    print(f"Auto-detected next project ID: {next_id}")
    
    # Interactive Prompts
    try:
        title = input("Enter Project Title (e.g., 'Urban Priority Triage'): ").strip()
        if not title:
            print("Title cannot be empty.")
            sys.exit(1)
            
        section = input("Enter Section (analytics [a] / datascience [d]): ").strip().lower()
        if section in ('a', 'analytics'):
            section_type = "analytics"
        elif section in ('d', 'datascience'):
            section_type = "datascience"
        else:
            print("Invalid section. Must be 'analytics' or 'datascience'.")
            sys.exit(1)
            
        app_url = input("Enter App URL (e.g., 'https://infrared-analysis.vercel.app/'): ").strip()
        if not app_url:
            print("App URL cannot be empty.")
            sys.exit(1)
            
        img_filename = input("Enter Image Filename (e.g., 'ds15.jpg'): ").strip()
        if not img_filename:
            print("Image filename cannot be empty.")
            sys.exit(1)
            
        print("\nEnter Description Paragraphs. Press Enter twice (an empty line) to finish:")
        paragraphs = []
        while True:
            line = input("> ").strip()
            if not line:
                break
            paragraphs.append(line)
            
        if not paragraphs:
            print("Description cannot be empty.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\nAborted.")
        sys.exit(1)

    print("\nAdding project with details:")
    print(f"  ID:          {next_id}")
    print(f"  Title:       {title}")
    print(f"  Section:     {section_type}")
    print(f"  App URL:     {app_url}")
    print(f"  Image:       {img_filename}")
    print(f"  Description: {len(paragraphs)} paragraph(s)")
    
    confirm = input("\nProceed? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Aborted.")
        sys.exit(1)

    page_filename = create_project_pages(base_dir, next_id, title, paragraphs, app_url, img_filename)
    add_card_to_index(base_dir, section_type, page_filename, title, img_filename)
    
    print("\nProject added successfully!")

if __name__ == "__main__":
    main()
