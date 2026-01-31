#!/usr/bin/env python3
"""
Build script for On The Way Heating & Air website.
Combines header/footer templates with page content to generate final HTML files.

Usage:
    python3 build.py          # Build all pages
    python3 build.py --watch  # Watch for changes and rebuild automatically

Directory Structure:
    src/
        templates/
            _head.html      # Common <head> content
            _header.html    # Site header/navigation
            _footer.html    # Site footer with scripts
        pages/
            services/ac/    # AC service pages
            services/heating/
            services/air-quality/
            locations/      # Location pages
    dist/                   # Output directory (generated files)
    
Page Template Format:
    Each page in src/pages/ should contain:
    - {{HEAD}} placeholder for common head content
    - {{HEADER}} placeholder for site header
    - {{FOOTER}} placeholder for site footer
    
    The script will automatically calculate {{ROOT_PATH}} based on file depth.
"""

import os
import re
import shutil
import argparse
from pathlib import Path

# Configuration
SRC_DIR = Path(__file__).parent / 'src'
DIST_DIR = Path(__file__).parent / 'dist'
TEMPLATES_DIR = SRC_DIR / 'templates'
PAGES_DIR = SRC_DIR / 'pages'
ROOT_FILES_DIR = Path(__file__).parent  # For copying root-level assets

# Files to copy from root to dist (assets, styles, etc.)
ROOT_ASSETS = [
    'styles.css',
    'main.js',
    'index.html',
    'On-The-Way.webp',
    'mascot-navbar.webp',
    'footer-logo.webp',
    'favicon.ico',
    'icon.png',
    'icon.webp',
    'logo.jpg',
    'hero-1280.webp',
    'hero-1920.webp',
    'hero-480.webp',
    'hero-768.webp',
    'hero-fallback.jpg',
    'hero-mobile.webp',
    'hero-mobile-bg.webp',
    'mascot-mobile.webp',
    'google-reviews.webp',
    'poppins-400.woff2',
    'poppins-600.woff2',
    'poppins-700.woff2',
    'montserrat-800.woff2',
]


def load_template(name: str) -> str:
    """Load a template file from the templates directory."""
    template_path = TEMPLATES_DIR / name
    if not template_path.exists():
        print(f"Warning: Template {name} not found at {template_path}")
        return ''
    return template_path.read_text(encoding='utf-8')


def calculate_root_path(page_path: Path) -> str:
    """
    Calculate the relative path from a page to the root directory.
    
    For example:
        pages/services/ac/emergency-ac-repair.html -> ../../../
        pages/locations/lutz.html -> ../../
        index.html -> ./
    """
    # Get relative path from dist directory
    try:
        rel_path = page_path.relative_to(DIST_DIR)
    except ValueError:
        rel_path = page_path.relative_to(PAGES_DIR)
    
    # Count directory depth
    depth = len(rel_path.parts) - 1  # -1 for the file itself
    
    if depth == 0:
        return './'
    return '../' * depth


def process_page(page_path: Path, templates: dict) -> str:
    """
    Process a single page file, replacing template placeholders.
    
    Args:
        page_path: Path to the source page file
        templates: Dictionary of loaded templates
        
    Returns:
        Processed HTML content
    """
    content = page_path.read_text(encoding='utf-8')
    
    # Calculate root path for this page's depth
    # We need to calculate based on where the file will be in dist
    rel_to_pages = page_path.relative_to(PAGES_DIR)
    output_path = DIST_DIR / 'pages' / rel_to_pages
    root_path = calculate_root_path(output_path)
    
    # Replace template placeholders
    content = content.replace('{{HEAD}}', templates.get('_head.html', ''))
    content = content.replace('{{HEADER}}', templates.get('_header.html', ''))
    content = content.replace('{{FOOTER}}', templates.get('_footer.html', ''))
    
    # Replace root path in all templates and content
    content = content.replace('{{ROOT_PATH}}', root_path)
    
    return content


def build_pages():
    """Build all pages from source to dist directory."""
    print("🔨 Building website...")
    
    # Load templates
    templates = {}
    for template_file in TEMPLATES_DIR.glob('_*.html'):
        templates[template_file.name] = template_file.read_text(encoding='utf-8')
    print(f"   Loaded {len(templates)} templates")
    
    # Create dist directory structure
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True)
    
    # Copy root assets
    copied_assets = 0
    for asset in ROOT_ASSETS:
        src_path = ROOT_FILES_DIR / asset
        if src_path.exists():
            shutil.copy2(src_path, DIST_DIR / asset)
            copied_assets += 1
    print(f"   Copied {copied_assets} root assets")
    
    # Process all pages
    pages_built = 0
    for page_path in PAGES_DIR.rglob('*.html'):
        # Calculate output path
        rel_path = page_path.relative_to(PAGES_DIR)
        output_path = DIST_DIR / 'pages' / rel_path
        
        # Create output directory
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Process and write page
        processed_content = process_page(page_path, templates)
        output_path.write_text(processed_content, encoding='utf-8')
        pages_built += 1
        print(f"   Built: pages/{rel_path}")
    
    print(f"\n✅ Build complete! {pages_built} pages built to {DIST_DIR}")
    return pages_built


def copy_to_root():
    """
    Copy built files back to root for deployment.
    This maintains backward compatibility with the current deployment setup.
    """
    print("\n📦 Copying to root for deployment...")
    
    # Copy pages directory
    pages_src = DIST_DIR / 'pages'
    pages_dest = ROOT_FILES_DIR / 'pages'
    
    if pages_src.exists():
        if pages_dest.exists():
            shutil.rmtree(pages_dest)
        shutil.copytree(pages_src, pages_dest)
        print(f"   Copied pages/ directory")
    
    print("✅ Ready for deployment!")


def main():
    parser = argparse.ArgumentParser(description='Build On The Way website')
    parser.add_argument('--watch', action='store_true', help='Watch for changes')
    parser.add_argument('--deploy', action='store_true', help='Copy to root after build')
    args = parser.parse_args()
    
    if args.watch:
        print("Watch mode not implemented yet. Running single build...")
    
    pages_built = build_pages()
    
    if args.deploy:
        copy_to_root()
    
    return pages_built


if __name__ == '__main__':
    main()
