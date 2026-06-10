# How to Add New Projects (addpro)

To maintain a consistent structure across the **RealDataLab** portfolio, follow either the automated script method or the manual checklist below to add new projects.

---

## Method 1: Automated Script (Recommended)

An interactive helper script, [`add_project.py`](file:///c:/12_CODINGHARD/web_realdatahub/RealDataHub.github.io/add_project.py), has been created in the repository root to automate the file creation and card insertion.

### Requirements
- Python 3.x

### Usage
1. Open terminal and navigate to the project directory:
   ```bash
   cd c:\12_CODINGHARD\web_realdatahub\RealDataHub.github.io
   ```
2. Run the script:
   ```bash
   python add_project.py
   ```
3. Follow the interactive prompts:
   - **Project Title**: e.g., `Urban Priority Triage`
   - **Section**: Enter `a` (or `analytics`) to place in the Analytics section, or `d` (or `datascience`) to place in the Data Science section.
   - **App URL**: The destination web app URL (usually on Vercel) that will be rendered inside the project's iframe.
   - **Image Filename**: The name of the project screenshot, which must be placed inside the `assets/img/` folder (e.g., `ds15.jpg`).
   - **Description**: Enter one or more paragraphs describing the project. Press **Enter** on a blank line when done.
4. Review the details and type `y` to confirm. The script will automatically:
   - Calculate the next sequence number (e.g., `29.html` and `29_app.html`).
   - Create the wrapper pages inside the `pages/` directory.
   - Inject the corresponding card link into `index.html` within the selected section.

---

## Method 2: Manual Steps

If you need to add a project manually, follow these 4 steps:

### Step 1: Add the Image Asset
Ensure the preview thumbnail image of the project is added to:
- Directory: `assets/img/`
- Recommendation: Use `.jpg` or `.png` formats. Standardize names like `ds[X].jpg` for Data Science or `an[X].jpg` for Analytics.

### Step 2: Create the Main Project Page
In the `pages/` directory, create a new file `XX.html` (where `XX` is the next sequential number, e.g., `30.html`). Use the following structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="[Short description of the project for search engine snippet]">
    <link rel="canonical" href="XX_app.html">
    <link rel="stylesheet" href="../assets/css/styles.css">
    <title>[Project Name]</title>
    <style>
        body { margin: 0; padding: 2rem; background-color: #fff; }
        .container { max-width: 1024px; margin: 0 auto; display: flex; flex-direction: column; gap: 2rem; }
        .image-section { width: 100%; overflow: hidden; border-radius: 0.5rem; box-shadow: 0px 4px 25px rgba(14, 36, 49, 0.15); }
        .image-section img { width: 100%; height: auto; display: block; cursor: pointer; }
        .text-section { padding: 2rem; line-height: 1.8; color: hsl(224, 56%, 12%); font-size: 1rem; }
        .text-section p { margin-bottom: 1rem; }
        .text-section p:last-child { margin-bottom: 0; }
        .redirect-notice { text-align: center; margin-top: 2rem; color: hsl(224, 89%, 60%); font-weight: 600; }
        @media screen and (min-width: 768px) {
            .container { padding: 2rem 0; }
            .text-section { font-size: 1.1rem; padding: 2.5rem; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="text-section">
            <p>[First paragraph of detailed project description...]</p>
            <p>[Second paragraph of detailed project description...]</p>
        </div>
        <div class="image-section">
            <img src="../assets/img/[IMAGE_FILENAME]" alt="redirect now!" title="do not wait, redirect now to app - [Project Name]" onclick="window.location.href='XX_app.html';">
        </div>
        <div class="redirect-notice" id="notice">
            <p>Click the image above to open the application in full screen.</p>
        </div>
    </div>
</body>
</html>
```

### Step 3: Create the App Wrapper Page
In the `pages/` directory, create `XX_app.html` (e.g., `30_app.html`) to display the project in full screen inside an iframe:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Project Name] App</title>
    <style>
        body, html { margin: 0; padding: 0; height: 100%; overflow: hidden; background-color: #fff; }
        iframe { width: 100%; height: 100%; border: none; display: block; }
    </style>
</head>
<body>
    <iframe src="[APP_URL]" title="[Project Name] App" allowfullscreen></iframe>
</body>
</html>
```

### Step 4: Link the Card in `index.html`
Open `index.html` at the root of the project and find the target section:
- **Analytics** section: `<section class="analytic" id="analytics">`
- **Data Science** section: `<section class="datascientist" id="datascience">`

In the chosen section, append the following link structure right before the closing `</div>` of the corresponding `work__container bd-grid`:

```html
                    <a href="pages/XX.html" target="_blank" rel="noopener" class="work__img">
                        <img src="assets/img/[IMAGE_FILENAME]" alt="[Project Name]" title="[Project Name]" loading="lazy">
                    </a>
```
