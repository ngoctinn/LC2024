import json
import os
import re

def update_html(file_path, content_data):
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 1. Update Shadowing Container
    shadowing_html = ""
    for turn in content_data['shadowing']:
        bg_color = "bg-blue-100" if turn['speaker'].startswith('M') else "bg-pink-100"
        text_color = "text-blue-600" if turn['speaker'].startswith('M') else "text-pink-600"
        speaker_initial = turn['speaker'][0]
        
        shadowing_html += f"""
                <div class="flex gap-4">
                    <div class="w-12 h-12 {bg_color} rounded-full flex items-center justify-center font-bold {text_color} flex-shrink-0">{speaker_initial}</div>
                    <div class="w-full">
                        <div>
                            <strong>{turn['en']}</strong>
                            <span class="chunk-vi">{turn['vi']}</span>
                        </div>
                    </div>
                </div>\n"""
    
    html = re.sub(r'<div id="shadowingContainer" class="space-y-6 text-lg">.*?</div>\s*</section>', 
                  f'<div id="shadowingContainer" class="space-y-6 text-lg">{shadowing_html}</div>\n        </section>', 
                  html, flags=re.DOTALL)

    # 2. Update Kiến thức trọng tâm
    table_rows = ""
    for item in content_data['focus']:
        paraphrase = f' <br> <span class="paraphrase-tag">Paraphrase</span> <strong>{item["paraphrase"]}</strong> (Q{item["q_num"]})' if 'paraphrase' in item else ""
        table_rows += f"""
                    <tr class="hover:bg-slate-50">
                        <td class="py-4 px-6"><strong>{item['chunk']}</strong></td>
                        <td class="py-4 px-6">{item['vi']}{paraphrase}</td>
                    </tr>"""
    
    html = re.sub(r'<tbody class="divide-y divide-slate-100 text-slate-700">.*?</tbody>', 
                  f'<tbody class="divide-y divide-slate-100 text-slate-700">{table_rows}\n                </tbody>', 
                  html, flags=re.DOTALL)

    # 3. Update Điền cụm từ
    word_bank = "".join([f'<span class="px-3 py-1 bg-white text-slate-700 rounded-md border border-slate-200 text-sm font-medium shadow-sm">{phrase}</span>\n                ' for phrase in content_data['word_bank']])
    html = re.sub(r'<!-- Word Bank -->.*?</div>', 
                  f'<!-- Word Bank -->\n            <div class="mb-6 flex flex-wrap gap-2 justify-center bg-slate-50 p-4 rounded-lg border border-slate-100">\n                {word_bank}</div>', 
                  html, flags=re.DOTALL)
    
    filling_html = ""
    for p in content_data['filling']:
        turn_text = p['text']
        speaker_color = "text-blue-600" if p['speaker'].startswith('M') else "text-pink-600"
        filling_html += f'<p class="mb-4">\n                    <span class="{speaker_color} font-bold">{p["speaker"]}:</span> {turn_text}\n                </p>\n                '
    
    html = re.sub(r'<div class="bg-blue-50 p-6 rounded-lg text-lg leading-loose font-medium text-slate-700">.*?</div>', 
                  f'<div class="bg-blue-50 p-6 rounded-lg text-lg leading-loose font-medium text-slate-700">\n                {filling_html}</div>', 
                  html, flags=re.DOTALL)

    # 4. Update Giải thích chi tiết
    expl_html = ""
    for q in content_data['explanations']:
        options_html = ""
        for opt, text in q['options'].items():
            is_correct = opt == q['ans']
            class_str = 'class="font-bold text-blue-600"' if is_correct else ""
            options_html += f"""
                        <div {class_str}>
                            ({opt}) {text}
                            <span class="text-slate-500 text-sm block mt-1">{q['options_vi'][opt]}</span>
                        </div>"""
        
        expl_html += f"""
                <!-- Q{q['num']} -->
                <div class="bg-slate-50 p-5 rounded-lg border border-slate-100">
                    <div class="font-semibold text-slate-800 mb-1 text-lg">{q['num']}. {q['question']}</div>
                    <div class="text-slate-500 text-sm mb-4">{q['question_vi']}</div>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-slate-700">
                        {options_html}
                    </div>
                    <div class="mt-4 p-4 bg-indigo-50 rounded-lg border-l-4 border-indigo-500">
                        <div class="font-bold text-indigo-800 mb-2">Giải thích:</div>
                        <p class="text-slate-700 text-sm">{q['explanation']}</p>
                    </div>
                </div>\n"""
    
    html = re.sub(r'<div class="space-y-6">.*?</div>\s*</section>', 
                  f'<div class="space-y-6">{expl_html}</div>\n        </section>', 
                  html, flags=re.DOTALL)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)

