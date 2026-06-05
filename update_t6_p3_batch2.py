import json
import os
import re
from update_t6_p3 import update_html

# Data for 44-46
content_44_46 = {
    'shadowing': [
        {'speaker': 'M-Au', 'en': "Asako, / how far along are you / on that news report / about the bank merger? / If you want it / to be included / in tomorrow morning’s newspaper, / it has to be on my desk / by nine p.m.", 'vi': "Asako, / cô đã thực hiện đến đâu rồi / với bản tin đó / về vụ sáp nhập ngân hàng? / Nếu cô muốn nó / được đưa vào / tờ báo sáng mai, / nó phải nằm trên bàn làm việc của tôi / trước 9 giờ tối."},
        {'speaker': 'W-Am', 'en': "Well, I'm still doing research / for this article. / I’m having trouble / getting all the facts / from the people involved. / They haven't returned / my phone calls.", 'vi': "À, tôi vẫn đang nghiên cứu / cho bài báo này. / Tôi đang gặp khó khăn / trong việc thu thập tất cả các sự kiện / từ những người có liên quan. / Họ vẫn chưa gọi lại / cho tôi."},
        {'speaker': 'M-Au', 'en': "Well, we can’t print the story / without confirming the details. / But if you can / have it finished / by Wednesday night, / I can put it / in Thursday’s paper.", 'vi': "À, chúng ta không thể in câu chuyện / mà không xác nhận các chi tiết được. / Nhưng nếu cô có thể / hoàn thành nó / vào tối thứ Tư, / tôi có thể đưa nó / vào tờ báo ngày thứ Năm."}
    ],
    'focus': [
        {'chunk': 'news report', 'vi': 'bản tin'},
        {'chunk': 'bank merger', 'vi': 'sáp nhập ngân hàng'},
        {'chunk': 'tomorrow morning’s newspaper', 'vi': 'tờ báo sáng mai', 'paraphrase': 'At a newspaper company', 'q_num': '44'},
        {'chunk': 'doing research', 'vi': 'đang nghiên cứu'},
        {'chunk': 'getting all the facts', 'vi': 'thu thập tất cả sự thật/thông tin', 'paraphrase': 'She cannot get the necessary information', 'q_num': '45'},
        {'chunk': 'confirming the details', 'vi': 'xác nhận các chi tiết'},
        {'chunk': 'finished by Wednesday night', 'vi': 'hoàn thành vào tối thứ Tư', 'paraphrase': 'Changing a deadline', 'q_num': '46'}
    ],
    'word_bank': ['report', 'merger', 'included', 'article', 'research', 'confirming'],
    'filling': [
        {'speaker': 'M-Au', 'text': 'Asako, how far along are you on that news <input type="text" data-answer="report" class="input-blank mx-1 w-[100px]"> about the bank <input type="text" data-answer="merger" class="input-blank mx-1 w-[100px]">?'},
        {'speaker': 'M-Au', 'text': 'If you want it to be <input type="text" data-answer="included" class="input-blank mx-1 w-[100px]"> in tomorrow morning’s newspaper, it has to be on my desk by nine p.m.'},
        {'speaker': 'W-Am', 'text': 'Well, I\'m still doing <input type="text" data-answer="research" class="input-blank mx-1 w-[100px]"> for this <input type="text" data-answer="article" class="input-blank mx-1 w-[100px]">. I’m having trouble getting all the facts.'},
        {'speaker': 'M-Au', 'text': 'Well, we can’t print the story without <input type="text" data-answer="confirming" class="input-blank mx-1 w-[120px]"> the details.'}
    ],
    'explanations': [
        {
            'num': '44', 'question': 'Where do the speakers most likely work?', 'question_vi': 'Những người nói có khả năng nhất làm việc ở đâu?',
            'options': {'A': 'At a bank', 'B': 'At a research laboratory', 'C': 'At a newspaper company', 'D': 'At a legal firm'},
            'options_vi': {'A': 'Tại một ngân hàng', 'B': 'Tại một phòng thí nghiệm nghiên cứu', 'C': 'Tại một công ty báo chí', 'D': 'Tại một công ty luật'},
            'ans': 'C', 'explanation': 'Người đàn ông nhắc đến việc đưa bản tin vào "tomorrow morning’s newspaper" (tờ báo sáng mai) và việc in ấn bài báo. Điều này chỉ ra họ làm việc tại một công ty báo chí. Đáp án là C.'
        },
        {
            'num': '45', 'question': 'Why has the woman been unable to finish a task?', 'question_vi': 'Tại sao người phụ nữ không thể hoàn thành một nhiệm vụ?',
            'options': {'A': 'She needs a manager’s signature.', 'B': 'She cannot access her files.', 'C': 'She cannot get the necessary information.', 'D': 'Some data are incorrect.'},
            'options_vi': {'A': 'Cô ấy cần chữ ký của quản lý.', 'B': 'Cô ấy không thể truy cập các tập tin của mình.', 'C': 'Cô ấy không thể lấy được thông tin cần thiết.', 'D': 'Một số dữ liệu không chính xác.'},
            'ans': 'C', 'explanation': 'Người phụ nữ nói cô ấy gặp khó khăn trong việc "getting all the facts from the people involved" (thu thập tất cả sự thật từ những người có liên quan) vì họ không gọi lại cho cô ấy. Đáp án là C.'
        },
        {
            'num': '46', 'question': 'What solution does the man propose?', 'question_vi': 'Giải pháp nào người đàn ông đề xuất?',
            'options': {'A': 'Changing a deadline', 'B': 'Scheduling a meeting', 'C': 'Asking a colleague for help', 'D': 'Reviewing some documents'},
            'options_vi': {'A': 'Thay đổi thời hạn', 'B': 'Lên lịch một cuộc họp', 'C': 'Nhờ một đồng nghiệp giúp đỡ', 'D': 'Xem xét một số tài liệu'},
            'ans': 'A', 'explanation': 'Người đàn ông đề xuất rằng nếu cô ấy hoàn thành vào tối thứ Tư thay vì tối nay, ông ấy sẽ đưa nó vào báo ngày thứ Năm. Đây là việc thay đổi thời hạn (deadline). Đáp án là A.'
        }
    ]
}

# Data for 47-49
content_47_49 = {
    'shadowing': [
        {'speaker': 'M-Cn', 'en': "We'll have to remove / the soil / from the garden bed / and lay down drainpipes / that'll take the water out / through holes / in the retaining wall.", 'vi': "Chúng ta sẽ phải loại bỏ / lớp đất / khỏi luống vườn / và đặt các ống thoát nước / để dẫn nước ra ngoài / qua các lỗ / ở bức tường chắn."},
        {'speaker': 'W-Am', 'en': "Sounds like a lot of work, / but it'll be worth it / to be able to grow / the garden that I want to.", 'vi': "Nghe có vẻ là rất nhiều việc, / nhưng nó sẽ xứng đáng / để có thể trồng / khu vườn mà tôi mong muốn."},
        {'speaker': 'M-Cn', 'en': "Do you think you’d like / bricks or stones / for the retaining wall? / Many homeowners prefer brick / because it creates a nice, uniform look. / But stones will last longer. / They are more expensive, though.", 'vi': "Bà nghĩ mình sẽ thích / gạch hay đá / cho bức tường chắn? / Nhiều chủ nhà thích gạch hơn / vì nó tạo ra một vẻ ngoài đẹp, đồng nhất. / Nhưng đá sẽ bền hơn. / Tuy nhiên, chúng đắt hơn."},
        {'speaker': 'W-Am', 'en': "I don’t want to have / to make repairs.", 'vi': "Tôi không muốn phải / sửa chữa nhiều."},
        {'speaker': 'M-Cn', 'en': "You have several / different kinds of stones / to choose from. / I have some pictures / of projects / I’ve completed in the past / you can look at.", 'vi': "Bà có vài / loại đá khác nhau / để lựa chọn. / Tôi có một số bức ảnh / về các dự án / tôi đã hoàn thành trong quá khứ / mà bà có thể xem."}
    ],
    'focus': [
        {'chunk': 'soil from the garden bed', 'vi': 'đất từ luống vườn', 'paraphrase': 'Landscaping', 'q_num': '47'},
        {'chunk': 'lay down drainpipes', 'vi': 'đặt ống thoát nước'},
        {'chunk': 'retaining wall', 'vi': 'tường chắn'},
        {'chunk': 'stones will last longer', 'vi': 'đá sẽ bền hơn', 'paraphrase': 'She prefers durable materials', 'q_num': '48'},
        {'chunk': 'make repairs', 'vi': 'sửa chữa'},
        {'chunk': 'pictures of projects', 'vi': 'ảnh của các dự án', 'paraphrase': 'Some photographs', 'q_num': '49'}
    ],
    'word_bank': ['remove', 'drainpipes', 'retaining', 'uniform', 'expensive', 'completed'],
    'filling': [
        {'speaker': 'M-Cn', 'text': 'We\'ll have to <input type="text" data-answer="remove" class="input-blank mx-1 w-[100px]"> the soil from the garden bed and lay down <input type="text" data-answer="drainpipes" class="input-blank mx-1 w-[120px]"> that\'ll take the water out through holes in the <input type="text" data-answer="retaining" class="input-blank mx-1 w-[100px]"> wall.'},
        {'speaker': 'M-Cn', 'text': 'Many homeowners prefer brick because it creates a nice, <input type="text" data-answer="uniform" class="input-blank mx-1 w-[100px]"> look. But stones will last longer. They are more <input type="text" data-answer="expensive" class="input-blank mx-1 w-[120px]">, though.'},
        {'speaker': 'M-Cn', 'text': 'I have some pictures of projects I’ve <input type="text" data-answer="completed" class="input-blank mx-1 w-[120px]"> in the past you can look at.'}
    ],
    'explanations': [
        {
            'num': '47', 'question': 'What kind of work does the man do?', 'question_vi': 'Người đàn ông làm loại công việc gì?',
            'options': {'A': 'Appliance repair', 'B': 'Painting', 'C': 'Landscaping', 'D': 'Roofing'},
            'options_vi': {'A': 'Sửa chữa thiết bị', 'B': 'Sơn', 'C': 'Làm cảnh quan', 'D': 'Làm mái nhà'},
            'ans': 'C', 'explanation': 'Người đàn ông nói về việc xử lý đất vườn ("soil from the garden bed"), lắp ống thoát nước và xây tường chắn vườn. Đây là những công việc thuộc về làm cảnh quan (landscaping). Đáp án là C.'
        },
        {
            'num': '48', 'question': 'What does the woman imply when she says, “I don’t want to have to make repairs”?', 'question_vi': 'Người phụ nữ ngụ ý điều gì khi nói: "Tôi không muốn phải sửa chữa"?',
            'options': {'A': 'She is not qualified for a task.', 'B': 'She prefers durable materials.', 'C': 'She will buy a new appliance.', 'D': 'She is not happy with a cost estimate.'},
            'options_vi': {'A': 'Cô ấy không đủ trình độ cho một nhiệm vụ.', 'B': 'Cô ấy thích các vật liệu bền.', 'C': 'Cô ấy sẽ mua một thiết bị mới.', 'D': 'Cô ấy không hài lòng với ước tính chi phí.'},
            'ans': 'B', 'explanation': 'Khi người đàn ông nói đá bền hơn nhưng đắt hơn gạch, người phụ nữ nói cô ấy không muốn phải sửa chữa. Điều này ngụ ý cô ấy sẵn sàng chi nhiều hơn để có vật liệu bền (đá). Đáp án là B.'
        },
        {
            'num': '49', 'question': 'What will the man show to the woman?', 'question_vi': 'Người đàn ông sẽ cho người phụ nữ xem cái gì?',
            'options': {'A': 'A list of prices', 'B': 'A license', 'C': 'Some references', 'D': 'Some photographs'},
            'options_vi': {'A': 'Một danh sách giá', 'B': 'Một giấy phép', 'C': 'Một số tài liệu tham khảo', 'D': 'Một số bức ảnh'},
            'ans': 'D', 'explanation': 'Người đàn ông nói: "I have some pictures of projects I’ve completed in the past you can look at" (Tôi có một số bức ảnh về các dự án tôi đã hoàn thành trong quá khứ mà bà có thể xem). Đáp án là D.'
        }
    ]
}

# Data for 50-52
content_50_52 = {
    'shadowing': [
        {'speaker': 'W-Br', 'en': "Good morning. / You've reached / Accounts Payable.", 'vi': "Chào buổi sáng. / Bạn đã gọi đến / Bộ phận Kế toán Phải trả."},
        {'speaker': 'M-Cn', 'en': "Hi. I'm calling / from the editorial department. / One of our freelance writers / has not received payment yet, / so I'm calling / to inquire about it. / Her contract number / is 9356.", 'vi': "Chào cô. Tôi gọi / từ bộ phận biên tập. / Một trong những nhà văn tự do của chúng tôi / vẫn chưa nhận được khoản thanh toán, / vì vậy tôi gọi điện / để hỏi về việc đó. / Số hợp đồng của cô ấy / là 9356."},
        {'speaker': 'W-Br', 'en': "OK, let me check. Hmm. / It looks like / she should have been paid / last week. / But Adem handles / those requests, / and he was on vacation. / He’s just catching up / today.", 'vi': "Được rồi, để tôi kiểm tra. Hừm. / Có vẻ như / lẽ ra cô ấy đã được thanh toán / vào tuần trước rồi. / Nhưng Adem là người xử lý / các yêu cầu đó, / và anh ấy đã đi nghỉ. / Anh ấy vừa mới bắt đầu làm bù / ngày hôm nay."},
        {'speaker': 'M-Cn', 'en': "Do you have an estimate / of how long it will take / to process the request?", 'vi': "Cô có ước tính / mất bao lâu / để xử lý yêu cầu này không?"},
        {'speaker': 'W-Br', 'en': "I’m not sure, / but I can speak / to Adem.", 'vi': "Tôi không chắc lắm, / nhưng tôi có thể nói chuyện / với Adem."}
    ],
    'focus': [
        {'chunk': 'Accounts Payable', 'vi': 'Bộ phận Kế toán Phải trả'},
        {'chunk': 'editorial department', 'vi': 'bộ phận biên tập'},
        {'chunk': 'received payment', 'vi': 'nhận được thanh toán', 'paraphrase': 'To ask about a payment', 'q_num': '50'},
        {'chunk': 'contract number', 'vi': 'số hợp đồng'},
        {'chunk': 'on vacation', 'vi': 'đi nghỉ/nghỉ phép', 'paraphrase': 'An employee was out of the office', 'q_num': '51'},
        {'chunk': 'estimate of how long it will take', 'vi': 'ước tính mất bao lâu', 'paraphrase': 'A time estimate', 'q_num': '52'}
    ],
    'word_bank': ['reached', 'payable', 'editorial', 'freelance', 'vacation', 'estimate'],
    'filling': [
        {'speaker': 'W-Br', 'text': 'Good morning. You\'ve <input type="text" data-answer="reached" class="input-blank mx-1 w-[100px]"> Accounts <input type="text" data-answer="payable" class="input-blank mx-1 w-[100px]">.'},
        {'speaker': 'M-Cn', 'text': 'Hi. I\'m calling from the <input type="text" data-answer="editorial" class="input-blank mx-1 w-[100px]"> department. One of our <input type="text" data-answer="freelance" class="input-blank mx-1 w-[100px]"> writers has not received payment yet.'},
        {'speaker': 'W-Br', 'text': 'But Adem handles those requests, and he was on <input type="text" data-answer="vacation" class="input-blank mx-1 w-[100px]">. He’s just catching up today.'},
        {'speaker': 'M-Cn', 'text': 'Do you have an <input type="text" data-answer="estimate" class="input-blank mx-1 w-[100px]"> of how long it will take to process the request?'}
    ],
    'explanations': [
        {
            'num': '50', 'question': 'Why is the man calling?', 'question_vi': 'Tại sao người đàn ông lại gọi điện?',
            'options': {'A': 'To track a shipment', 'B': 'To ask about a payment', 'C': 'To close an account', 'D': 'To request computer help'},
            'options_vi': {'A': 'Để theo dõi một lô hàng', 'B': 'Để hỏi về một khoản thanh toán', 'C': 'Để đóng một tài khoản', 'D': 'Để yêu cầu giúp đỡ về máy tính'},
            'ans': 'B', 'explanation': 'Người đàn ông nói: "One of our freelance writers has not received payment yet, so I\'m calling to inquire about it" (Một trong những nhà văn tự do của chúng tôi chưa nhận được tiền thanh toán, nên tôi gọi để hỏi về việc đó). Đáp án là B.'
        },
        {
            'num': '51', 'question': 'According to the woman, what caused a delay?', 'question_vi': 'Theo người phụ nữ, điều gì đã gây ra sự chậm trễ?',
            'options': {'A': 'An employee was out of the office.', 'B': 'A software program was updated.', 'C': 'A document was mislabeled.', 'D': 'A new policy was implemented.'},
            'options_vi': {'A': 'Một nhân viên không có mặt ở văn phòng.', 'B': 'Một chương trình phần mềm đã được cập nhật.', 'C': 'Một tài liệu bị dán nhãn sai.', 'D': 'Một chính sách mới đã được thực hiện.'},
            'ans': 'A', 'explanation': 'Người phụ nữ giải thích: "Adem handles those requests, and he was on vacation" (Adem xử lý những yêu cầu đó, và anh ấy đã đi nghỉ). Nghỉ phép nghĩa là không có mặt ở văn phòng. Đáp án là A.'
        },
        {
            'num': '52', 'question': 'What information will the woman most likely provide later?', 'question_vi': 'Thông tin nào người phụ nữ có khả năng nhất sẽ cung cấp sau đó?',
            'options': {'A': 'A cost breakdown', 'B': 'An account number', 'C': 'A time estimate', 'D': 'A phone number'},
            'options_vi': {'A': 'Bản chi tiết chi phí', 'B': 'Một số tài khoản', 'C': 'Một ước tính thời gian', 'D': 'Một số điện thoại'},
            'ans': 'C', 'explanation': 'Người đàn ông hỏi về ước tính thời gian xử lý ("estimate of how long it will take"). Người phụ nữ nói cô ấy không chắc nhưng sẽ hỏi Adem, ngụ ý cô ấy sẽ báo lại cho anh ta sau. Đáp án là C.'
        }
    ]
}

# Data for 53-55
content_53_55 = {
    'shadowing': [
        {'speaker': 'M-Au', 'en': "I’m the general manager / here at Rev It Auto Repair, / and this is Mr. Singh, / our service manager. / We're eager to hear / how your product / can benefit our shop.", 'vi': "Tôi là tổng quản lý / tại đây tại Rev It Auto Repair, / và đây là ông Singh, / quản lý dịch vụ của chúng tôi. / Chúng tôi rất háo hức được nghe / về việc sản phẩm của bà / có thể mang lại lợi ích gì cho cửa hàng chúng tôi."},
        {'speaker': 'W-Am', 'en': "Well, my product / is called Video Room. / It’s a library / of short videos / that your business can offer / in the waiting room. / These videos / will explain / common auto repairs / and educate your customers / on the repair process.", 'vi': "Vâng, sản phẩm của tôi / được gọi là Video Room. / Nó là một thư viện / gồm các video ngắn / mà doanh nghiệp của ông có thể cung cấp / trong phòng chờ. / Những video này / sẽ giải thích / các lỗi sửa chữa ô tô thông thường / và hướng dẫn khách hàng của ông / về quy trình sửa chữa."},
        {'speaker': 'M-Cn', 'en': "Can we add / our own customized content? / I’d love to include / a description / of our exclusive lifetime warranty.", 'vi': "Chúng tôi có thể thêm / nội dung tùy chỉnh của riêng mình không? / Tôi rất muốn đưa vào / một bản mô tả / về chính sách bảo hành trọn đời độc quyền của chúng tôi."},
        {'speaker': 'M-Au', 'en': "Yes. And can we also add / at-home auto-care advice?", 'vi': "Vâng. Và chúng ta cũng có thể thêm / lời khuyên tự chăm sóc xe tại nhà chứ?"}
    ],
    'focus': [
        {'chunk': 'Rev It Auto Repair', 'vi': 'Tên tiệm sửa xe', 'paraphrase': 'At an auto repair shop', 'q_num': '53'},
        {'chunk': 'service manager', 'vi': 'quản lý dịch vụ'},
        {'chunk': 'library of short videos', 'vi': 'thư viện các video ngắn', 'paraphrase': 'Some videos', 'q_num': '54'},
        {'chunk': 'common auto repairs', 'vi': 'các lỗi sửa xe thông thường'},
        {'chunk': 'educate your customers', 'vi': 'hướng dẫn/giáo dục khách hàng'},
        {'chunk': 'add our own customized content', 'vi': 'thêm nội dung tùy chỉnh riêng', 'paraphrase': 'Include customized content', 'q_num': '55'}
    ],
    'word_bank': ['manager', 'benefit', 'library', 'waiting room', 'educate', 'customized'],
    'filling': [
        {'speaker': 'M-Au', 'text': 'I’m the general <input type="text" data-answer="manager" class="input-blank mx-1 w-[100px]"> here at Rev It Auto Repair... We\'re eager to hear how your product can <input type="text" data-answer="benefit" class="input-blank mx-1 w-[100px]"> our shop.'},
        {'speaker': 'W-Am', 'text': 'It’s a <input type="text" data-answer="library" class="input-blank mx-1 w-[100px]"> of short videos that your business can offer in the <input type="text" data-answer="waiting room" class="input-blank mx-1 w-[120px]">.'},
        {'speaker': 'W-Am', 'text': 'These videos will explain common auto repairs and <input type="text" data-answer="educate" class="input-blank mx-1 w-[100px]"> your customers on the repair process.'},
        {'speaker': 'M-Cn', 'text': 'Can we add our own <input type="text" data-answer="customized" class="input-blank mx-1 w-[120px]"> content?'}
    ],
    'explanations': [
        {
            'num': '53', 'question': 'Where does the conversation take place?', 'question_vi': 'Cuộc trò chuyện diễn ra ở đâu?',
            'options': {'A': 'At a game arcade', 'B': 'At a grocery store', 'C': 'At an auto repair shop', 'D': 'At a parking garage'},
            'options_vi': {'A': 'Tại một khu trò chơi', 'B': 'Tại một cửa hàng tạp hóa', 'C': 'Tại một tiệm sửa xe ô tô', 'D': 'Tại một bãi đậu xe'},
            'ans': 'C', 'explanation': 'Người nói cho biết ông là quản lý tại "Rev It Auto Repair". Điều này chỉ ra họ đang ở một tiệm sửa xe ô tô. Đáp án là C.'
        },
        {
            'num': '54', 'question': 'What type of product does the woman mention?', 'question_vi': 'Người phụ nữ nhắc đến loại sản phẩm nào?',
            'options': {'A': 'Some videos', 'B': 'Some brochures', 'C': 'A price scanner', 'D': 'A mobile phone application'},
            'options_vi': {'A': 'Một số video', 'B': 'Một số tài liệu quảng cáo', 'C': 'Một máy quét giá', 'D': 'Một ứng dụng điện thoại di động'},
            'ans': 'A', 'explanation': 'Người phụ nữ mô tả sản phẩm của mình là "Video Room", một "library of short videos" (thư viện các video ngắn). Đáp án là A.'
        },
        {
            'num': '55', 'question': 'What do the men want to do?', 'question_vi': 'Những người đàn ông muốn làm gì?',
            'options': {'A': 'Extend business hours', 'B': 'Enter a local contest', 'C': 'Include customized content', 'D': 'Upgrade some equipment'},
            'options_vi': {'A': 'Kéo dài giờ kinh doanh', 'B': 'Tham gia một cuộc thi địa phương', 'C': 'Bao gồm nội dung tùy chỉnh', 'D': 'Nâng cấp một số thiết bị'},
            'ans': 'C', 'explanation': 'Người đàn ông Singh hỏi: "Can we add our own customized content?" (Chúng tôi có thể thêm nội dung tùy chỉnh của riêng mình không?). Đáp án là C.'
        }
    ]
}

update_html('Test 6/LC-T6-P3-Q44-46.html', content_44_46)
update_html('Test 6/LC-T6-P3-Q47-49.html', content_47_49)
update_html('Test 6/LC-T6-P3-Q50-52.html', content_50_52)
update_html('Test 6/LC-T6-P3-Q53-55.html', content_53_55)

