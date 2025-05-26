import os
import glob
import shutil
import random
from tqdm import tqdm
from collections import defaultdict # Useful for grouping files by category

# --- Configuration ---
input_dir = 'data/raw/html/'
json_dir = 'data/raw/json'
output_dir = 'cate/raw/html'
out_json_dir = 'cate/raw/json'
sampling_limit = 1200
# Specify the categories to process
target_categories = {'2404', '2405', '2406', '2407', '2408', '2409', '2410', '2411', '2412', '2501', '2502', '2503', '2504', '2505'}
# For reproducible sampling, uncomment and set a seed:
# random.seed(42)

# --- Phase 1: Discovering and grouping files by category ---
print("--- Phase 1: Discovering and grouping files by category ---")
print(f"Only processing targeted categories: {', '.join(sorted(target_categories))}")
htmls = glob.glob(os.path.join(input_dir, "**/*.html"), recursive=True)

# categories_map will store: {'category_name': [list_of_source_file_paths]}
categories_map = defaultdict(list)
valid_htmls = []

if not htmls:
    print(f"No HTML files found in {input_dir}. Exiting.")
    exit()

for html_file_path in tqdm(htmls, desc="Scanning source files"):
    # Get the relative path part (preserve subdirectory structure)
    rel_path = os.path.relpath(html_file_path, input_dir)
    rel_dir = os.path.dirname(rel_path)
    file_name = os.path.basename(html_file_path)
    
    # Get category name by splitting at the first dot
    parts = file_name.split('.', 1)
    category_name = parts[0]  # If filename starts with ".", this will be an empty string ""
    
    # Only process target categories
    if category_name not in target_categories:
        continue
        
    # Build the corresponding JSON file path, preserving the same subdirectory structure
    json_file_name = os.path.splitext(file_name)[0] + '.json'
    json_file_path = os.path.join(json_dir, rel_dir, json_file_name)
    
    # Only process HTML files that have a matching JSON file
    if os.path.exists(json_file_path):
        categories_map[category_name].append((html_file_path, json_file_path))
        valid_htmls.append(html_file_path)
    
total_valid = len(valid_htmls)
print(f"Scan complete: Found {len(htmls)} HTML files, {total_valid} have matching JSON files in targeted categories.")
print(f"Categories found: {', '.join(sorted(categories_map.keys()))}")

# --- Phase 2: Sampling within groups and copying selected files ---
print(f"\n--- Phase 2: Sampling and copying files (limit: {sampling_limit} per category) ---")

# Ensure base output directories exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created base output directory: {output_dir}")
if not os.path.exists(out_json_dir):
    os.makedirs(out_json_dir)
    print(f"Created JSON output directory: {out_json_dir}")

# Iterate over each category and their list of source file paths
for category_name, source_pairs_list in tqdm(categories_map.items(), desc="Processing categories"):
    pairs_to_copy_for_this_category = []
    num_files_in_category = len(source_pairs_list)
    
    if num_files_in_category > sampling_limit:
        tqdm.write(f"  Category '{category_name}': Found {num_files_in_category} file pairs. Sampling down to {sampling_limit}.")
        pairs_to_copy_for_this_category = random.sample(source_pairs_list, sampling_limit)
    else:
        tqdm.write(f"  Category '{category_name}': Found {num_files_in_category} file pairs. No sampling needed (at or below limit).")
        pairs_to_copy_for_this_category = source_pairs_list  # Copy all files for this category

    # Determine the target directory for this category's files
    html_target_dir = os.path.join(output_dir, category_name)
    json_target_dir = os.path.join(out_json_dir, category_name)
    
    # Ensure target directories exist
    os.makedirs(html_target_dir, exist_ok=True)
    os.makedirs(json_target_dir, exist_ok=True)

    # Copy the selected file pairs to their target locations
    copied_count = 0
    if pairs_to_copy_for_this_category: # Only proceed if there are files to copy
        for html_path, json_path in pairs_to_copy_for_this_category:
            html_file_name = os.path.basename(html_path)
            json_file_name = os.path.basename(json_path)
            
            html_dest_path = os.path.join(html_target_dir, html_file_name)
            json_dest_path = os.path.join(json_target_dir, json_file_name)
            
            try:
                # Copy HTML and JSON files
                shutil.copy2(html_path, html_dest_path)
                shutil.copy2(json_path, json_dest_path)
                copied_count += 1
            except Exception as e_copy:
                tqdm.write(f"    Error copying files: {e_copy}")
    
    if num_files_in_category > sampling_limit:
        tqdm.write(f"  Category '{category_name}': Copied {copied_count} sampled file pairs (out of {num_files_in_category} original).")
    elif copied_count > 0: # Only print if files were actually copied
        tqdm.write(f"  Category '{category_name}': Copied {copied_count} file pairs.")
    elif num_files_in_category == 0: # If the category was empty to begin with
        tqdm.write(f"  Category '{category_name}': No file pairs found originally.")

print("\nProcessing complete. Selected HTML and JSON files have been copied to their respective directories.")