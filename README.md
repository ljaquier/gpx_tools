# Usage
```bash
# Usage: python gpx_merger.py output.gpx input1.gpx input2.gpx ...
python3 gpx_merger.py merged.gpx sample/part1.gpx sample/part2.gpx

# Usage: python gpx_cleaner.py output.gpx input.gpx
python3 gpx_cleaner.py merged_cleaned.gpx merged.gpx

# Usage: python gpx_missing_segments_fixer.py output.gpx input.gpx reference.gpx
python3 -m pip install --upgrade -r requirements.txt -t lib
PYTHONPATH=./lib python3 gpx_missing_segments_fixer.py merged_cleaned_fixed.gpx merged_cleaned.gpx sample/reference.gpx
```
