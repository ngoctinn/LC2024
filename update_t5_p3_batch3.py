import json
import os
import re
from update_t5_p3 import update_html

# Data for 47-49
content_47_49 = {
    'shadowing': [
        {'speaker': 'W-Br', 'en': "Do you have a minute / to discuss the budget / for the upcoming Vancouver meeting? / I’ve looked over the travel requests / you submitted for your team. / Last year we sent / only two representatives.", 'vi': "Ông có chút thời gian nào / để thảo luận về ngân sách / cho cuộc họp Vancouver sắp tới không? / Tôi đã xem qua các yêu cầu đi lại / mà ông đã nộp cho nhóm của mình. / Năm ngoái chúng ta chỉ gửi / hai người đại diện thôi."},
        {'speaker': 'M-Au', 'en': "Ms. Tamura has just given us / approval to send three. / In fact, the clients are looking / to expand their online service options, / and the third representative / we’re bringing / is particularly knowledgeable about that.", 'vi': "Bà Tamura vừa mới / chấp thuận cho chúng tôi gửi ba người. / Thực tế là, khách hàng đang muốn / mở rộng các tùy chọn dịch vụ trực tuyến của họ, / và người đại diện thứ ba / mà chúng tôi đưa đi / đặc biệt am hiểu về lĩnh vực đó."},
        {'speaker': 'W-Br', 'en': "OK. I guess we'll have to / find savings somewhere else, then.", 'vi': "Được rồi. Tôi đoán là sau đó chúng ta sẽ phải / tìm cách tiết kiệm ở một nơi khác thôi."},
        {'speaker': 'M-Au', 'en': "l’ve already looked into / some new meeting venues. / The Renova Hotel is offering / discounted corporate rates / this month.", 'vi': "Tôi đã tìm hiểu / một số địa điểm họp mới rồi. / Khách sạn Renova đang cung cấp / mức giá ưu đãi cho doanh nghiệp / trong tháng này."}
    ],
    'focus': [
        {'chunk': 'upcoming Vancouver meeting', 'vi': 'cuộc họp Vancouver sắp tới'},
        {'chunk': 'travel requests', 'vi': 'yêu cầu đi lại'},
        {'chunk': 'only two representatives', 'vi': 'chỉ hai người đại diện', 'paraphrase': 'To question a decision', 'q_num': '47'},
        {'chunk': 'expand their online service options', 'vi': 'mở rộng tùy chọn dịch vụ trực tuyến', 'paraphrase': 'Increase their online offerings', 'q_num': '48'},
        {'chunk': 'particularly knowledgeable', 'vi': 'đặc biệt am hiểu'},
        {'chunk': 'discounted corporate rates', 'vi': 'mức giá ưu đãi cho doanh nghiệp', 'paraphrase': 'A discount for businesses', 'q_num': '49'}
    ],
    'word_bank': ['upcoming', 'requests', 'representatives', 'expand', 'knowledgeable', 'discounted'],
    'filling': [
        {'speaker': 'W-Br', 'text': 'Do you have a minute to discuss the budget for the <input type="text" data-answer="upcoming" class="input-blank mx-1 w-[100px]"> Vancouver meeting? I’ve looked over the travel <input type="text" data-answer="requests" class="input-blank mx-1 w-[100px]"> you submitted for your team.'},
        {'speaker': 'W-Br', 'text': 'Last year we sent only two <input type="text" data-answer="representatives" class="input-blank mx-1 w-[140px]">.'},
        {'speaker': 'M-Au', 'text': 'Ms. Tamura has just given us approval to send three. In fact, the clients are looking to <input type="text" data-answer="expand" class="input-blank mx-1 w-[100px]"> their online service options, and the third representative we’re bringing is particularly <input type="text" data-answer="knowledgeable" class="input-blank mx-1 w-[140px]"> about that.'},
        {'speaker': 'M-Au', 'text': 'l’ve already looked into some new meeting venues. The Renova Hotel is offering <input type="text" data-answer="discounted" class="input-blank mx-1 w-[120px]"> corporate rates this month.'}
    ],
    'explanations': [
        {
            'num': '47', 'question': 'Why does the woman say, “Last year we sent only two representatives”?', 'question_vi': 'Tại sao người phụ nữ nói: "Năm ngoái chúng ta chỉ gửi hai người đại diện"?',
            'options': {'A': 'To explain a delay', 'B': 'To compliment a team', 'C': 'To point out that an event was unsuccessful', 'D': 'To question a decision'},
            'options_vi': {'A': 'Để giải thích một sự chậm trễ', 'B': 'Để khen ngợi một nhóm', 'C': 'Để chỉ ra rằng một sự kiện đã không thành công', 'D': 'Để đặt câu hỏi về một quyết định'},
            'ans': 'D', 'explanation': 'Người phụ nữ nhắc lại con số năm ngoái (2 người) khi người đàn ông muốn gửi 3 người năm nay. Điều này cho thấy cô ấy đang nghi ngờ hoặc muốn thảo luận lại quyết định gửi thêm người. Đáp án là D.'
        },
        {
            'num': '48', 'question': 'According to the man, what do some clients want to do?', 'question_vi': 'Theo người đàn ông, một số khách hàng muốn làm gì?',
            'options': {'A': 'Increase their online offerings', 'B': 'Obtain additional financing', 'C': 'Open a new office', 'D': 'Recruit more employees'},
            'options_vi': {'A': 'Tăng cường các sản phẩm trực tuyến của họ', 'B': 'Nhận thêm tài trợ', 'C': 'Mở một văn phòng mới', 'D': 'Tuyển thêm nhân viên'},
            'ans': 'A', 'explanation': 'Người đàn ông nói: "the clients are looking to expand their online service options" (khách hàng đang tìm cách mở rộng các tùy chọn dịch vụ trực tuyến của họ). Đáp án là A.'
        },
        {
            'num': '49', 'question': 'According to the man, what is the Renova Hotel offering this month?', 'question_vi': 'Theo người đàn ông, khách sạn Renova đang cung cấp điều gì trong tháng này?',
            'options': {'A': 'A new shuttle service', 'B': 'A discount for businesses', 'C': 'A flexible cancellation policy', 'D': 'Complimentary meals'},
            'options_vi': {'A': 'Một dịch vụ đưa đón mới', 'B': 'Một khoản chiết khấu cho các doanh nghiệp', 'C': 'Một chính sách hủy bỏ linh hoạt', 'D': 'Các bữa ăn miễn phí'},
            'ans': 'B', 'explanation': 'Người đàn ông nói: "The Renova Hotel is offering discounted corporate rates this month" (Khách sạn Renova đang cung cấp mức giá ưu đãi cho doanh nghiệp trong tháng này). Đáp án là B.'
        }
    ]
}

# Data for 50-52
content_50_52 = {
    'shadowing': [
        {'speaker': 'W-Am', 'en': "Good morning. / l wanted to meet today / to discuss the recent decline / in our museum's ticket sales. / You're the outreach coordinator, / so I’m hoping you might have / some ideas on how we can attract / more community involvement.", 'vi': "Chào buổi sáng. / Tôi muốn gặp ông hôm nay / để thảo luận về sự sụt giảm gần đây / trong việc bán vé của bảo tàng chúng ta. / Ông là điều phối viên cộng đồng, / vì vậy tôi hy vọng ông có thể có / một số ý tưởng về cách chúng ta có thể thu hút / nhiều sự tham gia của cộng đồng hơn."},
        {'speaker': 'M-Cn', 'en': "Well, l recently read an article / about a museum in Chicago / that has a room / where visitors can paint on the walls. / It’s become very popular. / We could try it here— / we have that huge room on the third floor / that isn’t being used.", 'vi': "À, gần đây tôi có đọc một bài báo / về một bảo tàng ở Chicago / có một căn phòng / nơi khách tham quan có thể vẽ lên tường. / Nó đã trở nên rất phổ biến. / Chúng ta có thể thử ở đây— / chúng ta có căn phòng khổng lồ đó ở tầng ba / hiện đang không được sử dụng."},
        {'speaker': 'W-Am', 'en': "That's a great idea. / Can you draft a list / of the supplies we would need / to make sure we have the budget for them?", 'vi': "Đó là một ý tưởng tuyệt vời. / Ông có thể phác thảo một danh sách / các vật dụng chúng ta sẽ cần / để đảm bảo chúng ta có ngân sách cho chúng không?"}
    ],
    'focus': [
        {'chunk': 'recent decline in ticket sales', 'vi': 'sự sụt giảm bán vé gần đây', 'paraphrase': 'A decrease in ticket sales', 'q_num': '50'},
        {'chunk': 'outreach coordinator', 'vi': 'điều phối viên cộng đồng'},
        {'chunk': 'attract more community involvement', 'vi': 'thu hút nhiều sự tham gia của cộng đồng hơn'},
        {'chunk': 'visitors can paint on the walls', 'vi': 'khách tham quan có thể vẽ lên tường', 'paraphrase': 'Introducing a new activity', 'q_num': '51'},
        {'chunk': 'room on the third floor', 'vi': 'phòng ở tầng ba'},
        {'chunk': 'draft a list of the supplies', 'vi': 'phác thảo danh sách các vật dụng', 'paraphrase': 'Make a list of supplies', 'q_num': '52'}
    ],
    'word_bank': ['decline', 'outreach', 'involvement', 'popular', 'supplies', 'budget'],
    'filling': [
        {'speaker': 'W-Am', 'text': 'Good morning. l wanted to meet today to discuss the recent <input type="text" data-answer="decline" class="input-blank mx-1 w-[100px]"> in our museum\'s ticket sales. You\'re the <input type="text" data-answer="outreach" class="input-blank mx-1 w-[100px]"> coordinator, so I’m hoping you might have some ideas on how we can attract more community <input type="text" data-answer="involvement" class="input-blank mx-1 w-[120px]">.'},
        {'speaker': 'M-Cn', 'text': 'Well, l recently read an article about a museum in Chicago that has a room where visitors can paint on the walls. It’s become very <input type="text" data-answer="popular" class="input-blank mx-1 w-[100px]">.'},
        {'speaker': 'W-Am', 'text': 'That\'s a great idea. Can you draft a list of the <input type="text" data-answer="supplies" class="input-blank mx-1 w-[100px]"> we would need to make sure we have the <input type="text" data-answer="budget" class="input-blank mx-1 w-[100px]"> for them?'}
    ],
    'explanations': [
        {
            'num': '50', 'question': 'What problem does the woman mention?', 'question_vi': 'Người phụ nữ đề cập đến vấn đề gì?',
            'options': {'A': 'A decrease in ticket sales', 'B': 'A lack of exhibition space', 'C': 'A colleague’s resignation', 'D': 'A damaged painting'},
            'options_vi': {'A': 'Sự sụt giảm doanh số bán vé', 'B': 'Sự thiếu hụt không gian triển lãm', 'C': 'Sự từ chức của một đồng nghiệp', 'D': 'Một bức tranh bị hư hại'},
            'ans': 'A', 'explanation': 'Người phụ nữ nói: "discuss the recent decline in our museum\'s ticket sales" (thảo luận về sự sụt giảm doanh số bán vé bảo tàng gần đây của chúng ta). Đáp án là A.'
        },
        {
            'num': '51', 'question': 'What does the man suggest doing?', 'question_vi': 'Người đàn ông gợi ý làm gì?',
            'options': {'A': 'Relocating an exhibit', 'B': 'Consulting a specialist', 'C': 'Adding security measures', 'D': 'Introducing a new activity'},
            'options_vi': {'A': 'Di dời một cuộc triển lãm', 'B': 'Tham khảo ý kiến chuyên gia', 'C': 'Thêm các biện pháp an ninh', 'D': 'Giới thiệu một hoạt động mới'},
            'ans': 'D', 'explanation': 'Người đàn ông gợi ý tạo ra một căn phòng nơi khách tham quan có thể vẽ lên tường. Đây là một hoạt động mới cho bảo tàng. Đáp án là D.'
        },
        {
            'num': '52', 'question': 'What will the man most likely do next?', 'question_vi': 'Người đàn ông có khả năng nhất sẽ làm gì tiếp theo?',
            'options': {'A': 'Write a press release', 'B': 'Attend a budget meeting', 'C': 'Make a list of supplies', 'D': 'Plan a site visit'},
            'options_vi': {'A': 'Viết một thông cáo báo chí', 'B': 'Tham dự một cuộc họp ngân sách', 'C': 'Lập danh sách các vật dụng', 'D': 'Lên kế hoạch tham quan hiện trường'},
            'ans': 'C', 'explanation': 'Người phụ nữ yêu cầu: "Can you draft a list of the supplies we would need...?" (Ông có thể phác thảo danh sách các vật dụng chúng ta sẽ cần... không?). Đáp án là C.'
        }
    ]
}

# Data for 53-55
content_53_55 = {
    'shadowing': [
        {'speaker': 'W-Br', 'en': "Thilo, this is Ms. Gao, / a new customer. / She’s purchasing / an upholstered sofa. / We just walked around our showroom, / and she’s decided / on our Hudson model.", 'vi': "Thilo, đây là bà Gao, / một khách hàng mới. / Bà ấy đang mua / một chiếc ghế sofa bọc nệm. / Chúng tôi vừa đi dạo quanh phòng trưng bày, / và bà ấy đã quyết định chọn / mẫu Hudson của chúng ta."},
        {'speaker': 'M-Cn', 'en': "One of our best sellers!", 'vi': "Một trong những mẫu bán chạy nhất của chúng tôi đấy!"},
        {'speaker': 'W-Am', 'en': "It is really comfortable.", 'vi': "Nó thực sự rất thoải mái."},
        {'speaker': 'W-Br', 'en': "Can you assist her / with the paperwork / for our payment plan?", 'vi': "Ông có thể hỗ trợ bà ấy / các thủ tục giấy tờ / cho kế hoạch thanh toán của chúng ta không?"},
        {'speaker': 'M-Cn', 'en': "Sure. Happy to help you, Ms. Gao. / Are you getting the standard fabric?", 'vi': "Chắc chắn rồi. Rất vui được giúp bà, bà Gao. / Bà sẽ lấy loại vải tiêu chuẩn chứ?"},
        {'speaker': 'W-Am', 'en': "No—I’d like to select / a custom fabric.", 'vi': "Không—tôi muốn chọn / một loại vải tùy chỉnh."},
        {'speaker': 'M-Cn', 'en': "Just so you know, / the price will increase / some with a custom order.", 'vi': "Chỉ để bà biết, / giá sẽ tăng lên một chút / với đơn hàng tùy chỉnh."},
        {'speaker': 'W-Am', 'en': "I think it’s worth the extra cost. / It’ll really brighten up / my living room.", 'vi': "Tôi nghĩ nó đáng với chi phí bỏ thêm. / Nó sẽ thực sự làm sáng bừng / phòng khách của tôi."},
        {'speaker': 'M-Cn', 'en': "Wonderful. / Now in order to set up / a payment plan, / I'll need to see / some identification. / A driver's license will do.", 'vi': "Tuyệt vời. / Bây giờ để thiết lập / một kế hoạch thanh toán, / tôi sẽ cần xem / một số giấy tờ tùy thân. / Bằng lái xe là được rồi ạ."}
    ],
    'focus': [
        {'chunk': 'upholstered sofa', 'vi': 'sofa bọc nệm'},
        {'chunk': 'showroom', 'vi': 'phòng trưng bày', 'paraphrase': 'At a furniture store', 'q_num': '53'},
        {'chunk': 'payment plan', 'vi': 'kế hoạch thanh toán'},
        {'chunk': 'custom fabric', 'vi': 'vải tùy chỉnh', 'paraphrase': 'It is a custom order', 'q_num': '54'},
        {'chunk': 'worth the extra cost', 'vi': 'đáng với chi phí bỏ thêm'},
        {'chunk': 'some identification', 'vi': 'giấy tờ tùy thân', 'paraphrase': 'A form of identification', 'q_num': '55'}
    ],
    'word_bank': ['purchasing', 'upholstered', 'showroom', 'paperwork', 'identification', 'fabric'],
    'filling': [
        {'speaker': 'W-Br', 'text': 'Thilo, this is Ms. Gao, a new customer. She’s <input type="text" data-answer="purchasing" class="input-blank mx-1 w-[100px]"> an <input type="text" data-answer="upholstered" class="input-blank mx-1 w-[120px]"> sofa. We just walked around our <input type="text" data-answer="showroom" class="input-blank mx-1 w-[100px]">, and she’s decided on our Hudson model.'},
        {'speaker': 'W-Br', 'text': 'Can you assist her with the <input type="text" data-answer="paperwork" class="input-blank mx-1 w-[100px]"> for our payment plan?'},
        {'speaker': 'W-Am', 'text': 'No—I’d like to select a custom <input type="text" data-answer="fabric" class="input-blank mx-1 w-[100px]">.'},
        {'speaker': 'M-Cn', 'text': 'Wonderful. Now in order to set up a payment plan, I\'ll need to see some <input type="text" data-answer="identification" class="input-blank mx-1 w-[140px]">.'}
    ],
    'explanations': [
        {
            'num': '53', 'question': 'Where most likely are the speakers?', 'question_vi': 'Những người nói có khả năng nhất đang ở đâu?',
            'options': {'A': 'At a clothing factory', 'B': 'At a bookstore', 'C': 'At a tailor’s shop', 'D': 'At a furniture store'},
            'options_vi': {'A': 'Tại một nhà máy may mặc', 'B': 'Tại một hiệu sách', 'C': 'Tại một cửa hàng may đo', 'D': 'Tại một cửa hàng nội thất'},
            'ans': 'D', 'explanation': 'Họ đang nói về việc mua "upholstered sofa" (sofa bọc nệm) và đang ở trong "showroom" (phòng trưng bày). Điều này chỉ ra họ đang ở cửa hàng nội thất. Đáp án là D.'
        },
        {
            'num': '54', 'question': 'According to the man, why will a product cost more?', 'question_vi': 'Theo người đàn ông, tại sao một sản phẩm sẽ có giá cao hơn?',
            'options': {'A': 'It includes an extended warranty.', 'B': 'It is a custom order.', 'C': 'A rebate has expired.', 'D': 'Shipping will be expedited.'},
            'options_vi': {'A': 'Nó bao gồm bảo hành mở rộng.', 'B': 'Đó là một đơn đặt hàng tùy chỉnh.', 'C': 'Một khoản giảm giá đã hết hạn.', 'D': 'Vận chuyển sẽ được đẩy nhanh.'},
            'ans': 'B', 'explanation': 'Người đàn ông nói: "the price will increase some with a custom order" (giá sẽ tăng lên một chút với đơn hàng tùy chỉnh). Đáp án là B.'
        },
        {
            'num': '55', 'question': 'What does the man request?', 'question_vi': 'Người đàn ông yêu cầu điều gì?',
            'options': {'A': 'A purchase receipt', 'B': 'A delivery address', 'C': 'A form of identification', 'D': 'An account number'},
            'options_vi': {'A': 'Một biên lai mua hàng', 'B': 'Một địa chỉ giao hàng', 'C': 'Một hình thức nhận dạng/giấy tờ tùy thân', 'D': 'Một số tài khoản'},
            'ans': 'C', 'explanation': 'Người đàn ông nói: "I\'ll need to see some identification" (tôi sẽ cần xem một số giấy tờ tùy thân). Đáp án là C.'
        }
    ]
}

# Data for 56-58
content_56_58 = {
    'shadowing': [
        {'speaker': 'W-Am', 'en': "Good morning, Mr. Tong. / I’m here to check on my order. / How are the chairs / coming along?", 'vi': "Chào buổi sáng, ông Tong. / Tôi ở đây để kiểm tra đơn hàng của mình. / Những chiếc ghế / tiến triển đến đâu rồi?"},
        {'speaker': 'M-Cn', 'en': "The machines / have been assembling them. / They’re almost ready. / Right over here.", 'vi': "Máy móc / đã và đang lắp ráp chúng. / Chúng gần như đã xong rồi. / Ngay đằng này ạ."},
        {'speaker': 'W-Am', 'en': "Wow, they look so nice!", 'vi': "Oa, chúng trông thật đẹp!"},
        {'speaker': 'M-Cn', 'en': "Look at the curved shape / of the back. / The only way / you can get that unique shape / is by means of the specialized laser / we use.", 'vi': "Hãy nhìn vào hình dạng cong / của phần lưng ghế. / Cách duy nhất / bà có được hình dạng độc đáo đó / là nhờ vào tia laser chuyên dụng / mà chúng tôi sử dụng."},
        {'speaker': 'W-Am', 'en': "Amazing! / Can I also see / the pullout sofa?", 'vi': "Thật tuyệt vời! / Tôi có thể xem / chiếc sofa giường không?"},
        {'speaker': 'M-Cn', 'en': "Not right now. / It’s being treated / with mineral oil. / But later today / I should be able / to take a photo / and send it to you.", 'vi': "Hiện tại thì chưa được ạ. / Nó đang được xử lý / bằng dầu khoáng. / Nhưng vào cuối ngày hôm nay / tôi có thể / chụp một bức ảnh / và gửi nó cho bà."}
    ],
    'focus': [
        {'chunk': 'check on my order', 'vi': 'kiểm tra đơn hàng'},
        {'chunk': 'machines have been assembling them', 'vi': 'máy móc đang lắp ráp chúng', 'paraphrase': 'At a factory', 'q_num': '56'},
        {'chunk': 'curved shape of the back', 'vi': 'hình dạng cong của phần lưng', 'paraphrase': 'The shape', 'q_num': '57'},
        {'chunk': 'specialized laser', 'vi': 'tia laser chuyên dụng'},
        {'chunk': 'pullout sofa', 'vi': 'sofa giường (sofa kéo ra thành giường)'},
        {'chunk': 'take a photo and send it', 'vi': 'chụp ảnh và gửi nó', 'paraphrase': 'Send a photo', 'q_num': '58'}
    ],
    'word_bank': ['order', 'assembling', 'curved shape', 'specialized', 'pullout', 'mineral oil'],
    'filling': [
        {'speaker': 'W-Am', 'text': 'Good morning, Mr. Tong. I’m here to check on my <input type="text" data-answer="order" class="input-blank mx-1 w-[100px]">. How are the chairs coming along?'},
        {'speaker': 'M-Cn', 'text': 'The machines have been <input type="text" data-answer="assembling" class="input-blank mx-1 w-[100px]"> them. They’re almost ready. Right over here.'},
        {'speaker': 'M-Cn', 'text': 'Look at the <input type="text" data-answer="curved shape" class="input-blank mx-1 w-[120px]"> of the back. The only way you can get that unique shape is by means of the <input type="text" data-answer="specialized" class="input-blank mx-1 w-[120px]"> laser we use.'},
        {'speaker': 'W-Am', 'text': 'Amazing! Can I also see the <input type="text" data-answer="pullout" class="input-blank mx-1 w-[100px]"> sofa?'},
        {'speaker': 'M-Cn', 'text': 'Not right now. It’s being treated with <input type="text" data-answer="mineral oil" class="input-blank mx-1 w-[120px]">.'}
    ],
    'explanations': [
        {
            'num': '56', 'question': 'Where most likely are the speakers?', 'question_vi': 'Những người nói có khả năng nhất đang ở đâu?',
            'options': {'A': 'At a hotel', 'B': 'At a factory', 'C': 'At a retail store', 'D': 'At a trade show'},
            'options_vi': {'A': 'Tại một khách sạn', 'B': 'Tại một nhà máy', 'C': 'Tại một cửa hàng bán lẻ', 'D': 'Tại một cuộc triển lãm thương mại'},
            'ans': 'B', 'explanation': 'Người đàn ông nói: "The machines have been assembling them" (Máy móc đang lắp ráp chúng). Việc lắp ráp bằng máy móc quy mô lớn thường diễn ra tại nhà máy. Đáp án là B.'
        },
        {
            'num': '57', 'question': 'What feature does the man emphasize about some chairs?', 'question_vi': 'Đặc điểm nào người đàn ông nhấn mạnh về một số chiếc ghế?',
            'options': {'A': 'The color', 'B': 'The price', 'C': 'The shape', 'D': 'The durability'},
            'options_vi': {'A': 'Màu sắc', 'B': 'Giá cả', 'C': 'Hình dáng', 'D': 'Độ bền'},
            'ans': 'C', 'explanation': 'Người đàn ông nhấn mạnh vào "curved shape of the back" (hình dạng cong của lưng ghế) và nói đó là "unique shape" (hình dạng độc đáo). Đáp án là C.'
        },
        {
            'num': '58', 'question': 'What does the man say he will do later?', 'question_vi': 'Người đàn ông nói ông ấy sẽ làm gì sau đó?',
            'options': {'A': 'Modify a design', 'B': 'E-mail a contract', 'C': 'Create an invoice', 'D': 'Send a photo'},
            'options_vi': {'A': 'Sửa đổi một thiết kế', 'B': 'Gửi e-mail hợp đồng', 'C': 'Tạo một hóa đơn', 'D': 'Gửi một bức ảnh'},
            'ans': 'D', 'explanation': 'Người đàn ông nói: "later today I should be able to take a photo and send it to you" (vào cuối ngày hôm nay tôi có thể chụp một bức ảnh và gửi nó cho bà). Đáp án là D.'
        }
    ]
}

update_html('Test 5/LC-T5-P3-Q47-49.html', content_47_49)
update_html('Test 5/LC-T5-P3-Q50-52.html', content_50_52)
update_html('Test 5/LC-T5-P3-Q53-55.html', content_53_55)
update_html('Test 5/LC-T5-P3-Q56-58.html', content_56_58)

