import subprocess
import re
from datetime import datetime

##### INFO #####
# This creates a short print of the commit logs of a nested from the date, and filters the Bforartists commits
# This script assumes you have a python environment installed to your operating system. 

#### Use #####
# 1. Place the script in the root of where the Bforartists repository is
# 2. Open the script in something like VS Code
# 3. Run the script by pressing the play button to the top right, it should run with a python terminal

# 🔧 CONFIGURATION
REPO_PATH = "../Bforartists" # The root of where the Bforartists repository is
START_DATE = "2025-08-08"  # YYYY-MM-DD format

# 📅 Convert start date
start_dt = datetime.strptime(START_DATE, "%Y-%m-%d")

# 📋 Pattern to match task numbers like #123 and filter titles containing "from Bforartists"
task_pattern = re.compile(r"#(\d+)\s*[:-]?\s*(.*from Bforartists.*)")

# 🧹 Output list
task_list = []

# 🔍 Get git logs using subprocess
git_logs = subprocess.run(
    ["git", "log", f"--since={START_DATE}", "--pretty=format:%s"],
    cwd=REPO_PATH,
    capture_output=True,
    text=True
).stdout.splitlines()

# 📋 Process logs
for msg in git_logs:
    match = task_pattern.search(msg)
    if match:
        task_num = match.group(1)

        title = match.group(2)

        # Extract additional task numbers and preserve the title's capitalization
        task_numbers = ' '.join(f"#{num}" for num in re.findall(r"#(\d+)", title))
        task_words = title.lower().replace(" ", "-")  # Convert to lowercase and replace spaces with hyphens

        task_list.append(f"#{task_num}-{task_words}")


# 📤 Print results
print("\n".join(task_list))