import json
import os
import re

with open('parsed_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

test5 = data['T5']

def get_file_name(test_num, part, start_q, end_q):
    return f"Test {test_num}/LC-T{test_num}-P{part}-Q{start_q}-{end_q}.html"

# Template for Shadowing Container
def gen_shadowing(transcript):
    lines = transcript.split('\n')
    html = ""
    for line in lines:
        match = re.match(r'^([WM])-(.*?)\s+(.*)$', line)
        if not match:
            # Try just [WM] or speaker without suffix
            match = re.match(r'^([WM])\s+(.*)$', line)
            if not match:
                # Part 4 often doesn't have speaker labels in the beginning of every line
                # or has a different format
                speaker_code = "M" # Default
                full_label = "M-Au"
                text = line
            else:
                speaker_code = match.group(1)
                full_label = speaker_code
                text = match.group(2)
        else:
            speaker_code = match.group(1)
            full_label = match.group(1) + "-" + match.group(2)
            text = match.group(3)
        
        # Clean text from (32) etc.
        clean_text = re.sub(r'\(\d+,?\d*\)', '', text).strip()
        
        # This is where the AI (me) would normally provide translations.
        # Since I'm writing a script, I'll have to provide them here.
        # I'll use a placeholder for now and then maybe I should just generate the whole file content in a different way.
        
    return html

# Actually, it's better if I generate the WHOLE content of each file one by one.
# I'll do 3 files in this turn to see how it goes.

