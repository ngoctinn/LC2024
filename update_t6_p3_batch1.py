import json
import os
import re
from update_t6_p3 import update_html

# Data for 32-34
content_32_34 = {
    'shadowing': [
        {'speaker': 'M-Cn', 'en': "The renovations / we’re planning / for the theater / are long overdue.", 'vi': "Những việc tu sửa / mà chúng ta đang lên kế hoạch / cho nhà hát / đã quá hạn từ lâu rồi."},
        {'speaker': 'W-Br', 'en': "I'm glad / we have time / between productions / so we can get / the work done.", 'vi': "Tôi rất vui / vì chúng ta có thời gian / giữa các buổi công diễn / để chúng ta có thể / hoàn thành công việc."},
        {'speaker': 'M-Cn', 'en': "I agree—and even though / it’s great / that our latest musical production / has had such a successful run, / we can all use the break.", 'vi': "Tôi đồng ý—và mặc dù / thật tuyệt / khi vở nhạc kịch mới nhất của chúng ta / đã có một đợt diễn thành công như vậy, / tất cả chúng ta đều có thể tận dụng thời gian nghỉ ngơi này."},
        {'speaker': 'W-Br', 'en': "Plus, / it gives us time / to focus / on next month’s fund-raiser.", 'vi': "Thêm vào đó, / nó cho chúng ta thời gian / để tập trung / vào buổi gây quỹ tháng tới."},
        {'speaker': 'M-Cn', 'en': "Hopefully / we'll raise enough money / at that event / to replace the old lighting system / too.", 'vi': "Hy vọng rằng / chúng ta sẽ gây quỹ đủ tiền / tại sự kiện đó / để thay thế cả hệ thống chiếu sáng cũ / nữa."}
    ],
    'focus': [
        {'chunk': 'renovations for the theater', 'vi': 'tu sửa cho nhà hát', 'paraphrase': 'Theater renovations', 'q_num': '32'},
        {'chunk': 'between productions', 'vi': 'giữa các buổi công diễn'},
        {'chunk': 'successful run', 'vi': 'đợt diễn thành công', 'paraphrase': 'It has been successful', 'q_num': '33'},
        {'chunk': 'fund-raiser', 'vi': 'buổi gây quỹ', 'paraphrase': 'A fund-raiser', 'q_num': '34'},
        {'chunk': 'replace the old lighting system', 'vi': 'thay thế hệ thống chiếu sáng cũ'}
    ],
    'word_bank': ['renovations', 'overdue', 'productions', 'successful', 'fund-raiser', 'lighting'],
    'filling': [
        {'speaker': 'M-Cn', 'text': 'The <input type="text" data-answer="renovations" class="input-blank mx-1 w-[120px]"> we’re planning for the theater are long <input type="text" data-answer="overdue" class="input-blank mx-1 w-[100px]">.'},
        {'speaker': 'W-Br', 'text': 'I\'m glad we have time between <input type="text" data-answer="productions" class="input-blank mx-1 w-[120px]"> so we can get the work done.'},
        {'speaker': 'M-Cn', 'text': 'Even though it’s great that our latest musical production has had such a <input type="text" data-answer="successful" class="input-blank mx-1 w-[120px]"> run, we can all use the break.'},
        {'speaker': 'W-Br', 'text': 'Plus, it gives us time to focus on next month’s <input type="text" data-answer="fund-raiser" class="input-blank mx-1 w-[120px]">.'},
        {'speaker': 'M-Cn', 'text': 'Hopefully we\'ll raise enough money at that event to replace the old <input type="text" data-answer="lighting" class="input-blank mx-1 w-[100px]"> system too.'}
    ],
    'explanations': [
        {
            'num': '32', 'question': 'What are the speakers mainly discussing?', 'question_vi': 'Những người nói chủ yếu thảo luận về vấn đề gì?',
            'options': {'A': 'Theater renovations', 'B': 'Changes to a performance schedule', 'C': 'Selection of a new lighting director', 'D': 'A promotional gift'},
            'options_vi': {'A': 'Tu sửa nhà hát', 'B': 'Thay đổi lịch biểu diễn', 'C': 'Lựa chọn giám đốc ánh sáng mới', 'D': 'Một món quà khuyến mại'},
            'ans': 'A', 'explanation': 'Người đàn ông bắt đầu bằng: "The renovations we’re planning for the theater are long overdue" (Những việc tu sửa mà chúng ta đang lên kế hoạch cho nhà hát đã quá hạn từ lâu rồi). Đáp án là A.'
        },
        {
            'num': '33', 'question': 'What does the man say about a musical production?', 'question_vi': 'Người đàn ông nói gì về một vở nhạc kịch?',
            'options': {'A': 'It was based on a book.', 'B': 'It has been successful.', 'C': 'It will be performed overseas.', 'D': 'Some casting changes were made.'},
            'options_vi': {'A': 'Nó dựa trên một cuốn sách.', 'B': 'Nó đã thành công.', 'C': 'Nó sẽ được biểu diễn ở nước ngoài.', 'D': 'Một số thay đổi về diễn viên đã được thực hiện.'},
            'ans': 'B', 'explanation': 'Người đàn ông nói: "our latest musical production has had such a successful run" (vở nhạc kịch mới nhất của chúng ta đã có một đợt diễn thành công như vậy). Đáp án là B.'
        },
        {
            'num': '34', 'question': 'What event are the speakers planning?', 'question_vi': 'Sự kiện nào mà những người nói đang lên kế hoạch?',
            'options': {'A': 'A press conference', 'B': 'A fund-raiser', 'C': 'An audition', 'D': 'An autograph session'},
            'options_vi': {'A': 'Một cuộc họp báo', 'B': 'Một buổi gây quỹ', 'C': 'Một buổi thử giọng', 'D': 'Một buổi ký tặng'},
            'ans': 'B', 'explanation': 'Người phụ nữ nhắc đến việc tập trung vào "next month’s fund-raiser" (buổi gây quỹ tháng tới). Đáp án là B.'
        }
    ]
}

# Data for 35-37
content_35_37 = {
    'shadowing': [
        {'speaker': 'M-Au', 'en': "Fernanda, / I wanted to tell you / that the top candidate we chose / for the customer-care position / just accepted our job offer. / I'll send him a contract / later today.", 'vi': "Fernanda, / tôi muốn nói với cô rằng / ứng viên hàng đầu mà chúng ta đã chọn / cho vị trí chăm sóc khách hàng / vừa mới chấp nhận lời mời làm việc của chúng ta. / Tôi sẽ gửi hợp đồng cho anh ấy / vào cuối ngày hôm nay."},
        {'speaker': 'W-Am', 'en': "Great! / But now I think / we need a bigger office space / for our business. / With the new hire, / there'll be ten of us / in the office.", 'vi': "Tuyệt quá! / Nhưng bây giờ tôi nghĩ / chúng ta cần một không gian văn phòng lớn hơn / cho doanh nghiệp của mình. / Với người mới được thuê, / sẽ có mười người chúng ta / trong văn phòng."},
        {'speaker': 'M-Au', 'en': "I agree. / Our lease expires next month, / so we should look / at a different space. / There’s a new office building / on Second Street. / It has solar panels, / so all of its energy / comes from renewable sources.", 'vi': "Tôi đồng ý. / Hợp đồng thuê của chúng ta sẽ hết hạn vào tháng tới, / vì vậy chúng ta nên tìm / một không gian khác. / Có một tòa nhà văn phòng mới / trên Phố Second. / Nó có các tấm pin năng lượng mặt trời, / vì vậy tất cả năng lượng của nó / đều đến từ các nguồn tái tạo."},
        {'speaker': 'W-Am', 'en': "I like that. / But I’m worried / we may not be able / to afford the lease.", 'vi': "Tôi thích điều đó. / Nhưng tôi lo lắng / chúng ta có thể không đủ khả năng / chi trả tiền thuê."},
        {'speaker': 'M-Au', 'en': "We'll see. / I'll contact the rental agency / today.", 'vi': "Để xem đã. / Tôi sẽ liên lạc với đại lý cho thuê / hôm nay."}
    ],
    'focus': [
        {'chunk': 'chose for the customer-care position', 'vi': 'đã chọn cho vị trí chăm sóc khách hàng', 'paraphrase': 'They chose a job candidate', 'q_num': '35'},
        {'chunk': 'bigger office space', 'vi': 'không gian văn phòng lớn hơn'},
        {'chunk': 'lease expires next month', 'vi': 'hợp đồng thuê hết hạn tháng tới'},
        {'chunk': 'energy comes from renewable sources', 'vi': 'năng lượng từ các nguồn tái tạo', 'paraphrase': 'It uses renewable energy', 'q_num': '36'},
        {'chunk': 'solar panels', 'vi': 'các tấm pin năng lượng mặt trời'},
        {'chunk': 'afford the lease', 'vi': 'đủ khả năng chi trả tiền thuê', 'paraphrase': 'A high price', 'q_num': '37'}
    ],
    'word_bank': ['candidate', 'accepted', 'contract', 'expires', 'renewable', 'afford'],
    'filling': [
        {'speaker': 'M-Au', 'text': 'Fernanda, I wanted to tell you that the top <input type="text" data-answer="candidate" class="input-blank mx-1 w-[100px]"> we chose for the customer-care position just <input type="text" data-answer="accepted" class="input-blank mx-1 w-[100px]"> our job offer. I\'ll send him a <input type="text" data-answer="contract" class="input-blank mx-1 w-[100px]"> later today.'},
        {'speaker': 'M-Au', 'text': 'Our lease <input type="text" data-answer="expires" class="input-blank mx-1 w-[100px]"> next month, so we should look at a different space.'},
        {'speaker': 'M-Au', 'text': 'It has solar panels, so all of its energy comes from <input type="text" data-answer="renewable" class="input-blank mx-1 w-[100px]"> sources.'},
        {'speaker': 'W-Am', 'text': 'I like that. But I’m worried we may not be able to <input type="text" data-answer="afford" class="input-blank mx-1 w-[100px]"> the lease.'}
    ],
    'explanations': [
        {
            'num': '35', 'question': 'What did the speakers recently do?', 'question_vi': 'Những người nói vừa làm gì gần đây?',
            'options': {'A': 'They launched a new product.', 'B': 'They chose a job candidate.', 'C': 'They moved to a different city.', 'D': 'They renovated a space.'},
            'options_vi': {'A': 'Họ đã ra mắt một sản phẩm mới.', 'B': 'Họ đã chọn một ứng viên xin việc.', 'C': 'Họ đã chuyển đến một thành phố khác.', 'D': 'Họ đã tu sửa một không gian.'},
            'ans': 'B', 'explanation': 'Người đàn ông nói: "the top candidate we chose for the customer-care position just accepted our job offer" (ứng viên hàng đầu mà chúng ta đã chọn cho vị trí chăm sóc khách hàng vừa mới chấp nhận lời mời làm việc). Điều này nghĩa là họ vừa chọn một ứng viên. Đáp án là B.'
        },
        {
            'num': '36', 'question': 'What do the speakers like about a building?', 'question_vi': 'Những người nói thích điều gì về một tòa nhà?',
            'options': {'A': 'It provides 24-hour access.', 'B': 'It has an outdoor space.', 'C': 'It is near public transportation.', 'D': 'It uses renewable energy.'},
            'options_vi': {'A': 'Nó cung cấp quyền truy cập 24 giờ.', 'B': 'Nó có không gian ngoài trời.', 'C': 'Nó gần phương tiện giao thông công cộng.', 'D': 'Nó sử dụng năng lượng tái tạo.'},
            'ans': 'D', 'explanation': 'Người đàn ông mô tả tòa nhà: "It has solar panels, so all of its energy comes from renewable sources" (Nó có các tấm pin năng lượng mặt trời, vì vậy tất cả năng lượng của nó đều đến từ các nguồn tái tạo). Đáp án là D.'
        },
        {
            'num': '37', 'question': 'What is the woman worried about?', 'question_vi': 'Người phụ nữ lo lắng về điều gì?',
            'options': {'A': 'A new competitor', 'B': 'A longer commute', 'C': 'A high price', 'D': 'An upcoming deadline'},
            'options_vi': {'A': 'Một đối thủ cạnh tranh mới', 'B': 'Quãng đường đi làm dài hơn', 'C': 'Một mức giá cao', 'D': 'Một thời hạn sắp tới'},
            'ans': 'C', 'explanation': 'Người phụ nữ nói: "I’m worried we may not be able to afford the lease" (Tôi lo lắng chúng ta có thể không đủ khả năng chi trả tiền thuê). Khả năng chi trả liên quan đến giá cả. Đáp án là C.'
        }
    ]
}

# Data for 38-40
content_38_40 = {
    'shadowing': [
        {'speaker': 'M-Au', 'en': "How can I help you?", 'vi': "Tôi có thể giúp gì cho bà ạ?"},
        {'speaker': 'W-Br', 'en': "Hi, I'd like to order a cake / for my son's birthday / next week. / He really likes dinosaurs.", 'vi': "Chào ông, tôi muốn đặt một chiếc bánh / cho sinh nhật con trai tôi / vào tuần tới. / Cháu thực sự thích khủng long."},
        {'speaker': 'M-Au', 'en': "I have several / different dinosaur-shaped pans / for you to choose from.", 'vi': "Tôi có vài / khuôn hình khủng long khác nhau / để bà lựa chọn."},
        {'speaker': 'W-Br', 'en': "Actually, I was hoping / you could make a standing cake / instead of a flat one.", 'vi': "Thực ra, tôi hy vọng / ông có thể làm một chiếc bánh đứng / thay vì một chiếc bánh phẳng."},
        {'speaker': 'M-Au', 'en': "Oh, I see. I'm sorry. / I do have someone on staff / who can make those, / but she's all booked up / for the next few weeks. / Try Carmen's Creations / on Pine Street.", 'vi': "Ồ, tôi hiểu rồi. Tôi xin lỗi. / Tôi đúng là có một nhân viên / có thể làm loại đó, / nhưng cô ấy đã kín lịch / trong vài tuần tới rồi. / Bà hãy thử Carmen's Creations / trên phố Pine xem sao."}
    ],
    'focus': [
        {'chunk': 'order a cake for my son\'s birthday', 'vi': 'đặt bánh cho sinh nhật con trai', 'paraphrase': 'A birthday party', 'q_num': '38'},
        {'chunk': 'dinosaur-shaped pans', 'vi': 'khuôn hình khủng long', 'paraphrase': 'A baker', 'q_num': '39'},
        {'chunk': 'standing cake instead of a flat one', 'vi': 'bánh đứng thay vì bánh phẳng'},
        {'chunk': 'all booked up', 'vi': 'đã kín lịch', 'paraphrase': 'A request cannot be fulfilled', 'q_num': '40'},
        {'chunk': 'Try Carmen\'s Creations', 'vi': 'Thử (đến cửa hàng) Carmen\'s Creations'}
    ],
    'word_bank': ['order', 'birthday', 'dinosaurs', 'standing', 'booked up', 'fulfilled'],
    'filling': [
        {'speaker': 'W-Br', 'text': 'Hi, I\'d like to <input type="text" data-answer="order" class="input-blank mx-1 w-[100px]"> a cake for my son\'s <input type="text" data-answer="birthday" class="input-blank mx-1 w-[100px]"> next week. He really likes <input type="text" data-answer="dinosaurs" class="input-blank mx-1 w-[100px]">.'},
        {'speaker': 'W-Br', 'text': 'Actually, I was hoping you could make a <input type="text" data-answer="standing" class="input-blank mx-1 w-[100px]"> cake instead of a flat one.'},
        {'speaker': 'M-Au', 'text': 'Oh, I see. I\'m sorry. I do have someone on staff who can make those, but she\'s all <input type="text" data-answer="booked up" class="input-blank mx-1 w-[120px]"> for the next few weeks.'}
    ],
    'explanations': [
        {
            'num': '38', 'question': 'What event is the woman planning?', 'question_vi': 'Sự kiện nào người phụ nữ đang lên kế hoạch?',
            'options': {'A': 'A retirement party', 'B': 'A birthday party', 'C': 'A science fair', 'D': 'A school festival'},
            'options_vi': {'A': 'Một bữa tiệc nghỉ hưu', 'B': 'Một bữa tiệc sinh nhật', 'C': 'Một hội chợ khoa học', 'D': 'Một lễ hội trường học'},
            'ans': 'B', 'explanation': 'Người phụ nữ nói cô ấy muốn đặt bánh cho "my son\'s birthday next week" (sinh nhật con trai tôi vào tuần tới). Đáp án là B.'
        },
        {
            'num': '39', 'question': 'Who most likely is the man?', 'question_vi': 'Người đàn ông có khả năng nhất là ai?',
            'options': {'A': 'A baker', 'B': 'A musician', 'C': 'A gardener', 'D': 'A teacher'},
            'options_vi': {'A': 'Thợ làm bánh', 'B': 'Nhạc sĩ', 'C': 'Làm vườn', 'D': 'Giáo viên'},
            'ans': 'A', 'explanation': 'Người đàn ông đang thảo luận về việc đặt bánh và các loại khuôn bánh ("dinosaur-shaped pans"). Điều này chỉ ra ông ấy là thợ làm bánh. Đáp án là A.'
        },
        {
            'num': '40', 'question': 'Why does the man apologize?', 'question_vi': 'Tại sao người đàn ông lại xin lỗi?',
            'options': {'A': 'Some tools cannot be found.', 'B': 'Some invitations were sent late.', 'C': 'A store is closed for a holiday.', 'D': 'A request cannot be fulfilled.'},
            'options_vi': {'A': 'Một số công cụ không thể tìm thấy.', 'B': 'Một số thiệp mời đã được gửi muộn.', 'C': 'Cửa hàng đóng cửa nghỉ lễ.', 'D': 'Yêu cầu không thể được thực hiện.'},
            'ans': 'D', 'explanation': 'Người đàn ông xin lỗi vì ông ấy không thể làm chiếc bánh đứng theo yêu cầu của người phụ nữ do nhân viên phụ trách đã kín lịch ("she\'s all booked up"). Đáp án là D.'
        }
    ]
}

# Data for 41-43
content_41_43 = {
    'shadowing': [
        {'speaker': 'W-Am', 'en': "Hello, / you've reached / Quick Phone Repair Service.", 'vi': "Xin chào, / bạn đã gọi đến / Dịch vụ Sửa chữa Điện thoại Nhanh."},
        {'speaker': 'M-Cn', 'en': "Hi, I went online / to schedule a repair / for my mobile phone, / but all appointments / in your store / were booked for today. / Have you had any cancellations?", 'vi': "Chào cô, tôi đã lên mạng / để lên lịch sửa chữa / cho điện thoại di động của mình, / nhưng tất cả các cuộc hẹn / tại cửa hàng của cô / đều đã được đặt hết cho ngày hôm nay. / Các cô có trường hợp hủy hẹn nào không?"},
        {'speaker': 'W-Am', 'en': "No, unfortunately not. / What's the problem / with your phone?", 'vi': "Không, thật không may là không có ạ. / Có vấn đề gì / với điện thoại của ông vậy?"},
        {'speaker': 'M-Cn', 'en': "The phone only lasts / about an hour / before it has to be recharged.", 'vi': "Điện thoại chỉ dùng được / khoảng một giờ / trước khi nó phải được sạc lại."},
        {'speaker': 'W-Am', 'en': "It sounds like / you need a new battery. / If you come to the store now, / we can try to fit you in / as a walk-in appointment. / You may have to wait around / for a bit.", 'vi': "Nghe có vẻ như / ông cần một viên pin mới. / Nếu ông đến cửa hàng ngay bây giờ, / chúng tôi có thể cố gắng sắp xếp cho ông / theo diện khách không hẹn trước. / Ông có thể sẽ phải chờ / một chút ạ."},
        {'speaker': 'M-Cn', 'en': "I don’t mind waiting.", 'vi': "Tôi không phiền việc phải chờ đâu."}
    ],
    'focus': [
        {'chunk': 'schedule a repair', 'vi': 'lên lịch sửa chữa', 'paraphrase': 'Make an appointment', 'q_num': '41'},
        {'chunk': 'appointments in your store', 'vi': 'các cuộc hẹn tại cửa hàng'},
        {'chunk': 'cancellations', 'vi': 'việc hủy hẹn'},
        {'chunk': 'last about an hour before it has to be recharged', 'vi': 'dùng được khoảng 1 giờ trước khi phải sạc lại', 'paraphrase': 'It has a short battery life', 'q_num': '42'},
        {'chunk': 'new battery', 'vi': 'pin mới'},
        {'chunk': 'walk-in appointment', 'vi': 'cuộc hẹn không đặt trước/khách vãng lai', 'paraphrase': 'Visit a store', 'q_num': '43'}
    ],
    'word_bank': ['reached', 'schedule', 'cancellations', 'recharged', 'battery', 'walk-in'],
    'filling': [
        {'speaker': 'W-Am', 'text': 'Hello, you\'ve <input type="text" data-answer="reached" class="input-blank mx-1 w-[100px]"> Quick Phone Repair Service.'},
        {'speaker': 'M-Cn', 'text': 'Hi, I went online to <input type="text" data-answer="schedule" class="input-blank mx-1 w-[100px]"> a repair for my mobile phone... Have you had any <input type="text" data-answer="cancellations" class="input-blank mx-1 w-[130px]">?'},
        {'speaker': 'M-Cn', 'text': 'The phone only lasts about an hour before it has to be <input type="text" data-answer="recharged" class="input-blank mx-1 w-[120px]">.'},
        {'speaker': 'W-Am', 'text': 'It sounds like you need a new <input type="text" data-answer="battery" class="input-blank mx-1 w-[100px]">. If you come to the store now, we can try to fit you in as a <input type="text" data-answer="walk-in" class="input-blank mx-1 w-[100px]"> appointment.'}
    ],
    'explanations': [
        {
            'num': '41', 'question': 'What did the man try to do online?', 'question_vi': 'Người đàn ông đã cố gắng làm gì trực tuyến?',
            'options': {'A': 'Purchase a new phone', 'B': 'Make an appointment', 'C': 'Order a part', 'D': 'Cancel a contract'},
            'options_vi': {'A': 'Mua một chiếc điện thoại mới', 'B': 'Đặt một cuộc hẹn', 'C': 'Đặt một bộ phận', 'D': 'Hủy bỏ một hợp đồng'},
            'ans': 'B', 'explanation': 'Người đàn ông nói: "I went online to schedule a repair" (tôi đã lên mạng để lên lịch sửa chữa). Việc lên lịch sửa chữa tương ứng với việc đặt một cuộc hẹn. Đáp án là B.'
        },
        {
            'num': '42', 'question': 'What does the man say is wrong with his mobile phone?', 'question_vi': 'Người đàn ông nói có vấn đề gì với điện thoại di động của mình?',
            'options': {'A': 'It has a short battery life.', 'B': 'The screen is damaged.', 'C': 'A cable is missing.', 'D': 'It has limited storage space.'},
            'options_vi': {'A': 'Nó có thời lượng pin ngắn.', 'B': 'Màn hình bị hư hại.', 'C': 'Một sợi cáp bị thiếu.', 'D': 'Nó có không gian lưu trữ hạn chế.'},
            'ans': 'A', 'explanation': 'Người đàn ông nói: "The phone only lasts about an hour before it has to be recharged" (Điện thoại chỉ dùng được khoảng 1 giờ trước khi phải sạc lại). Điều này có nghĩa là pin rất nhanh hết. Đáp án là A.'
        },
        {
            'num': '43', 'question': 'What will the man most likely do next?', 'question_vi': 'Người đàn ông có khả năng nhất sẽ làm gì tiếp theo?',
            'options': {'A': 'Speak with a manager', 'B': 'Call technical support', 'C': 'Visit a store', 'D': 'Restart a device'},
            'options_vi': {'A': 'Nói chuyện với một quản lý', 'B': 'Gọi hỗ trợ kỹ thuật', 'C': 'Đến một cửa hàng', 'D': 'Khởi động lại một thiết bị'},
            'ans': 'C', 'explanation': 'Người phụ nữ gợi ý: "If you come to the store now, we can try to fit you in" (Nếu ông đến cửa hàng ngay bây giờ, chúng tôi có thể cố gắng sắp xếp cho ông). Người đàn ông trả lời ông không phiền việc phải chờ, ngụ ý ông sẽ đến đó. Đáp án là C.'
        }
    ]
}

update_html('Test 6/LC-T6-P3-Q32-34.html', content_32_34)
update_html('Test 6/LC-T6-P3-Q35-37.html', content_35_37)
update_html('Test 6/LC-T6-P3-Q38-40.html', content_38_40)
update_html('Test 6/LC-T6-P3-Q41-43.html', content_41_43)

