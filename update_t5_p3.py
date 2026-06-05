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

# Data for Test 5 Part 3 (Q32-Q34)
content_32_34 = {
    'shadowing': [
        {'speaker': 'W-Br', 'en': "Hi, Shenchao, / I'm practicing my presentation / in the conference room / across the hall, / and the projector in there / keeps shutting off. / I think it's overheating. / Has this happened to you?", 
         'vi': "Chào Shenchao, / tôi đang thực hành bài thuyết trình của mình / trong phòng hội nghị / phía bên kia hành lang, / và máy chiếu trong đó / cứ liên tục bị tắt. / Tôi nghĩ nó đang quá nóng. / Việc này có từng xảy ra với bạn không?"},
        {'speaker': 'M-Cn', 'en': "Oh, that projector is old. / It really needs to be replaced. / If I were you, / l'd just move to room 204 / and practice there. / Also, that room has a window. / It's much nicer.", 
         'vi': "Ồ, cái máy chiếu đó cũ rồi. / Nó thực sự cần được thay thế. / Nếu tôi là bạn, / tôi sẽ chuyển sang phòng 204 / và thực hành ở đó. / Ngoài ra, phòng đó có cửa sổ. / Nó đẹp hơn nhiều."},
        {'speaker': 'W-Br', 'en': "OK. Thanks.", 'vi': "Được rồi. Cảm ơn nhé."},
        {'speaker': 'M-Cn', 'en': "By the way, / you’ll need a special cable / to connect to the control panel / in that room. / Here, you can use this one. / Just leave it plugged in / when you're finished.", 
         'vi': "Nhân tiện, / bạn sẽ cần một sợi cáp đặc biệt / để kết nối với bảng điều khiển / trong căn phòng đó. / Đây, bạn có thể dùng cái này. / Cứ để nó cắm ở đó / khi bạn hoàn thành xong."}
    ],
    'focus': [
        {'chunk': 'practicing my presentation', 'vi': 'thực hành bài thuyết trình của mình'},
        {'chunk': 'projector keeps shutting off', 'vi': 'máy chiếu cứ liên tục bị tắt', 'paraphrase': 'a projector is not working', 'q_num': '32'},
        {'chunk': 'needs to be replaced', 'vi': 'cần được thay thế'},
        {'chunk': 'move to room 204', 'vi': 'chuyển sang phòng 204', 'paraphrase': 'Moving to a different room', 'q_num': '33'},
        {'chunk': 'special cable', 'vi': 'sợi cáp đặc biệt', 'paraphrase': 'a cable', 'q_num': '34'},
        {'chunk': 'connect to the control panel', 'vi': 'kết nối với bảng điều khiển'}
    ],
    'word_bank': ['practicing', 'shutting off', 'replaced', 'move to', 'special cable', 'connect'],
    'filling': [
        {'speaker': 'W-Br', 'text': 'Hi, Shenchao, I\'m <input type="text" data-answer="practicing" class="input-blank mx-1 w-[100px]"> my presentation in the conference room across the hall, and the projector in there keeps <input type="text" data-answer="shutting off" class="input-blank mx-1 w-[120px]">. I think it\'s overheating.'},
        {'speaker': 'M-Cn', 'text': 'Oh, that projector is old. It really needs to be <input type="text" data-answer="replaced" class="input-blank mx-1 w-[100px]">. If I were you, l\'d just <input type="text" data-answer="move to" class="input-blank mx-1 w-[100px]"> room 204 and practice there.'},
        {'speaker': 'W-Br', 'text': 'OK. Thanks.'},
        {'speaker': 'M-Cn', 'text': 'By the way, you’ll need a <input type="text" data-answer="special cable" class="input-blank mx-1 w-[130px]"> to <input type="text" data-answer="connect" class="input-blank mx-1 w-[100px]"> to the control panel in that room.'}
    ],
    'explanations': [
        {
            'num': '32', 'question': 'What problem does the woman describe?', 'question_vi': 'Người phụ nữ mô tả vấn đề gì?',
            'options': {'A': 'A room is not available.', 'B': 'A window will not open.', 'C': 'A projector is not working.', 'D': 'The weather has changed suddenly.'},
            'options_vi': {'A': 'Một phòng không có sẵn.', 'B': 'Một cửa sổ sẽ không mở.', 'C': 'Một máy chiếu không hoạt động.', 'D': 'Thời tiết đã thay đổi đột ngột.'},
            'ans': 'C', 'explanation': 'Người phụ nữ nói: "the projector in there keeps shutting off" (máy chiếu trong đó cứ liên tục bị tắt). Điều này tương ứng với việc máy chiếu không hoạt động. Đáp án là C.'
        },
        {
            'num': '33', 'question': 'What does the man suggest doing?', 'question_vi': 'Người đàn ông gợi ý làm gì?',
            'options': {'A': 'Moving to a different room', 'B': 'Calling a technician', 'C': 'Canceling an event', 'D': 'Ordering some supplies'},
            'options_vi': {'A': 'Chuyển sang một phòng khác', 'B': 'Gọi kỹ thuật viên', 'C': 'Hủy bỏ một sự kiện', 'D': 'Đặt mua một số vật tư'},
            'ans': 'A', 'explanation': 'Người đàn ông gợi ý: "I\'d just move to room 204 and practice there" (tôi sẽ chỉ chuyển sang phòng 204 và thực hành ở đó). Đáp án là A.'
        },
        {
            'num': '34', 'question': 'What does the man hand to the woman?', 'question_vi': 'Người đàn ông đưa cho người phụ nữ cái gì?',
            'options': {'A': 'An umbrella', 'B': 'Some keys', 'C': 'A cable', 'D': 'Some printouts'},
            'options_vi': {'A': 'Một chiếc ô', 'B': 'Một số chìa khóa', 'C': 'Một sợi cáp', 'D': 'Một số bản in'},
            'ans': 'C', 'explanation': 'Người đàn ông nói: "you’ll need a special cable... Here, you can use this one" (bạn sẽ cần một sợi cáp đặc biệt... Đây, bạn có thể dùng cái này) và đưa nó cho cô ấy. Đáp án là C.'
        }
    ]
}

update_html('Test 5/LC-T5-P3-Q32-34.html', content_32_34)

# Data for 35-37
content_35_37 = {
    'shadowing': [
        {'speaker': 'W-Am', 'en': "Hi. / I'm Amanda Hoffman, / and I'm on the panel / of publishing experts. / I was told / to check in here / at the registration desk.", 'vi': "Chào bạn. / Tôi là Amanda Hoffman, / và tôi nằm trong ban / chuyên gia xuất bản. / Tôi được bảo / đến đăng ký tại đây / tại quầy đăng ký."},
        {'speaker': 'M-Au', 'en': "Yes, Ms. Hoffman. / Welcome to the Portland Literary Conference. / Here's your registration packet, / which includes a gift card / to thank you for participating.", 'vi': "Vâng, thưa bà Hoffman. / Chào mừng bà đến với Hội nghị Văn học Portland. / Đây là bộ tài liệu đăng ký của bà, / bao gồm một thẻ quà tặng / để cảm ơn bà đã tham gia."},
        {'speaker': 'W-Am', 'en': "Oh, thank you. / Just to confirm, / the panel discussion / begins at three P.M., / right?", 'vi': "Ồ, cảm ơn bạn. / Chỉ để xác nhận lại, / buổi thảo luận của ban chuyên gia / bắt đầu lúc 3 giờ chiều, / đúng không?"},
        {'speaker': 'M-Au', 'en': "Yes, / but we do ask / that all panel members / arrive ten minutes beforehand. / I hope you enjoy the conference!", 'vi': "Vâng, / nhưng chúng tôi yêu cầu / tất cả các thành viên trong ban / đến trước mười phút. / Hy vọng bà tận hưởng hội nghị!"}
    ],
    'focus': [
        {'chunk': 'panel of publishing experts', 'vi': 'ban chuyên gia xuất bản', 'paraphrase': 'Publishing', 'q_num': '35'},
        {'chunk': 'registration desk', 'vi': 'quầy đăng ký'},
        {'chunk': 'registration packet', 'vi': 'bộ tài liệu đăng ký'},
        {'chunk': 'includes a gift card', 'vi': 'bao gồm một thẻ quà tặng', 'paraphrase': 'A gift card', 'q_num': '36'},
        {'chunk': 'panel discussion', 'vi': 'buổi thảo luận của ban chuyên gia'},
        {'chunk': 'arrive ten minutes beforehand', 'vi': 'đến trước mười phút', 'paraphrase': 'Arrive early', 'q_num': '37'}
    ],
    'word_bank': ['publishing', 'registration desk', 'packet', 'gift card', 'panel discussion', 'beforehand'],
    'filling': [
        {'speaker': 'W-Am', 'text': 'Hi. I\'m Amanda Hoffman, and I\'m on the panel of <input type="text" data-answer="publishing" class="input-blank mx-1 w-[120px]"> experts. I was told to check in here at the <input type="text" data-answer="registration desk" class="input-blank mx-1 w-[160px]">.'},
        {'speaker': 'M-Au', 'text': 'Yes, Ms. Hoffman. Welcome to the Portland Literary Conference. Here\'s your registration <input type="text" data-answer="packet" class="input-blank mx-1 w-[100px]">, which includes a <input type="text" data-answer="gift card" class="input-blank mx-1 w-[100px]"> to thank you for participating.'},
        {'speaker': 'W-Am', 'text': 'Oh, thank you. Just to confirm, the <input type="text" data-answer="panel discussion" class="input-blank mx-1 w-[150px]"> begins at three P.M., right?'},
        {'speaker': 'M-Au', 'text': 'Yes, but we do ask that all panel members arrive ten minutes <input type="text" data-answer="beforehand" class="input-blank mx-1 w-[120px]">. I hope you enjoy the conference!'}
    ],
    'explanations': [
        {
            'num': '35', 'question': 'What industry does Amanda Hoffman work in?', 'question_vi': 'Amanda Hoffman làm việc trong ngành nào?',
            'options': {'A': 'Hospitality', 'B': 'Healthcare', 'C': 'Publishing', 'D': 'Information technology'},
            'options_vi': {'A': 'Nhà hàng khách sạn', 'B': 'Chăm sóc sức khỏe', 'C': 'Xuất bản', 'D': 'Công nghệ thông tin'},
            'ans': 'C', 'explanation': 'Cô ấy giới thiệu: "I\'m on the panel of publishing experts" (tôi nằm trong ban chuyên gia xuất bản). Đáp án là C.'
        },
        {
            'num': '36', 'question': 'According to the man, what is included in the registration packet?', 'question_vi': 'Theo người đàn ông, cái gì được bao gồm trong bộ tài liệu đăng ký?',
            'options': {'A': 'A map', 'B': 'A gift card', 'C': 'A schedule of events', 'D': 'A certificate of attendance'},
            'options_vi': {'A': 'Một bản đồ', 'B': 'Một thẻ quà tặng', 'C': 'Một lịch trình sự kiện', 'D': 'Một chứng nhận tham gia'},
            'ans': 'B', 'explanation': 'Người đàn ông nói: "your registration packet, which includes a gift card" (bộ tài liệu đăng ký của bà, bao gồm một thẻ quà tặng). Đáp án là B.'
        },
        {
            'num': '37', 'question': 'What does the man tell the woman to do?', 'question_vi': 'Người đàn ông bảo người phụ nữ làm gì?',
            'options': {'A': 'Arrive early', 'B': 'Pay a fee', 'C': 'Wear a name badge', 'D': 'Choose a menu option'},
            'options_vi': {'A': 'Đến sớm', 'B': 'Trả một khoản phí', 'C': 'Đeo thẻ tên', 'D': 'Chọn một tùy chọn thực đơn'},
            'ans': 'A', 'explanation': 'Người đàn ông nói: "we do ask that all panel members arrive ten minutes beforehand" (chúng tôi yêu cầu tất cả các thành viên đến trước 10 phút). Điều này nghĩa là đến sớm. Đáp án là A.'
        }
    ]
}

update_html('Test 5/LC-T5-P3-Q35-37.html', content_35_37)

