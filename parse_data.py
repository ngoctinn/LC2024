import re
import json
import os

def parse_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by empty lines
    blocks = re.split(r'\n\s*\n', content.strip())
    
    parsed_data = []
    for block in blocks:
        lines = block.strip().split('\n')
        transcript_lines = []
        questions = []
        
        for line in lines:
            if re.match(r'^\d+\s', line):
                # Question line
                q_match = re.match(r'^(\d+)\s+(.*?)\s+A\.\s+(.*?)\s+B\.\s+(.*?)\s+C\.\s+(.*?)\s+D\.\s+(.*?)\s+Ans:(.*)$', line)
                if q_match:
                    questions.append({
                        'num': q_match.group(1),
                        'question': q_match.group(2),
                        'options': {
                            'A': q_match.group(3),
                            'B': q_match.group(4),
                            'C': q_match.group(5),
                            'D': q_match.group(6)
                        },
                        'ans': q_match.group(7).strip()
                    })
            else:
                transcript_lines.append(line)
        
        parsed_data.append({
            'transcript': '\n'.join(transcript_lines),
            'questions': questions
        })
    return parsed_data

t5_data = parse_file('assets/data_draft/T5.txt')
t6_data = parse_file('assets/data_draft/T6.txt')

with open('parsed_data.json', 'w', encoding='utf-8') as f:
    json.dump({'T5': t5_data, 'T6': t6_data}, f, ensure_ascii=False, indent=4)

