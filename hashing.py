import hashlib
import os
import json
import argparse

# Function to produce hash of a given file
def hashfile(filepath):
    fingerprint = hashlib.sha256()
    with open(filepath, "rb") as f:
        chunk = f.read(8192)
        while chunk:
            fingerprint.update(chunk)
            chunk = f.read(8192)

    return fingerprint.hexdigest()

# Create a parser object and set mandatory and optional arguments for user to enter
parser = argparse.ArgumentParser(description="File Integrity Monitor")
parser.add_argument("directory", help="Folder to scan")
parser.add_argument("--baseline", default="baseline.json", help="Baseline file to compare against or create")
parser.add_argument("--update", action="store_true", help="Save current scan as the new baseline")
args = parser.parse_args()

# Traverse through the directory provided and create a hash for files at each level
new_results = {}
for root, dirs, files in os.walk(args.directory):
    for file in files:
        file_path = os.path.join(root, file)
        new_results[file_path] = hashfile(file_path)

# If the user provides the update flag or if a baseline file of hashes doesn't exist, then we create one
# Else if a baseline file already exists then we read it and compare the hashes in it against
# the hashes created in this instance
if args.update or not os.path.exists(args.baseline):
    with open(args.baseline, "w") as f:
        json.dump(new_results, f, indent=2)
    
    print(f"Baseline saved to {args.baseline} ({len(new_results)} files)")
else:
    with open(args.baseline, "r") as f:
        old_results = json.load(f)

    old_paths = set(old_results.keys())
    new_paths = set(new_results.keys())

    added_paths = new_paths - old_paths
    removed_paths = old_paths - new_paths
    common_paths = old_paths & new_paths
    modified = [path for path in common_paths if old_results[path] != new_results[path]]

    print("Added:", added_paths)
    print("Removed:", removed_paths)
    print("Modified:", modified)



    


