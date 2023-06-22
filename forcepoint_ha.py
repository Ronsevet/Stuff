import os
import sys
import hashlib

hashes = {}
duplicates = {}

def find_duplicates(directory):
  for entry in os.scandir(directory):
    if entry.is_file():
      with open(entry.path, "rb") as f:
        hash = hashlib.md5(f.read()).hexdigest()
        if hash in hashes:
          hashes[hash].append(entry.path)
        else:
          hashes[hash] = [entry.path]
    elif entry.is_dir():
        for result in find_duplicates(entry.path):
          yield result

  for hash, paths in hashes.items():
    if len(paths) > 1:
      duplicates[hash] = paths

def main():
  # Get the directory to search.
  directory = sys.argv[1]

  # Find duplicate files.
  for result in find_duplicates(directory):
    duplicates.update(result)

  # Print the duplicate file paths.
  for hash, paths in duplicates.items():
    print("duplicate files:", hash, paths)

if __name__ == "__main__":
  main()