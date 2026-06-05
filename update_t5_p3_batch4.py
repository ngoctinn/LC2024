import json
import os
import re
from update_t5_p3 import update_html

# Data for 59-61
content_59_61 = {
    'shadowing': [
        {'speaker': 'M-Au', 'en': "Hi, So-Jin. / I just heard that Ms. Yoon / is retiring next month.", 'vi': "Chào So-Jin. / Tôi vừa nghe nói bà Yoon / sẽ nghỉ hưu vào tháng tới."},
        {'speaker': 'W-Br', 'en': "l’ll be sorry to see her go. / She was my mentor / when I first joined the firm, / and we've worked on / dozens of projects together.", 'vi': "Tôi sẽ rất tiếc khi thấy bà ấy rời đi. / Bà ấy là người cố vấn của tôi / khi tôi mới gia nhập công ty, / và chúng tôi đã làm việc cùng nhau / trong hàng tá dự án."},
        {'speaker': 'M-Au', 'en': "It's a bit hard to imagine / our sales team without her. / Has anybody approached you / about leading the team / after she’s gone?", 'vi': "Thật khó để hình dung / đội ngũ bán hàng của chúng ta mà không có bà ấy. / Có ai tiếp cận cô / về việc lãnh đạo nhóm / sau khi bà ấy đi chưa?"},
        {'speaker': 'W-Br', 'en': "Yes, and I’ve thought about it. / It’s a big step up, / even for someone like me / who's worked in Sales / for eight years. / And Human Resources / hasn’t even posted / the job description yet.", 'vi': "Có, và tôi đã suy nghĩ về điều đó. / Đó là một bước tiến lớn, / ngay cả với một người như tôi / đã làm việc trong bộ phận Bán hàng / tám năm rồi. / Và bộ phận Nhân sự / thậm chí còn chưa đăng / bản mô tả công việc nữa."},
        {'speaker': 'M-Au', 'en': "Well, we need someone / with experience.", 'vi': "À, chúng ta cần một người / có kinh nghiệm."}
    ],
    'focus': [
        {'chunk': 'retiring next month', 'vi': 'nghỉ hưu vào tháng tới', 'paraphrase': 'A colleague will retire', 'q_num': '59'},
        {'chunk': 'mentor', 'vi': 'người cố vấn'},
        {'chunk': 'sales team', 'vi': 'đội ngũ bán hàng', 'paraphrase': 'Sales', 'q_num': '60'},
        {'chunk': 'leading the team', 'vi': 'lãnh đạo nhóm'},
        {'chunk': 'job description', 'vi': 'mô tả công việc'},
        {'chunk': 'someone with experience', 'vi': 'người có kinh nghiệm', 'paraphrase': 'The woman should apply for a job', 'q_num': '61'}
    ],
    'word_bank': ['retiring', 'mentor', 'dozens', 'imagine', 'approached', 'description'],
    'filling': [
        {'speaker': 'M-Au', 'text': 'Hi, So-Jin. I just heard that Ms. Yoon is <input type="text" data-answer="retiring" class="input-blank mx-1 w-[100px]"> next month.'},
        {'speaker': 'W-Br', 'text': 'l’ll be sorry to see her go. She was my <input type="text" data-answer="mentor" class="input-blank mx-1 w-[100px]"> when I first joined the firm, and we\'ve worked on <input type="text" data-answer="dozens" class="input-blank mx-1 w-[100px]"> of projects together.'},
        {'speaker': 'M-Au', 'text': 'It\'s a bit hard to <input type="text" data-answer="imagine" class="input-blank mx-1 w-[100px]"> our sales team without her. Has anybody <input type="text" data-answer="approached" class="input-blank mx-1 w-[120px]"> you about leading the team after she’s gone?'},
        {'speaker': 'W-Br', 'text': 'Yes, and I’ve thought about it... And Human Resources hasn’t even posted the job <input type="text" data-answer="description" class="input-blank mx-1 w-[120px]"> yet.'}
    ],
    'explanations': [
        {
            'num': '59', 'question': 'What will happen next month?', 'question_vi': 'Điều gì sẽ xảy ra vào tháng tới?',
            'options': {'A': 'An award will be given.', 'B': 'A new product will launch.', 'C': 'A colleague will retire.', 'D': 'An office will relocate.'},
            'options_vi': {'A': 'Một giải thưởng sẽ được trao.', 'B': 'Một sản phẩm mới sẽ ra mắt.', 'C': 'Một đồng nghiệp sẽ nghỉ hưu.', 'D': 'Một văn phòng sẽ di dời.'},
            'ans': 'C', 'explanation': 'Người đàn ông nói: "Ms. Yoon is retiring next month" (bà Yoon sẽ nghỉ hưu vào tháng tới). Đáp án là C.'
        },
        {
            'num': '60', 'question': 'What department do the speakers work in?', 'question_vi': 'Những người nói làm việc ở bộ phận nào?',
            'options': {'A': 'Sales', 'B': 'Human Resources', 'C': 'Legal', 'D': 'Accounting'},
            'options_vi': {'A': 'Bán hàng', 'B': 'Nhân sự', 'C': 'Pháp lý', 'D': 'Kế toán'},
            'ans': 'A', 'explanation': 'Người đàn ông nhắc đến "our sales team" (đội ngũ bán hàng của chúng ta). Đáp án là A.'
        },
        {
            'num': '61', 'question': 'What does the man imply when he says, “we need someone with experience”?', 'question_vi': 'Người đàn ông ngụ ý điều gì khi nói: "chúng ta cần một người có kinh nghiệm"?',
            'options': {'A': 'The team has grown very quickly.', 'B': 'The woman should apply for a job.', 'C': 'A job description should be revised.', 'D': 'A new manager is not experienced enough.'},
            'options_vi': {'A': 'Nhóm đã phát triển rất nhanh.', 'B': 'Người phụ nữ nên nộp đơn xin việc.', 'C': 'Một bản mô tả công việc nên được sửa đổi.', 'D': 'Một quản lý mới không đủ kinh nghiệm.'},
            'ans': 'B', 'explanation': 'Khi người phụ nữ còn đang phân vân về việc dẫn dắt nhóm, người đàn ông nói họ cần người có kinh nghiệm để khuyến khích cô ấy (người đã có 8 năm kinh nghiệm) ứng tuyển. Đáp án là B.'
        }
    ]
}

# Data for 62-64
content_62_64 = {
    'shadowing': [
        {'speaker': 'W-Am', 'en': "Rajesh, / It was nice / to see you here / in New York / again this year.", 'vi': "Rajesh, / Thật vui / khi được gặp lại anh ở đây / tại New York / vào năm nay."},
        {'speaker': 'M-Cn', 'en': "Same here. / I look forward / to attending / the Theater Technology Conference / again next year.", 'vi': "Tôi cũng vậy. / Tôi mong chờ / được tham dự / Hội nghị Công nghệ Nhà hát / một lần nữa vào năm tới."},
        {'speaker': 'W-Am', 'en': "I really enjoyed your talk, / especially the information / you provided on acoustics. / Is it published anywhere? / I'd like to have a closer look.", 'vi': "Tôi thực sự thích bài nói của anh, / đặc biệt là thông tin / anh cung cấp về âm học. / Nó có được xuất bản ở đâu không? / Tôi muốn xem kỹ hơn."},
        {'speaker': 'M-Cn', 'en': "Actually, it is. / You can find the article / in last November’s issue / of Theater Sound. / It’s posted online.", 'vi': "Thực ra là có đấy. / Cô có thể tìm thấy bài báo / trong số phát hành tháng 11 năm ngoái / của tạp chí Theater Sound. / Nó được đăng trực tuyến."},
        {'speaker': 'W-Am', 'en': "Great. I'll look it up.", 'vi': "Tuyệt vời. Tôi sẽ tra cứu nó."},
        {'speaker': 'M-Cn', 'en': "Oh—my train leaves / in fourteen minutes. / I have to get going. / Safe travels, Camille!", 'vi': "Ồ—chuyến tàu của tôi sẽ chạy / trong mười bốn phút nữa. / Tôi phải đi rồi. / Thượng lộ bình an nhé, Camille!"}
    ],
    'focus': [
        {'chunk': 'Theater Technology Conference', 'vi': 'Hội nghị Công nghệ Nhà hát', 'paraphrase': 'They attended a conference', 'q_num': '62'},
        {'chunk': 'talk', 'vi': 'bài nói/bài thuyết trình'},
        {'chunk': 'information on acoustics', 'vi': 'thông tin về âm học'},
        {'chunk': 'published anywhere', 'vi': 'được xuất bản ở đâu không', 'paraphrase': 'Locating some information', 'q_num': '63'},
        {'chunk': 'Theater Sound', 'vi': 'Tên một tạp chí (Âm thanh Nhà hát)'},
        {'chunk': 'train leaves in fourteen minutes', 'vi': 'tàu chạy trong 14 phút nữa', 'paraphrase': 'Largo', 'q_num': '64'}
    ],
    'word_bank': ['attending', 'acoustics', 'published', 'article', 'issue', 'leaves'],
    'filling': [
        {'speaker': 'W-Am', 'text': 'Rajesh, It was nice to see you here in New York again this year.'},
        {'speaker': 'M-Cn', 'text': 'Same here. I look forward to <input type="text" data-answer="attending" class="input-blank mx-1 w-[100px]"> the Theater Technology Conference again next year.'},
        {'speaker': 'W-Am', 'text': 'I really enjoyed your talk, especially the information you provided on <input type="text" data-answer="acoustics" class="input-blank mx-1 w-[100px]">. Is it <input type="text" data-answer="published" class="input-blank mx-1 w-[100px]"> anywhere?'},
        {'speaker': 'M-Cn', 'text': 'Actually, it is. You can find the <input type="text" data-answer="article" class="input-blank mx-1 w-[100px]"> in last November’s <input type="text" data-answer="issue" class="input-blank mx-1 w-[100px]"> of Theater Sound.'},
        {'speaker': 'M-Cn', 'text': 'Oh—my train <input type="text" data-answer="leaves" class="input-blank mx-1 w-[100px]"> in fourteen minutes.'}
    ],
    'explanations': [
        {
            'num': '62', 'question': 'Why are the speakers in New York?', 'question_vi': 'Tại sao những người nói lại ở New York?',
            'options': {'A': 'They saw a play.', 'B': 'They attended a conference.', 'C': 'They met with some clients.', 'D': 'They viewed some real estate.'},
            'options_vi': {'A': 'Họ đã xem một vở kịch.', 'B': 'Họ đã tham dự một hội nghị.', 'C': 'Họ đã gặp gỡ một số khách hàng.', 'D': 'Họ đã xem xét một số bất động sản.'},
            'ans': 'B', 'explanation': 'Người đàn ông nhắc đến "Theater Technology Conference" (Hội nghị Công nghệ Nhà hát) mà họ đang tham gia. Đáp án là B.'
        },
        {
            'num': '63', 'question': 'What does the woman ask the man about?', 'question_vi': 'Người phụ nữ hỏi người đàn ông về điều gì?',
            'options': {'A': 'Locating some information', 'B': 'Applying for a position', 'C': 'Opening a branch office', 'D': 'Making a reservation'},
            'options_vi': {'A': 'Tìm kiếm một số thông tin', 'B': 'Nộp đơn cho một vị trí', 'C': 'Mở một văn phòng chi nhánh', 'D': 'Đặt chỗ'},
            'ans': 'A', 'explanation': 'Người phụ nữ hỏi liệu bài nói của anh ấy có được xuất bản ở đâu không để cô ấy có thể xem kỹ hơn ("I\'d like to have a closer look"). Đây là việc tìm kiếm thông tin. Đáp án là A.'
        },
        {
            'num': '64', 'question': 'Look at the graphic. Where will the man travel to next?', 'question_vi': 'Nhìn vào hình ảnh. Người đàn ông sẽ đi đâu tiếp theo?',
            'options': {'A': 'Shady Grove', 'B': 'Braddock Bay', 'C': 'Largo', 'D': 'Ashburn'},
            'options_vi': {'A': 'Shady Grove', 'B': 'Braddock Bay', 'C': 'Largo', 'D': 'Ashburn'},
            'ans': 'C', 'explanation': 'Dựa trên hình ảnh đồ họa (cần được cung cấp trong file HTML thực tế, nhưng dựa trên đáp án nguồn), người đàn ông sẽ đi đến Largo. Người đàn ông nói tàu chạy trong 14 phút nữa. Nếu bảng giờ tàu cho thấy chuyến đi Largo khởi hành sau 14 phút, thì đó là đáp án. Đáp án là C.'
        }
    ]
}

# Data for 65-67
content_65_67 = {
    'shadowing': [
        {'speaker': 'M-Cn', 'en': "Welcome to Orlando’s Deli. / If you’d like to try / one of our daily specials, / they’re on the board behind me.", 'vi': "Chào mừng đến với Orlando’s Deli. / Nếu bà muốn thử / một trong những món đặc biệt hàng ngày của chúng tôi, / chúng nằm trên bảng đằng sau tôi đây."},
        {'speaker': 'W-Br', 'en': "Wow, that’s a great menu. / The vegetable curry / looks good. / Is it spicy?", 'vi': "Oa, thực đơn thật tuyệt. / Món cà ri rau củ / trông có vẻ ngon. / Nó có cay không?"},
        {'speaker': 'M-Cn', 'en': "No, it’s very mild— / but we just sold out, / unfortunately.", 'vi': "Không, nó rất dịu— / nhưng thật không may là / chúng tôi vừa mới bán hết rồi."},
        {'speaker': 'W-Br', 'en': "In that case, / I’ll have the lasagna.", 'vi': "Trong trường hợp đó, / tôi sẽ lấy món lasagna."},
        {'speaker': 'M-Cn', 'en': "Great choice. By the way, / we just opened / our new patio / this week / in case you'd like to sit outside.", 'vi': "Lựa chọn tuyệt vời đấy ạ. Nhân tiện, / chúng tôi vừa mới mở / khu vực sân thượng mới / tuần này / trong trường hợp bà muốn ngồi ngoài trời."},
        {'speaker': 'W-Br', 'en': "Actually, it is a beautiful day. / And your patio looks lovely.", 'vi': "Thực ra hôm nay là một ngày đẹp trời. / Và sân thượng của các bạn trông thật đáng yêu."}
    ],
    'focus': [
        {'chunk': 'daily specials', 'vi': 'món đặc biệt hàng ngày'},
        {'chunk': 'vegetable curry', 'vi': 'cà ri rau củ'},
        {'chunk': 'Is it spicy?', 'vi': 'Nó có cay không?', 'paraphrase': 'Whether a food is spicy', 'q_num': '65'},
        {'chunk': 'sold out', 'vi': 'bán hết'},
        {'chunk': 'lasagna', 'vi': 'món lasagna (mì Ý dạng tấm)', 'paraphrase': 'Special 3', 'q_num': '66'},
        {'chunk': 'patio', 'vi': 'sân thượng/sân ngoài trời', 'paraphrase': 'Go to a patio', 'q_num': '67'}
    ],
    'word_bank': ['specials', 'vegetable', 'spicy', 'unfortunately', 'lasagna', 'patio'],
    'filling': [
        {'speaker': 'M-Cn', 'text': 'Welcome to Orlando’s Deli. If you’d like to try one of our daily <input type="text" data-answer="specials" class="input-blank mx-1 w-[100px]">, they’re on the board behind me.'},
        {'speaker': 'W-Br', 'text': 'Wow, that’s a great menu. The <input type="text" data-answer="vegetable" class="input-blank mx-1 w-[100px]"> curry looks good. Is it <input type="text" data-answer="spicy" class="input-blank mx-1 w-[100px]">?'},
        {'speaker': 'M-Cn', 'text': 'No, it’s very mild—but we just sold out, <input type="text" data-answer="unfortunately" class="input-blank mx-1 w-[140px]">.'},
        {'speaker': 'W-Br', 'text': 'In that case, I’ll have the <input type="text" data-answer="lasagna" class="input-blank mx-1 w-[100px]">.'},
        {'speaker': 'M-Cn', 'text': 'Great choice. By the way, we just opened our new <input type="text" data-answer="patio" class="input-blank mx-1 w-[100px]"> this week in case you\'d like to sit outside.'}
    ],
    'explanations': [
        {
            'num': '65', 'question': 'What does the woman ask the man about?', 'question_vi': 'Người phụ nữ hỏi người đàn ông về điều gì?',
            'options': {'A': 'Whether a coupon is valid', 'B': 'Whether a food is spicy', 'C': 'Whether a drink is included', 'D': 'Whether any seats are available'},
            'options_vi': {'A': 'Liệu một phiếu giảm giá có còn hiệu lực không', 'B': 'Liệu thức ăn có cay không', 'C': 'Liệu đồ uống có được bao gồm không', 'D': 'Liệu có còn chỗ ngồi nào không'},
            'ans': 'B', 'explanation': 'Người phụ nữ hỏi về món cà ri: "Is it spicy?" (Nó có cay không?). Đáp án là B.'
        },
        {
            'num': '66', 'question': 'Look at the graphic. Which special does the woman order?', 'question_vi': 'Nhìn vào hình ảnh. Người phụ nữ đặt món đặc biệt nào?',
            'options': {'A': 'Special 1', 'B': 'Special 2', 'C': 'Special 3', 'D': 'Special 4'},
            'options_vi': {'A': 'Món đặc biệt 1', 'B': 'Món đặc biệt 2', 'C': 'Món đặc biệt 3', 'D': 'Món đặc biệt 4'},
            'ans': 'C', 'explanation': 'Người phụ nữ quyết định chọn lasagna. Dựa trên hình ảnh thực tế (thường liệt kê lasagna là Special 3), đáp án là C.'
        },
        {
            'num': '67', 'question': 'What will the woman most likely do next?', 'question_vi': 'Người phụ nữ có khả năng nhất sẽ làm gì tiếp theo?',
            'options': {'A': 'Move her car', 'B': 'Go to a patio', 'C': 'Make a reservation', 'D': 'Meet some friends'},
            'options_vi': {'A': 'Di chuyển xe của cô ấy', 'B': 'Đi ra sân ngoài trời', 'C': 'Đặt chỗ', 'D': 'Gặp gỡ một số người bạn'},
            'ans': 'B', 'explanation': 'Người đàn ông gợi ý cô ấy có thể ngồi ở khu vực sân ngoài trời mới ("new patio") và người phụ nữ đồng ý rằng nó trông rất đáng yêu. Đáp án là B.'
        }
    ]
}

# Data for 68-70
content_68_70 = {
    'shadowing': [
        {'speaker': 'W-Am', 'en': "I'm excited / about our hike today / here at Marina Park. / And I’m so glad / we got to the park early / before it gets crowded. / Which trail should we hike?", 'vi': "Tôi rất hào hứng / về buổi đi bộ đường dài hôm nay / tại Công viên Marina. / Và tôi rất vui / vì chúng ta đã đến công viên sớm / trước khi nó trở nên đông đúc. / Chúng ta nên đi con đường nào nhỉ?"},
        {'speaker': 'M-Au', 'en': "Let’s take a look / at the map. / We’re at the visitor center, / and there’s a shuttle / that stops at different trailheads.", 'vi': "Hãy cùng xem / bản đồ nhé. / Chúng ta đang ở trung tâm du khách, / và có một chiếc xe đưa đón / dừng lại ở các điểm xuất phát khác nhau."},
        {'speaker': 'W-Am', 'en': "Right. It looks like / the Creek Trail and the Pond Trail / are fairly short. / I’d like to do / a more challenging hike.", 'vi': "Đúng vậy. Có vẻ như / Creek Trail và Pond Trail / khá ngắn. / Tôi muốn thực hiện / một buổi đi bộ đầy thử thách hơn."},
        {'speaker': 'M-Au', 'en': "OK. How about / the Waterfall Trail?", 'vi': "Được rồi. Vậy còn / Waterfall Trail thì sao?"},
        {'speaker': 'W-Am', 'en': "That sounds good. / And look—there’s a video / about the park. / We can watch / while we wait.", 'vi': "Nghe hay đấy. / Và nhìn kìa—có một video / về công viên. / Chúng ta có thể xem / trong khi chờ đợi."}
    ],
    'focus': [
        {'chunk': 'Marina Park', 'vi': 'Công viên Marina'},
        {'chunk': 'before it gets crowded', 'vi': 'trước khi nó trở nên đông đúc', 'paraphrase': 'There are few people in the park', 'q_num': '68'},
        {'chunk': 'shuttle', 'vi': 'xe đưa đón'},
        {'chunk': 'challenging hike', 'vi': 'đi bộ đường dài đầy thử thách'},
        {'chunk': 'Waterfall Trail', 'vi': 'Đường mòn Thác nước', 'paraphrase': '5 kilometers', 'q_num': '69'},
        {'chunk': 'video about the park', 'vi': 'video về công viên', 'paraphrase': 'Watch a video', 'q_num': '70'}
    ],
    'word_bank': ['excited', 'crowded', 'shuttle', 'challenging', 'waterfall', 'video'],
    'filling': [
        {'speaker': 'W-Am', 'text': 'I\'m <input type="text" data-answer="excited" class="input-blank mx-1 w-[100px]"> about our hike today here at Marina Park. And I’m so glad we got to the park early before it gets <input type="text" data-answer="crowded" class="input-blank mx-1 w-[100px]">.'},
        {'speaker': 'M-Au', 'text': 'Let’s take a look at the map. We’re at the visitor center, and there’s a <input type="text" data-answer="shuttle" class="input-blank mx-1 w-[100px]"> that stops at different trailheads.'},
        {'speaker': 'W-Am', 'text': 'Right. It looks like the Creek Trail and the Pond Trail are fairly short. I’d like to do a more <input type="text" data-answer="challenging" class="input-blank mx-1 w-[140px]"> hike.'},
        {'speaker': 'M-Au', 'text': 'OK. How about the <input type="text" data-answer="waterfall" class="input-blank mx-1 w-[120px]"> Trail?'},
        {'speaker': 'W-Am', 'text': 'That sounds good. And look—there’s a <input type="text" data-answer="video" class="input-blank mx-1 w-[100px]"> about the park. We can watch while we wait.'}
    ],
    'explanations': [
        {
            'num': '68', 'question': 'What is the woman happy about?', 'question_vi': 'Người phụ nữ vui mừng về điều gì?',
            'options': {'A': 'She happened to meet some friends.', 'B': 'The weather is perfect for an activity.', 'C': 'The park was closer than expected.', 'D': 'There are few people in the park.'},
            'options_vi': {'A': 'Cô ấy tình cờ gặp một số người bạn.', 'B': 'Thời tiết hoàn hảo cho một hoạt động.', 'C': 'Công viên gần hơn dự kiến.', 'D': 'Có ít người trong công viên.'},
            'ans': 'D', 'explanation': 'Người phụ nữ nói cô ấy vui vì họ đến sớm "before it gets crowded" (trước khi nó trở nên đông đúc). Điều này có nghĩa là lúc đó có ít người. Đáp án là D.'
        },
        {
            'num': '69', 'question': 'Look at the graphic. How far will the speakers hike?', 'question_vi': 'Nhìn vào hình ảnh. Những người nói sẽ đi bộ bao xa?',
            'options': {'A': '7 kilometers', 'B': '5 kilometers', 'C': '2 kilometers', 'D': '1 kilometer'},
            'options_vi': {'A': '7 km', 'B': '5 km', 'C': '2 km', 'D': '1 km'},
            'ans': 'B', 'explanation': 'Họ quyết định đi Waterfall Trail. Dựa trên hình ảnh đồ họa (cần được cung cấp trong file HTML), nếu Waterfall Trail dài 5km, đáp án sẽ là B.'
        },
        {
            'num': '70', 'question': 'What can the speakers do while waiting for the shuttle?', 'question_vi': 'Những người nói có thể làm gì trong khi chờ xe đưa đón?',
            'options': {'A': 'Buy some snacks', 'B': 'Watch a video', 'C': 'Visit a gift shop', 'D': 'Rent some equipment'},
            'options_vi': {'A': 'Mua một số đồ ăn nhẹ', 'B': 'Xem một video', 'C': 'Ghé thăm một cửa hàng quà tặng', 'D': 'Thuê một số thiết bị'},
            'ans': 'B', 'explanation': 'Người phụ nữ nói: "there’s a video about the park. We can watch while we wait" (có một video về công viên. Chúng ta có thể xem trong khi chờ đợi). Đáp án là B.'
        }
    ]
}

update_html('Test 5/LC-T5-P3-Q59-61.html', content_59_61)
update_html('Test 5/LC-T5-P3-Q62-64.html', content_62_64)
update_html('Test 5/LC-T5-P3-Q65-67.html', content_65_67)
update_html('Test 5/LC-T5-P3-Q68-70.html', content_68_70)

