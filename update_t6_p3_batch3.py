import json
import os
import re
from update_t6_p3 import update_html

# Data for 56-58
content_56_58 = {
    'shadowing': [
        {'speaker': 'M-Au', 'en': "Hi, Carmen. / l’ve just reviewed / the outline you gave me / for the nature documentary / we’re making. / I think it’ll be a great film, / but I’m a bit concerned. / I want it to be / less than an hour.", 'vi': "Chào Carmen. / Tôi vừa xem lại / bản phác thảo cô đưa cho tôi / cho bộ phim tài liệu thiên nhiên / mà chúng ta đang thực hiện. / Tôi nghĩ đó sẽ là một bộ phim tuyệt vời, / nhưng tôi hơi lo ngại một chút. / Tôi muốn nó dài / ít hơn một giờ."},
        {'speaker': 'W-Br', 'en': "I understand. / I'll take another look at it / and see / where I can take out / some unnecessary scenes / from the storyboard.", 'vi': "Tôi hiểu rồi. / Tôi sẽ xem xét lại một lần nữa / và xem / nơi nào tôi có thể lược bỏ / một số cảnh không cần thiết / khỏi kịch bản hình ảnh (storyboard)."},
        {'speaker': 'M-Au', 'en': "Great. In the meantime, / I need to follow up / with our camera team / to make sure / they have all the equipment / they need / to begin filming.", 'vi': "Tuyệt vời. Trong lúc chờ đợi, / tôi cần liên hệ lại / với đội quay phim của chúng ta / để đảm bảo / họ có đầy đủ thiết bị / họ cần / để bắt đầu quay phim."}
    ],
    'focus': [
        {'chunk': 'nature documentary we’re making', 'vi': 'phim tài liệu thiên nhiên đang làm', 'paraphrase': 'Filmmaking', 'q_num': '56'},
        {'chunk': 'outline', 'vi': 'bản phác thảo'},
        {'chunk': 'less than an hour', 'vi': 'ít hơn một giờ', 'paraphrase': 'Some revisions are needed', 'q_num': '57'},
        {'chunk': 'take out unnecessary scenes', 'vi': 'lược bỏ những cảnh không cần thiết'},
        {'chunk': 'storyboard', 'vi': 'kịch bản hình ảnh'},
        {'chunk': 'camera team', 'vi': 'đội quay phim'},
        {'chunk': 'equipment they need to begin filming', 'vi': 'thiết bị họ cần để bắt đầu quay', 'paraphrase': 'To confirm equipment availability', 'q_num': '58'}
    ],
    'word_bank': ['reviewed', 'documentary', 'concerned', 'unnecessary', 'storyboard', 'equipment'],
    'filling': [
        {'speaker': 'M-Au', 'text': 'Hi, Carmen. l’ve just <input type="text" data-answer="reviewed" class="input-blank mx-1 w-[100px]"> the outline you gave me for the nature <input type="text" data-answer="documentary" class="input-blank mx-1 w-[120px]"> we’re making.'},
        {'speaker': 'M-Au', 'text': 'I think it’ll be a great film, but I’m a bit <input type="text" data-answer="concerned" class="input-blank mx-1 w-[100px]">. I want it to be less than an hour.'},
        {'speaker': 'W-Br', 'text': 'I\'ll take another look at it and see where I can take out some <input type="text" data-answer="unnecessary" class="input-blank mx-1 w-[120px]"> scenes from the <input type="text" data-answer="storyboard" class="input-blank mx-1 w-[120px]">.'},
        {'speaker': 'M-Au', 'text': 'I need to follow up with our camera team to make sure they have all the <input type="text" data-answer="equipment" class="input-blank mx-1 w-[120px]"> they need to begin filming.'}
    ],
    'explanations': [
        {
            'num': '56', 'question': 'What industry do the speakers most likely work in?', 'question_vi': 'Những người nói có khả năng nhất làm việc trong ngành nào?',
            'options': {'A': 'Fashion photography', 'B': 'Information technology', 'C': 'Filmmaking', 'D': 'Marketing'},
            'options_vi': {'A': 'Nhiếp ảnh thời trang', 'B': 'Công nghệ thông tin', 'C': 'Làm phim', 'D': 'Tiếp thị'},
            'ans': 'C', 'explanation': 'Người đàn ông nhắc đến "nature documentary" (phim tài liệu thiên nhiên) và việc "filming" (quay phim). Điều này chỉ ra họ làm việc trong ngành làm phim. Đáp án là C.'
        },
        {
            'num': '57', 'question': 'What does the man imply when he says, “I want it to be less than an hour”?', 'question_vi': 'Người đàn ông ngụ ý điều gì khi nói: "Tôi muốn nó dài ít hơn một giờ"?',
            'options': {'A': 'He is very busy.', 'B': 'He approves an itinerary.', 'C': 'A route has a lot of traffic.', 'D': 'Some revisions are needed.'},
            'options_vi': {'A': 'Ông ấy rất bận.', 'B': 'Ông ấy chấp thuận một hành trình.', 'C': 'Một con đường có nhiều phương tiện giao thông.', 'D': 'Cần có một số sửa đổi.'},
            'ans': 'D', 'explanation': 'Yêu cầu phim ngắn hơn 1 giờ ngụ ý rằng nội dung hiện tại đang quá dài và cần được chỉnh sửa, cắt bỏ bớt. Người phụ nữ cũng trả lời sẽ lược bỏ những cảnh không cần thiết. Đáp án là D.'
        },
        {
            'num': '58', 'question': 'Why does the man need to contact a team?', 'question_vi': 'Tại sao người đàn ông cần liên hệ với một đội ngũ?',
            'options': {'A': 'To explain a permit procedure', 'B': 'To confirm equipment availability', 'C': 'To introduce a colleague', 'D': 'To devise a safety plan'},
            'options_vi': {'A': 'Để giải thích một thủ tục cấp phép', 'B': 'Để xác nhận sự sẵn có của thiết bị', 'C': 'Để giới thiệu một đồng nghiệp', 'D': 'Để lập một kế hoạch an toàn'},
            'ans': 'B', 'explanation': 'Người đàn ông nói ông cần liên hệ với đội quay phim để "make sure they have all the equipment they need to begin filming" (đảm bảo họ có đầy đủ thiết bị cần thiết để bắt đầu quay). Đáp án là B.'
        }
    ]
}

# Data for 59-61
content_59_61 = {
    'shadowing': [
        {'speaker': 'M-Au', 'en': "Kriti and Melissa, / I reviewed the results / of the soil tests yesterday, / and most of the sports fields / we manage / have healthy soil.", 'vi': "Kriti và Melissa, / tôi đã xem xét kết quả / của các bài kiểm tra đất hôm qua, / và hầu hết các sân thể thao / mà chúng ta quản lý / đều có đất khỏe mạnh."},
        {'speaker': 'M-Au', 'en': "But unfortunately, / the baseball field on Smith Drive / has elevated levels of potassium.", 'vi': "Nhưng thật không may, / sân bóng chày trên đường Smith Drive / có mức kali tăng cao."},
        {'speaker': 'W-Am', 'en': "The grass on that field / is so brown and weedy. / Now we know why.", 'vi': "Cỏ trên sân đó / rất nâu và đầy cỏ dại. / Bây giờ chúng ta đã biết lý do tại sao rồi."},
        {'speaker': 'W-Br', 'en': "We’ll need to order / some special fertilizer / to put on it. / Do you think / we need approval / to do that?", 'vi': "Chúng ta sẽ cần đặt / một loại phân bón đặc biệt / để bón lên đó. / Chị có nghĩ / chúng ta cần sự chấp thuận / để làm việc đó không?"},
        {'speaker': 'M-Au', 'en': "Yes—since it’s / an unforeseen expense, / it has to be approved / by the acquisitions department. / Melissa, do you have time / to prepare a cost estimate?", 'vi': "Có chứ—vì đó là / một khoản chi phí không lường trước được, / nó phải được phê duyệt / bởi bộ phận thu mua. / Melissa, cô có thời gian / để chuẩn bị một bản ước tính chi phí không?"},
        {'speaker': 'W-Br', 'en': "Sure. It won’t take long. / I'll send it / by lunchtime, / and I'll cc you both / on the e-mail.", 'vi': "Chắc chắn rồi. Sẽ không mất nhiều thời gian đâu. / Tôi sẽ gửi nó / trước giờ ăn trưa, / và tôi sẽ gửi bản sao cho cả hai người / trong e-mail."}
    ],
    'focus': [
        {'chunk': 'soil tests', 'vi': 'kiểm tra đất', 'paraphrase': 'Some test results', 'q_num': '59'},
        {'chunk': 'elevated levels of potassium', 'vi': 'mức kali tăng cao'},
        {'chunk': 'brown and weedy', 'vi': 'nâu và đầy cỏ dại'},
        {'chunk': 'special fertilizer', 'vi': 'phân bón đặc biệt', 'paraphrase': 'Improve the condition of a sports field', 'q_num': '60'},
        {'chunk': 'unforeseen expense', 'vi': 'chi phí không lường trước được'},
        {'chunk': 'cost estimate', 'vi': 'ước tính chi phí', 'paraphrase': 'A cost estimate', 'q_num': '61'}
    ],
    'word_bank': ['reviewed', 'elevated', 'potassium', 'fertilizer', 'approval', 'unforeseen'],
    'filling': [
        {'speaker': 'M-Au', 'text': 'Kriti and Melissa, I <input type="text" data-answer="reviewed" class="input-blank mx-1 w-[100px]"> the results of the soil tests yesterday, and most of the sports fields we manage have healthy soil.'},
        {'speaker': 'M-Au', 'text': 'But unfortunately, the baseball field on Smith Drive has <input type="text" data-answer="elevated" class="input-blank mx-1 w-[100px]"> levels of <input type="text" data-answer="potassium" class="input-blank mx-1 w-[100px]">.'},
        {'speaker': 'W-Br', 'text': 'We’ll need to order some special <input type="text" data-answer="fertilizer" class="input-blank mx-1 w-[100px]"> to put on it. Do you think we need <input type="text" data-answer="approval" class="input-blank mx-1 w-[100px]"> to do that?'},
        {'speaker': 'M-Au', 'text': 'Yes—since it’s an <input type="text" data-answer="unforeseen" class="input-blank mx-1 w-[120px]"> expense, it has to be approved.'}
    ],
    'explanations': [
        {
            'num': '59', 'question': 'What did the man review yesterday?', 'question_vi': 'Người đàn ông đã xem xét cái gì vào ngày hôm qua?',
            'options': {'A': 'A budget', 'B': 'A weather report', 'C': 'Some test results', 'D': 'Some hiring plans'},
            'options_vi': {'A': 'Một ngân sách', 'B': 'Một dự báo thời tiết', 'C': 'Một số kết quả kiểm tra', 'D': 'Một số kế hoạch tuyển dụng'},
            'ans': 'C', 'explanation': 'Người đàn ông nói: "I reviewed the results of the soil tests yesterday" (Tôi đã xem xét kết quả của các bài kiểm tra đất hôm qua). Đáp án là C.'
        },
        {
            'num': '60', 'question': 'What do the speakers hope to do?', 'question_vi': 'Những người nói hy vọng làm được điều gì?',
            'options': {'A': 'Improve the condition of a sports field', 'B': 'Expand the city’s athletic programs', 'C': 'Plan a fund-raising event', 'D': 'Acquire more public land'},
            'options_vi': {'A': 'Cải thiện tình trạng của một sân thể thao', 'B': 'Mở rộng các chương trình thể thao của thành phố', 'C': 'Lên kế hoạch cho một sự kiện gây quỹ', 'D': 'Thu mua thêm đất công'},
            'ans': 'A', 'explanation': 'Họ đang bàn về việc dùng phân bón đặc biệt để xử lý sân bóng chày đang bị héo nâu và nhiều cỏ dại. Điều này có nghĩa là họ muốn cải thiện tình trạng của sân thể thao đó. Đáp án là A.'
        },
        {
            'num': '61', 'question': 'What will Melissa send by e-mail?', 'question_vi': 'Melissa sẽ gửi cái gì qua e-mail?',
            'options': {'A': 'A summary of work tasks', 'B': 'A letter of appreciation', 'C': 'A news article', 'D': 'A cost estimate'},
            'options_vi': {'A': 'Bản tóm tắt các nhiệm vụ công việc', 'B': 'Một lá thư cảm ơn', 'C': 'Một bài báo', 'D': 'Một bản ước tính chi phí'},
            'ans': 'D', 'explanation': 'Người đàn ông yêu cầu Melissa chuẩn bị một "cost estimate" (ước tính chi phí) và cô ấy đồng ý sẽ gửi nó trước giờ ăn trưa. Đáp án là D.'
        }
    ]
}

# Data for 62-64
content_62_64 = {
    'shadowing': [
        {'speaker': 'W-Am', 'en': "Rodrigo, / you wanted to talk to me / about the schedule / for the bowling leagues / at our alley?", 'vi': "Rodrigo, / anh muốn nói chuyện với tôi / về lịch trình / cho các giải bowling / tại ngõ (sân) của chúng ta phải không?"},
        {'speaker': 'M-Cn', 'en': "Yes. As you know, / many of the members / in the adult league / have young children / who participate / in the junior league.", 'vi': "Vâng. Như chị đã biết, / nhiều thành viên / trong giải đấu dành cho người lớn / có con nhỏ / tham gia / vào giải đấu dành cho thiếu nhi."},
        {'speaker': 'M-Cn', 'en': "And they explained to me / that it would be / really convenient / if we moved the junior league / to the same night / that the adult league plays. / That way / they could all come together / on the same night.", 'vi': "Và họ đã giải thích với tôi / rằng sẽ rất thuận tiện / nếu chúng ta chuyển giải đấu thiếu nhi / sang cùng một buổi tối / mà giải người lớn thi đấu. / Bằng cách đó / họ có thể đi cùng nhau / trong cùng một đêm."},
        {'speaker': 'W-Am', 'en': "That’s a great idea. / We have a few / available bowling lanes / on that day / that the junior league can use.", 'vi': "Đó là một ý tưởng tuyệt vời. / Chúng ta có một vài / đường băng bowling trống / vào ngày đó / mà giải thiếu nhi có thể sử dụng."},
        {'speaker': 'W-Am', 'en': "I’ll e-mail the parents / of the junior bowlers / and let them know / the day will change / starting next month.", 'vi': "Tôi sẽ gửi e-mail cho phụ huynh / của các vận động viên thiếu nhi / và cho họ biết / ngày thi đấu sẽ thay đổi / bắt đầu từ tháng tới."}
    ],
    'focus': [
        {'chunk': 'bowling leagues at our alley', 'vi': 'các giải bowling tại sân của mình', 'paraphrase': 'At a bowling alley', 'q_num': '62'},
        {'chunk': 'adult league', 'vi': 'giải đấu người lớn'},
        {'chunk': 'junior league', 'vi': 'giải đấu thiếu nhi'},
        {'chunk': 'convenient', 'vi': 'thuận tiện'},
        {'chunk': 'same night the adult league plays', 'vi': 'cùng đêm giải người lớn thi đấu', 'paraphrase': 'Thursday', 'q_num': '63'},
        {'chunk': 'available bowling lanes', 'vi': 'đường băng bowling trống'},
        {'chunk': 'e-mail the parents', 'vi': 'gửi e-mail cho phụ huynh', 'paraphrase': 'Send an e-mail', 'q_num': '64'}
    ],
    'word_bank': ['schedule', 'leagues', 'alley', 'participate', 'convenient', 'available'],
    'filling': [
        {'speaker': 'W-Am', 'text': 'Rodrigo, you wanted to talk to me about the <input type="text" data-answer="schedule" class="input-blank mx-1 w-[100px]"> for the bowling <input type="text" data-answer="leagues" class="input-blank mx-1 w-[100px]"> at our <input type="text" data-answer="alley" class="input-blank mx-1 w-[100px]">?'},
        {'speaker': 'M-Cn', 'text': 'Many of the members in the adult league have young children who <input type="text" data-answer="participate" class="input-blank mx-1 w-[100px]"> in the junior league.'},
        {'speaker': 'M-Cn', 'text': 'It would be really <input type="text" data-answer="convenient" class="input-blank mx-1 w-[120px]"> if we moved the junior league to the same night that the adult league plays.'},
        {'speaker': 'W-Am', 'text': 'We have a few <input type="text" data-answer="available" class="input-blank mx-1 w-[100px]"> bowling lanes on that day.'}
    ],
    'explanations': [
        {
            'num': '62', 'question': 'Where do the speakers work?', 'question_vi': 'Những người nói làm việc ở đâu?',
            'options': {'A': 'At a bowling alley', 'B': 'At a swimming pool', 'C': 'At an ice-skating rink', 'D': 'At a baseball field'},
            'options_vi': {'A': 'Tại một sân chơi bowling', 'B': 'Tại một hồ bơi', 'C': 'Tại một sân trượt băng', 'D': 'Tại một sân bóng chày'},
            'ans': 'A', 'explanation': 'Họ đang thảo luận về "bowling leagues" (các giải đấu bowling) tại "our alley" (sân/ngõ bowling của chúng ta). Đáp án là A.'
        },
        {
            'num': '63', 'question': 'Look at the graphic. On which day will the Junior League meet starting next month?', 'question_vi': 'Nhìn vào hình ảnh. Giải đấu thiếu nhi sẽ gặp nhau vào ngày nào bắt đầu từ tháng tới?',
            'options': {'A': 'Monday', 'B': 'Tuesday', 'C': 'Wednesday', 'D': 'Thursday'},
            'options_vi': {'A': 'Thứ Hai', 'B': 'Thứ Ba', 'C': 'Thứ Tư', 'D': 'Thứ Năm'},
            'ans': 'D', 'explanation': 'Họ sẽ chuyển giải thiếu nhi sang cùng ngày với giải người lớn. Dựa trên hình ảnh đồ họa (file HTML), nếu giải người lớn diễn ra vào thứ Năm, đáp án sẽ là D.'
        },
        {
            'num': '64', 'question': 'What does the woman say she will do?', 'question_vi': 'Người phụ nữ nói cô ấy sẽ làm gì?',
            'options': {'A': 'Hang a poster', 'B': 'Send an e-mail', 'C': 'Deliver a package', 'D': 'Process a payment'},
            'options_vi': {'A': 'Treo một tấm áp phích', 'B': 'Gửi một e-mail', 'C': 'Giao một kiện hàng', 'D': 'Xử lý một khoản thanh toán'},
            'ans': 'B', 'explanation': 'Người phụ nữ nói: "I’ll e-mail the parents of the junior bowlers" (Tôi sẽ gửi e-mail cho phụ huynh của các vận động viên thiếu nhi). Đáp án là B.'
        }
    ]
}

# Data for 65-67
content_65_67 = {
    'shadowing': [
        {'speaker': 'M-Cn', 'en': "Hi. / Where can I find / a schedule of library events?", 'vi': "Xin chào. / Tôi có thể tìm / lịch trình các sự kiện của thư viện ở đâu?"},
        {'speaker': 'W-Br', 'en': "Oh, I’ve got it right here. / We usually have events / almost every day, / but we're closed this Friday. / The library is being used / for the district elections.", 'vi': "Ồ, tôi có nó ngay đây rồi. / Chúng tôi thường có các sự kiện / hầu như mỗi ngày, / nhưng chúng tôi đóng cửa vào thứ Sáu này. / Thư viện đang được sử dụng / cho cuộc bầu cử khu vực."},
        {'speaker': 'M-Cn', 'en': "I see. / Are there any movies / showing?", 'vi': "Tôi hiểu rồi. / Có bộ phim nào / đang chiếu không?"},
        {'speaker': 'W-Br', 'en': "Yes, there’s one / on Thursday evening.", 'vi': "Có, có một phim / vào tối thứ Năm."},
        {'speaker': 'M-Cn', 'en': "Oh, too bad. / I’m away / for a client meeting / on Thursday.", 'vi': "Ồ, tệ thật. / Tôi đi vắng / để gặp khách hàng / vào thứ Năm."},
        {'speaker': 'W-Br', 'en': "Well, if you like / Sumit Mehta’s books, / you might be interested / in his book signing.", 'vi': "À, nếu ông thích / sách của Sumit Mehta, / ông có thể sẽ quan tâm / đến buổi ký tặng sách của ông ấy đấy."},
        {'speaker': 'M-Cn', 'en': "I do like his novels! / Thanks, I’ll come back for that.", 'vi': "Tôi thực sự thích tiểu thuyết của ông ấy! / Cảm ơn nhé, tôi sẽ quay lại vì buổi đó."}
    ],
    'focus': [
        {'chunk': 'schedule of library events', 'vi': 'lịch sự kiện thư viện'},
        {'chunk': 'closed this Friday', 'vi': 'đóng cửa vào thứ Sáu này'},
        {'chunk': 'district elections', 'vi': 'cuộc bầu cử khu vực', 'paraphrase': 'An election will be held there', 'q_num': '65'},
        {'chunk': 'movies showing', 'vi': 'chiếu phim'},
        {'chunk': 'client meeting on Thursday', 'vi': 'gặp khách hàng vào thứ Năm', 'paraphrase': 'He has a business meeting', 'q_num': '66'},
        {'chunk': 'book signing', 'vi': 'buổi ký tặng sách', 'paraphrase': 'On Wednesday', 'q_num': '67'}
    ],
    'word_bank': ['schedule', 'elections', 'showing', 'conflict', 'obligation', 'novels'],
    'filling': [
        {'speaker': 'M-Cn', 'text': 'Hi. Where can I find a <input type="text" data-answer="schedule" class="input-blank mx-1 w-[100px]"> of library events?'},
        {'speaker': 'W-Br', 'text': 'The library is being used for the district <input type="text" data-answer="elections" class="input-blank mx-1 w-[100px]">.'},
        {'speaker': 'M-Cn', 'text': 'Are there any movies <input type="text" data-answer="showing" class="input-blank mx-1 w-[100px]">?'},
        {'speaker': 'M-Cn', 'text': 'I’m away for a client meeting on Thursday.'},
        {'speaker': 'M-Cn', 'text': 'I do like his <input type="text" data-answer="novels" class="input-blank mx-1 w-[100px]">! Thanks, I’ll come back for that.'}
    ],
    'explanations': [
        {
            'num': '65', 'question': 'According to the woman, why will the library be closed on Friday?', 'question_vi': 'Theo người phụ nữ, tại sao thư viện sẽ đóng cửa vào thứ Sáu?',
            'options': {'A': 'An election will be held there.', 'B': 'Some renovations will take place.', 'C': 'Bad weather is expected.', 'D': 'A national holiday will be observed.'},
            'options_vi': {'A': 'Một cuộc bầu cử sẽ được tổ chức ở đó.', 'B': 'Một số hoạt động tu sửa sẽ diễn ra.', 'C': 'Thời tiết xấu dự kiến sẽ xảy ra.', 'D': 'Một ngày lễ quốc gia sẽ được tổ chức.'},
            'ans': 'A', 'explanation': 'Người phụ nữ nói: "The library is being used for the district elections" (Thư viện đang được sử dụng cho cuộc bầu cử khu vực). Đáp án là A.'
        },
        {
            'num': '66', 'question': 'What schedule conflict does the man mention?', 'question_vi': 'Sự xung đột lịch trình nào mà người đàn ông đề cập?',
            'options': {'A': 'He has a family obligation.', 'B': 'His car will be at a mechanic’s shop.', 'C': 'He will be attending a performance.', 'D': 'He has a business meeting.'},
            'options_vi': {'A': 'Anh ấy có nghĩa vụ gia đình.', 'B': 'Xe của anh ấy sẽ ở tiệm sửa xe.', 'C': 'Anh ấy sẽ tham dự một buổi biểu diễn.', 'D': 'Anh ấy có một cuộc họp kinh doanh.'},
            'ans': 'D', 'explanation': 'Người đàn ông nói ông không thể xem phim vào thứ Năm vì: "I’m away for a client meeting on Thursday" (Tôi đi vắng để gặp khách hàng vào thứ Năm). Đây là một cuộc họp kinh doanh. Đáp án là D.'
        },
        {
            'num': '67', 'question': 'Look at the graphic. When will the man most likely attend a library event?', 'question_vi': 'Nhìn vào hình ảnh. Khi nào người đàn ông có khả năng nhất sẽ tham dự một sự kiện ở thư viện?',
            'options': {'A': 'On Monday', 'B': 'On Tuesday', 'C': 'On Wednesday', 'D': 'On Thursday'},
            'options_vi': {'A': 'Thứ Hai', 'B': 'Thứ Ba', 'C': 'Thứ Tư', 'D': 'Thứ Năm'},
            'ans': 'C', 'explanation': 'Người đàn ông nói ông sẽ quay lại để dự buổi ký tặng sách. Dựa trên hình ảnh đồ họa (file HTML), nếu buổi ký tặng sách của Sumit Mehta diễn ra vào thứ Tư, đáp án sẽ là C.'
        }
    ]
}

# Data for 68-70
content_68_70 = {
    'shadowing': [
        {'speaker': 'W-Br', 'en': "Good news, Tariq. / We'll have enough money / to make those repairs / to the bridge over the fish pond / that you mentioned. / We've been awarded a grant / to make some repairs / to the park grounds.", 'vi': "Tin tốt đây Tariq. / Chúng ta sẽ có đủ tiền / để tiến hành sửa chữa / cây cầu bắc qua ao cá / mà anh đã đề cập. / Chúng ta vừa được trao một khoản tài trợ / để thực hiện một số sửa chữa / cho khuôn viên công viên."},
        {'speaker': 'M-Au', 'en': "That's great! / That bridge needs / a new coat of paint / to protect it / from the elements. / I think I sent you / a list of paint colors / when I first talked to you / about the project.", 'vi': "Tuyệt quá! / Cây cầu đó cần / một lớp sơn mới / để bảo vệ nó / khỏi các yếu tố thời tiết. / Tôi nghĩ tôi đã gửi cho chị / một danh sách các màu sơn / khi tôi nói chuyện với chị lần đầu / về dự án này."},
        {'speaker': 'W-Br', 'en': "You did. / Because it’s such / an iconic symbol / of the park, / and it’s in so many photographs, / we want it to be / as close to the original color / as when it was first built, / even though that’s / the most expensive option / on the list.", 'vi': "Anh đã gửi rồi. / Bởi vì nó là / một biểu tượng mang tính hình tượng / của công viên, / và nó xuất hiện trong rất nhiều bức ảnh, / chúng tôi muốn nó / gần với màu gốc nhất / như khi nó mới được xây dựng lần đầu, / mặc dù đó là / lựa chọn đắt nhất / trong danh sách."}
    ],
    'focus': [
        {'chunk': 'repairs to the bridge over the fish pond', 'vi': 'sửa chữa cầu qua ao cá', 'paraphrase': 'Repairing a bridge', 'q_num': '68'},
        {'chunk': 'awarded a grant', 'vi': 'được trao một khoản tài trợ', 'paraphrase': 'With money from a grant', 'q_num': '69'},
        {'chunk': 'park grounds', 'vi': 'khuôn viên công viên'},
        {'chunk': 'new coat of paint', 'vi': 'lớp sơn mới'},
        {'chunk': 'iconic symbol', 'vi': 'biểu tượng mang tính hình tượng'},
        {'chunk': 'most expensive option', 'vi': 'lựa chọn đắt nhất', 'paraphrase': 'Misty Blue', 'q_num': '70'}
    ],
    'word_bank': ['repairs', 'mentioned', 'awarded', 'grant', 'elements', 'iconic'],
    'filling': [
        {'speaker': 'W-Br', 'text': 'Good news, Tariq. We\'ll have enough money to make those <input type="text" data-answer="repairs" class="input-blank mx-1 w-[100px]"> to the bridge over the fish pond that you <input type="text" data-answer="mentioned" class="input-blank mx-1 w-[100px]">.'},
        {'speaker': 'W-Br', 'text': 'We\'ve been <input type="text" data-answer="awarded" class="input-blank mx-1 w-[100px]"> a <input type="text" data-answer="grant" class="input-blank mx-1 w-[100px]"> to make some repairs to the park grounds.'},
        {'speaker': 'M-Au', 'text': 'That bridge needs a new coat of paint to protect it from the <input type="text" data-answer="elements" class="input-blank mx-1 w-[100px]">.'},
        {'speaker': 'W-Br', 'text': 'Because it’s such an <input type="text" data-answer="iconic" class="input-blank mx-1 w-[100px]"> symbol of the park, we want it to be as close to the original color.'}
    ],
    'explanations': [
        {
            'num': '68', 'question': 'What is the conversation about?', 'question_vi': 'Cuộc trò chuyện nói về vấn đề gì?',
            'options': {'A': 'Extending a fence', 'B': 'Building a storage shed', 'C': 'Repairing a bridge', 'D': 'Updating an entrance area'},
            'options_vi': {'A': 'Kéo dài một hàng rào', 'B': 'Xây dựng một nhà kho lưu trữ', 'C': 'Sửa chữa một cây cầu', 'D': 'Cập nhật một khu vực lối vào'},
            'ans': 'C', 'explanation': 'Người phụ nữ nói về việc sửa chữa "the bridge over the fish pond" (cây cầu bắc qua ao cá). Đáp án là C.'
        },
        {
            'num': '69', 'question': 'According to the woman, how is a project being funded?', 'question_vi': 'Theo người phụ nữ, một dự án đang được tài trợ như thế nào?',
            'options': {'A': 'With donations from visitors', 'B': 'With money from a grant', 'C': 'With revenue from ticket sales', 'D': 'With proceeds from a charity auction'},
            'options_vi': {'A': 'Với các khoản quyên góp từ khách du lịch', 'B': 'Với tiền từ một khoản tài trợ', 'C': 'Với doanh thu từ việc bán vé', 'D': 'Với số tiền thu được từ một cuộc đấu giá từ thiện'},
            'ans': 'B', 'explanation': 'Người phụ nữ nói: "We\'ve been awarded a grant to make some repairs" (Chúng ta vừa được trao một khoản tài trợ để thực hiện một số sửa chữa). Đáp án là B.'
        },
        {
            'num': '70', 'question': 'Look at the graphic. Which color does the woman select?', 'question_vi': 'Nhìn vào hình ảnh. Người phụ nữ chọn màu nào?',
            'options': {'A': 'Garden Green', 'B': 'Misty Blue', 'C': 'Sunrise Peach', 'D': 'Antique White'},
            'options_vi': {'A': 'Xanh lá vườn', 'B': 'Xanh sương mù', 'C': 'Đào bình minh', 'D': 'Trắng cổ điển'},
            'ans': 'B', 'explanation': 'Người phụ nữ chọn tùy chọn đắt nhất ("most expensive option"). Dựa trên hình ảnh đồ họa (file HTML), nếu Misty Blue là màu đắt nhất, đáp án sẽ là B.'
        }
    ]
}

update_html('Test 6/LC-T6-P3-Q56-58.html', content_56_58)
update_html('Test 6/LC-T6-P3-Q59-61.html', content_59_61)
update_html('Test 6/LC-T6-P3-Q62-64.html', content_62_64)
update_html('Test 6/LC-T6-P3-Q65-67.html', content_65_67)
update_html('Test 6/LC-T6-P3-Q68-70.html', content_68_70)

