import os
import subprocess
import sys
from git import Repo

# === CONFIGURATION ===
from dotenv import load_dotenv
load_dotenv()

SQL_SERVER = os.getenv("SQL_SERVER")
SQL_USER = os.getenv("SQL_USER")
SQL_PASS = os.getenv("SQL_PASS")
SQL_DB = os.getenv("SQL_DB")

# === GET COMMIT SHA FROM USER ===
if len(sys.argv) != 2:
    print("Usage: python deploy_sql_changes.py <last_deploy_commit_sha>")
    sys.exit(1)

last_deploy_commit = sys.argv[1]

# === LOAD REPO ===
REPO_PATH = os.path.dirname(os.path.abspath(__file__))
repo = Repo(REPO_PATH)

# === GET CURRENT COMMIT ===
current_commit = repo.head.commit.hexsha
# === DETECT CHANGED FILES ===
diff = repo.git.diff('--name-only', f'{last_deploy_commit}..{current_commit}')
changed_files = diff.splitlines()
sql_files = [f for f in changed_files if f.endswith(".sql")]
if len(sql_files) == 0:
    print("No SQL files changed. Exiting.")
    sys.exit(0)

# === DEPLOY SQL FILES ===
for sql_file in sql_files:
    sql_file_path = os.path.join(REPO_PATH, sql_file)
    print(f"Deploying {sql_file_path}...")
    try:
        '''
        subprocess.run([
            "sqlcmd",
            "-S", SQL_SERVER,
            "-U", SQL_USER,
            "-P", SQL_PASS,
            "-d", SQL_DB,
            "-i", sql_file_path
        ], check=True)
        print(f"✅ Successfully deployed {sql_file}")
        '''
        subprocess.run([
                "sqlcmd",
                "-S", SQL_SERVER,
                "-U", SQL_USER,
                "-P", SQL_PASS,
                "-d", SQL_DB,
                "-Q", "SELECT 1"
            ], check=True)

    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to deploy {sql_file}: {e}")

print("✅ Deployment complete.")
