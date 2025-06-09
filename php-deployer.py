# run command : python php_deployer.py "F:\GIT-Push\PHP\Datum" "C:\Xampp-new\htdocs"
import os
import shutil
import webbrowser
import stat
import argparse
from pathlib import Path

def on_rm_error(func, path, exc_info):
    """Error handler for shutil.rmtree"""
    path = Path(path)
    # Clear read-only flag
    path.chmod(stat.S_IWRITE)
    try:
        func(path)
    except Exception as e:
        print(f"Could not remove {path}: {e}")

def deploy_php_project(project_path, htdocs_path):
    """Deploys PHP project to htdocs directory and opens in browser"""
    try:
        project_path = Path(project_path)
        htdocs_path = Path(htdocs_path)
        
        if not project_path.exists():
            raise FileNotFoundError(f"Project directory not found: {project_path}")
        if not htdocs_path.exists():
            raise FileNotFoundError(f"htdocs directory not found: {htdocs_path}")
        
        folder_name = project_path.name
        dest_path = htdocs_path / folder_name
        
        # Remove existing deployment with error handling
        if dest_path.exists():
            print(f"Removing existing deployment: {dest_path}")
            shutil.rmtree(dest_path, onerror=on_rm_error)
        
        # Copy project to htdocs
        print(f"Copying {project_path} to {htdocs_path}")
        shutil.copytree(project_path, dest_path)
        
        # Open in browser
        url = f"http://localhost/{folder_name}"
        print(f"Opening: {url}")
        webbrowser.open(url)
        
        print("Deployment successful!")
        
    except Exception as e:
        print(f"Error during deployment: {str(e)}")
        if "Access is denied" in str(e):
            print("\nTIP: Try running this script as Administrator")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Deploy PHP project to htdocs')
    parser.add_argument('project_path', help='Path to PHP project directory')
    parser.add_argument('htdocs_path', help='Path to htdocs directory')
    args = parser.parse_args()
    deploy_php_project(args.project_path, args.htdocs_path)