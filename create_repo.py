"""
GitHub Repository Creator
This script creates a new GitHub repository and configures git
"""
import requests
import subprocess
import sys

def create_repository(username, token):
    """Create a new repository on GitHub using the API"""
    
    repo_name = "building-energy-api"
    description = "Building Energy Data API - REST API for managing building energy consumption"
    
    # GitHub API endpoint
    url = "https://api.github.com/user/repos"
    
    # Headers with authentication
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Building-Energy-API-Setup"
    }
    
    # Repository data
    data = {
        "name": repo_name,
        "description": description,
        "private": False,
        "auto_init": False
    }
    
    print(f"🚀 Creating repository: {repo_name}")
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)
        
        if response.status_code == 201:
            print("✅ Repository created successfully!")
            repo_url = response.json()["clone_url"]
            print(f"📍 Repository URL: {repo_url}")
            return repo_url
        elif response.status_code == 422:
            print("⚠️  Repository already exists!")
            return f"https://github.com/{username}/{repo_name}.git"
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.json())
            return None
            
    except Exception as e:
        print(f"❌ Error creating repository: {e}")
        return None

def push_to_github(repo_url, git_path):
    """Push the code to GitHub"""
    
    print(f"\n📤 Pushing code to GitHub...")
    
    try:
        # Verify remote is set correctly
        subprocess.run(
            [git_path, "remote", "remove", "origin"],
            cwd="e:\\building-energy-api",
            capture_output=True,
            timeout=5
        )
        
        # Add new remote
        subprocess.run(
            [git_path, "remote", "add", "origin", repo_url],
            cwd="e:\\building-energy-api",
            capture_output=True,
            timeout=5
        )
        
        # Push to GitHub
        result = subprocess.run(
            [git_path, "push", "-u", "origin", "main"],
            cwd="e:\\building-energy-api",
            capture_output=True,
            timeout=30,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Code pushed successfully!")
            return True
        else:
            print(f"❌ Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error pushing code: {e}")
        return False

if __name__ == "__main__":
    
    print("=" * 60)
    print("GitHub Repository Setup")
    print("=" * 60)
    
    # Get credentials
    username = input("\n👤 GitHub Username (e.g., musmanhussain01-a11y): ").strip()
    token = input("🔑 GitHub Personal Access Token: ").strip()
    
    if not username or not token:
        print("❌ Username and token are required!")
        sys.exit(1)
    
    # Git path
    git_path = "C:\\Program Files\\Git\\bin\\git.exe"
    
    # Create repository
    repo_url = create_repository(username, token)
    
    if repo_url:
        # Push code
        if push_to_github(repo_url, git_path):
            print("\n" + "=" * 60)
            print("✅ Setup Complete!")
            print("=" * 60)
            print(f"\n🎉 Your code is now on GitHub!")
            print(f"📍 Repository: {repo_url.replace('.git', '')}")
            print(f"\n Share this link with Mahsa: {repo_url.replace('.git', '')}")
        else:
            print("\n❌ Failed to push code")
    else:
        print("\n❌ Failed to create repository")
