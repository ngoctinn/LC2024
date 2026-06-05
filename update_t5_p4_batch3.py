import json
import os
import re
from update_t5_p4 import update_html

# Data for 95-97
content_95_97 = {
    'shadowing': [
        {'speaker': 'W-Am', 'en': "This is the custodial staff's cabinet / for cleaning supplies. / As part of your training, / you'll be expected to learn / which cleaning solutions / are used / for different surfaces in the hotel, / such as carpet and tile flooring.", 'vi': "Đây là tủ đựng đồ dùng vệ sinh / của nhân viên tạp vụ. / Là một phần trong quá trình đào tạo của các bạn, / các bạn sẽ phải học / loại dung dịch vệ sinh nào / được sử dụng / cho các bề mặt khác nhau trong khách sạn, / chẳng hạn như sàn trải thảm và sàn gạch."},
        {'speaker': 'W-Am', 'en': "The spray bottle on the top shelf, / Baxlon, is for glass surfaces. / The product directly / under the spray bottle / is brand new. / It was just released / this month, / and it’s excellent / for polishing furniture.", 'vi': "Chai xịt ở ngăn trên cùng, / Baxlon, dùng cho các bề mặt kính. / Sản phẩm ngay phía dưới / chai xịt đó / là loại hoàn toàn mới. / Nó vừa mới được ra mắt / trong tháng này, / và nó rất tuyệt vời / để đánh bóng đồ nội thất."},
        {'speaker': 'W-Am', 'en': "Oh, and every Tuesday / at one o'clock, / a delivery truck brings / any supplies / that we're low on. / Don’t forget / to check that.", 'vi': "Ồ, và vào mỗi thứ Ba / lúc một giờ, / một xe tải giao hàng sẽ mang đến / bất kỳ vật dụng nào / mà chúng ta sắp hết. / Đừng quên / kiểm tra việc đó nhé."}
    ],
    'focus': [
        {'chunk': 'custodial staff', 'vi': 'nhân viên tạp vụ/vệ sinh', 'paraphrase': 'To train employees', 'q_num': '95'},
        {'chunk': 'cleaning solutions', 'vi': 'dung dịch vệ sinh'},
        {'chunk': 'Baxlon, is for glass surfaces', 'vi': 'Baxlon dùng cho bề mặt kính'},
        {'chunk': 'released this month', 'vi': 'được ra mắt trong tháng này', 'paraphrase': 'Clean Sure', 'q_num': '96'},
        {'chunk': 'polishing furniture', 'vi': 'đánh bóng đồ nội thất'},
        {'chunk': 'delivery truck brings supplies', 'vi': 'xe tải giao hàng mang vật tư đến', 'paraphrase': 'A delivery arrives', 'q_num': '97'}
    ],
    'word_bank': ['custodial', 'cabinet', 'solutions', 'surfaces', 'released', 'polishing'],
    'filling': [
        {'speaker': 'W-Am', 'text': 'This is the <input type="text" data-answer="custodial" class="input-blank mx-1 w-[120px]"> staff\'s <input type="text" data-answer="cabinet" class="input-blank mx-1 w-[100px]"> for cleaning supplies.'},
        {'speaker': 'W-Am', 'text': 'As part of your training, you\'ll be expected to learn which cleaning <input type="text" data-answer="solutions" class="input-blank mx-1 w-[120px]"> are used for different <input type="text" data-answer="surfaces" class="input-blank mx-1 w-[100px]"> in the hotel.'},
        {'speaker': 'W-Am', 'text': 'The product directly under the spray bottle was just <input type="text" data-answer="released" class="input-blank mx-1 w-[100px]"> this month, and it’s excellent for <input type="text" data-answer="polishing" class="input-blank mx-1 w-[120px]"> furniture.'}
    ],
    'explanations': [
        {
            'num': '95', 'question': 'What is the purpose of the talk?', 'question_vi': 'Mục đích của bài nói chuyện là gì?',
            'options': {'A': 'To discuss a schedule', 'B': 'To consider changing suppliers', 'C': 'To train employees', 'D': 'To develop an inventory system'},
            'options_vi': {'A': 'Để thảo luận về một lịch trình', 'B': 'Để cân nhắc việc thay đổi nhà cung cấp', 'C': 'Để đào tạo nhân viên', 'D': 'Để phát triển một hệ thống kiểm kê'},
            'ans': 'C', 'explanation': 'Người nói cho biết: "As part of your training, you\'ll be expected to learn..." (Là một phần của quá trình đào tạo, các bạn sẽ phải học...). Đây là một buổi đào tạo nhân viên. Đáp án là C.'
        },
        {
            'num': '96', 'question': 'Look at the graphic. Which product does the speaker say is new?', 'question_vi': 'Nhìn vào hình ảnh. Người nói cho biết sản phẩm nào là mới?',
            'options': {'A': 'Klennlee', 'B': 'Baxlon', 'C': 'Z-Factor', 'D': 'Clean Sure'},
            'options_vi': {'A': 'Klennlee', 'B': 'Baxlon', 'C': 'Z-Factor', 'D': 'Clean Sure'},
            'ans': 'D', 'explanation': 'Người nói cho biết sản phẩm ngay bên dưới chai xịt (Baxlon) là sản phẩm mới. Dựa trên hình ảnh đồ họa (file HTML), nếu sản phẩm đó là Clean Sure, thì đáp án là D.'
        },
        {
            'num': '97', 'question': 'What happens at one o’clock on Tuesdays?', 'question_vi': 'Điều gì xảy ra vào lúc một giờ các ngày thứ Ba?',
            'options': {'A': 'An expense report is due.', 'B': 'A work shift begins.', 'C': 'A staff meeting is held.', 'D': 'A delivery arrives.'},
            'options_vi': {'A': 'Hết hạn nộp báo cáo chi phí.', 'B': 'Một ca làm việc bắt đầu.', 'C': 'Một cuộc họp nhân viên được tổ chức.', 'D': 'Một chuyến giao hàng đến.'},
            'ans': 'D', 'explanation': 'Người nói cho biết: "every Tuesday at one o\'clock, a delivery truck brings any supplies that we\'re low on" (vào mỗi thứ Ba lúc một giờ, một xe tải giao hàng sẽ mang đến những vật tư mà chúng ta sắp hết). Đáp án là D.'
        }
    ]
}

# Data for 98-100
content_98_100 = {
    'shadowing': [
        {'speaker': 'M-Au', 'en': "Welcome back / to this professional development workshop. / We’ll continue / from where we left off / in our discussion / on advertising / through social media / using videos, / and we'll end today’s meeting / by performing a group task.", 'vi': "Chào mừng các bạn quay trở lại / buổi hội thảo phát triển chuyên môn này. / Chúng ta sẽ tiếp tục / từ phần tạm dừng trước đó / trong cuộc thảo luận / về việc quảng cáo / thông qua mạng xã hội / bằng cách sử dụng video, / và chúng ta sẽ kết thúc cuộc họp hôm nay / bằng cách thực hiện một nhiệm vụ nhóm."},
        {'speaker': 'M-Au', 'en': "Last week, / we discussed the planning phase / for a video marketing campaign. / Today, we'll move on / to the production phase.", 'vi': "Tuần trước, / chúng ta đã thảo luận về giai đoạn lập kế hoạch / cho một chiến dịch tiếp thị video. / Hôm nay, chúng ta sẽ chuyển sang / giai đoạn sản xuất."},
        {'speaker': 'M-Au', 'en': "During this phase, / you'll need to ensure / that high-quality equipment / is used / for lighting and camera work / and that you have / the best video editors / you can get for the job.", 'vi': "Trong giai đoạn này, / các bạn sẽ cần đảm bảo / rằng các thiết bị chất lượng cao / được sử dụng / cho công việc chiếu sáng và quay phim / và rằng các bạn có / những người biên tập video tốt nhất / mà các bạn có thể thuê được cho công việc này."},
        {'speaker': 'M-Au', 'en': "We're very lucky / to have an expert here today / to talk about her experience / with the process. / Please give your attention / to Usha Madan.", 'vi': "Chúng ta rất may mắn / khi có một chuyên gia ở đây hôm nay / để nói về kinh nghiệm của cô ấy / với quy trình này. / Xin hãy dành sự chú ý / cho cô Usha Madan."}
    ],
    'focus': [
        {'chunk': 'professional development workshop', 'vi': 'hội thảo phát triển chuyên môn'},
        {'chunk': 'advertising through social media', 'vi': 'quảng cáo qua mạng xã hội', 'paraphrase': 'Marketing', 'q_num': '98'},
        {'chunk': 'planning phase', 'vi': 'giai đoạn lập kế hoạch'},
        {'chunk': 'production phase', 'vi': 'giai đoạn sản xuất', 'paraphrase': 'Step 3', 'q_num': '99'},
        {'chunk': 'high-quality equipment', 'vi': 'thiết bị chất lượng cao'},
        {'chunk': 'expert talk about her experience', 'vi': 'chuyên gia nói về kinh nghiệm của mình', 'paraphrase': 'Listen to a guest speaker', 'q_num': '100'}
    ],
    'word_bank': ['professional', 'workshop', 'advertising', 'campaign', 'production', 'equipment'],
    'filling': [
        {'speaker': 'M-Au', 'text': 'Welcome back to this <input type="text" data-answer="professional" class="input-blank mx-1 w-[120px]"> development <input type="text" data-answer="workshop" class="input-blank mx-1 w-[100px]">.'},
        {'speaker': 'M-Au', 'text': 'We’ll continue from where we left off in our discussion on <input type="text" data-answer="advertising" class="input-blank mx-1 w-[120px]"> through social media using videos.'},
        {'speaker': 'M-Au', 'text': 'Last week, we discussed the planning phase for a video marketing <input type="text" data-answer="campaign" class="input-blank mx-1 w-[120px]">. Today, we\'ll move on to the <input type="text" data-answer="production" class="input-blank mx-1 w-[120px]"> phase.'},
        {'speaker': 'M-Au', 'text': 'During this phase, you\'ll need to ensure that high-quality <input type="text" data-answer="equipment" class="input-blank mx-1 w-[120px]"> is used for lighting and camera work.'}
    ],
    'explanations': [
        {
            'num': '98', 'question': 'What is the topic of the course?', 'question_vi': 'Chủ đề của khóa học là gì?',
            'options': {'A': 'Marketing', 'B': 'Investing', 'C': 'Documentary filmmaking', 'D': 'Software development'},
            'options_vi': {'A': 'Tiếp thị', 'B': 'Đầu tư', 'C': 'Làm phim tài liệu', 'D': 'Phát triển phần mềm'},
            'ans': 'A', 'explanation': 'Người nói cho biết họ đang thảo luận về "advertising through social media using videos" (quảng cáo qua mạng xã hội bằng cách sử dụng video). Đây là một chủ đề thuộc Marketing. Đáp án là A.'
        },
        {
            'num': '99', 'question': 'Look at the graphic. Which step will be discussed today?', 'question_vi': 'Nhìn vào hình ảnh. Bước nào sẽ được thảo luận hôm nay?',
            'options': {'A': 'Step 1', 'B': 'Step 2', 'C': 'Step 3', 'D': 'Step 4'},
            'options_vi': {'A': 'Bước 1', 'B': 'Bước 2', 'C': 'Bước 3', 'D': 'Bước 4'},
            'ans': 'C', 'explanation': 'Người nói cho biết: "Last week, we discussed the planning phase... Today, we\'ll move on to the production phase" (Tuần trước chúng ta thảo luận giai đoạn lập kế hoạch... Hôm nay, chúng ta sẽ chuyển sang giai đoạn sản xuất). Nếu sản xuất là Step 3 trên đồ họa, đáp án là C.'
        },
        {
            'num': '100', 'question': 'What will the listeners do next?', 'question_vi': 'Những người nghe sẽ làm gì tiếp theo?',
            'options': {'A': 'Read a handout', 'B': 'Watch a video', 'C': 'Take a coffee break', 'D': 'Listen to a guest speaker'},
            'options_vi': {'A': 'Đọc tài liệu phát tay', 'B': 'Xem một video', 'C': 'Nghỉ giải lao', 'D': 'Lắng nghe một diễn giả khách mời'},
            'ans': 'D', 'explanation': 'Người nói giới thiệu một chuyên gia là cô Usha Madan đến để nói chuyện về kinh nghiệm của mình. Đáp án là D.'
        }
    ]
}

update_html('Test 5/LC-T5-P4-Q95-97.html', content_95_97)
update_html('Test 5/LC-T5-P4-Q98-100.html', content_98_100)

