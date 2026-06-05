import json
import os
import re
from update_t5_p3 import update_html

# Data for 38-40
content_38_40 = {
    'shadowing': [
        {'speaker': 'W-Br', 'en': "I'm looking for a gift / for my brother's birthday party / this weekend. / He loves teas, / and you have so many varieties!", 'vi': "Tôi đang tìm một món quà / cho bữa tiệc sinh nhật của anh trai tôi / vào cuối tuần này. / Anh ấy rất thích trà, / và các bạn có rất nhiều loại!"},
        {'speaker': 'M-Cn', 'en': "Well, I could recommend / a quality brand / if you know / what type he enjoys.", 'vi': "À, tôi có thể giới thiệu / một thương hiệu chất lượng / nếu bà biết / loại nào anh ấy thích."},
        {'speaker': 'W-Br', 'en': "Oh, I'm not sure. Hmm. / Maybe I should get him / a gift card / so he can choose his own.", 'vi': "Ồ, tôi không chắc lắm. Ừm. / Có lẽ tôi nên mua cho anh ấy / một chiếc thẻ quà tặng / để anh ấy có thể tự chọn."},
        {'speaker': 'M-Cn', 'en': "That's a good idea.", 'vi': "Đó là một ý tưởng hay đấy."},
        {'speaker': 'W-Br', 'en': "l'Il get one for 50 dollars. / Do your cards have / an expiration date?", 'vi': "Tôi sẽ lấy một cái trị giá 50 đô la. / Thẻ của các bạn có / ngày hết hạn không?"},
        {'speaker': 'M-Cn', 'en': "Yes. We ask / that they be used / within one year of purchase.", 'vi': "Có ạ. Chúng tôi yêu cầu / chúng phải được sử dụng / trong vòng một năm kể từ ngày mua."}
    ],
    'focus': [
        {'chunk': "brother's birthday party", 'vi': 'tiệc sinh nhật của anh trai', 'paraphrase': 'A birthday party', 'q_num': '38'},
        {'chunk': 'recommend a quality brand', 'vi': 'giới thiệu một thương hiệu chất lượng', 'paraphrase': 'Make a recommendation', 'q_num': '39'},
        {'chunk': 'gift card', 'vi': 'thẻ quà tặng'},
        {'chunk': 'choose his own', 'vi': 'tự chọn (trà) cho mình'},
        {'chunk': 'expiration date', 'vi': 'ngày hết hạn', 'paraphrase': 'An expiration date', 'q_num': '40'},
        {'chunk': 'within one year of purchase', 'vi': 'trong vòng một năm kể từ ngày mua'}
    ],
    'word_bank': ['birthday party', 'recommend', 'quality brand', 'gift card', 'expiration date', 'purchase'],
    'filling': [
        {'speaker': 'W-Br', 'text': 'I\'m looking for a gift for my brother\'s <input type="text" data-answer="birthday party" class="input-blank mx-1 w-[140px]"> this weekend. He loves teas, and you have so many varieties!'},
        {'speaker': 'M-Cn', 'text': 'Well, I could <input type="text" data-answer="recommend" class="input-blank mx-1 w-[100px]"> a <input type="text" data-answer="quality brand" class="input-blank mx-1 w-[120px]"> if you know what type he enjoys.'},
        {'speaker': 'W-Br', 'text': 'Oh, I\'m not sure. Hmm. Maybe I should get him a <input type="text" data-answer="gift card" class="input-blank mx-1 w-[100px]"> so he can choose his own.'},
        {'speaker': 'W-Br', 'text': 'l\'Il get one for 50 dollars. Do your cards have an <input type="text" data-answer="expiration date" class="input-blank mx-1 w-[140px]">?'},
        {'speaker': 'M-Cn', 'text': 'Yes. We ask that they be used within one year of <input type="text" data-answer="purchase" class="input-blank mx-1 w-[100px]">.'}
    ],
    'explanations': [
        {
            'num': '38', 'question': 'What event will the woman attend this weekend?', 'question_vi': 'Sự kiện nào người phụ nữ sẽ tham dự vào cuối tuần này?',
            'options': {'A': 'A wedding', 'B': 'A birthday party', 'C': 'A retirement dinner', 'D': 'A graduation celebration'},
            'options_vi': {'A': 'Một đám cưới', 'B': 'Một bữa tiệc sinh nhật', 'C': 'Một bữa tối nghỉ hưu', 'D': 'Một lễ kỷ niệm tốt nghiệp'},
            'ans': 'B', 'explanation': 'Người phụ nữ nói cô ấy tìm quà cho "my brother\'s birthday party this weekend" (bữa tiệc sinh nhật của anh trai tôi vào cuối tuần này). Đáp án là B.'
        },
        {
            'num': '39', 'question': 'What does the man offer to do?', 'question_vi': 'Người đàn ông đề nghị làm gì?',
            'options': {'A': 'Authorize free shipping', 'B': 'Apply a discount', 'C': 'Provide a sample', 'D': 'Make a recommendation'},
            'options_vi': {'A': 'Ủy quyền vận chuyển miễn phí', 'B': 'Áp dụng giảm giá', 'C': 'Cung cấp một mẫu thử', 'D': 'Đưa ra một lời khuyên/giới thiệu'},
            'ans': 'D', 'explanation': 'Người đàn ông nói: "I could recommend a quality brand" (tôi có thể giới thiệu một thương hiệu chất lượng). Đáp án là D.'
        },
        {
            'num': '40', 'question': 'What does the woman ask about?', 'question_vi': 'Người phụ nữ hỏi về điều gì?',
            'options': {'A': 'An expiration date', 'B': 'A manufacturer’s guarantee', 'C': 'The origin of a product', 'D': 'The cost of a product'},
            'options_vi': {'A': 'Một ngày hết hạn', 'B': 'Bảo hành của nhà sản xuất', 'C': 'Nguồn gốc của một sản phẩm', 'D': 'Giá của một sản phẩm'},
            'ans': 'A', 'explanation': 'Người phụ nữ hỏi: "Do your cards have an expiration date?" (Thẻ của các bạn có ngày hết hạn không?). Đáp án là A.'
        }
    ]
}

# Data for 41-43
content_41_43 = {
    'shadowing': [
        {'speaker': 'M-Au', 'en': "Thanks for meeting with us, Ms. Raj. / We're excited to learn / about the product / your company has developed / for factories like ours.", 'vi': "Cảm ơn bà đã gặp chúng tôi, bà Raj. / Chúng tôi rất hào hứng được tìm hiểu / về sản phẩm / mà công ty bà đã phát triển / cho các nhà máy như của chúng tôi."},
        {'speaker': 'W-Am', 'en': "I’m happy to tell you about it. / It’s an application / to monitor factory machines. / It identifies problems in operations / and generates a report / about the efficiency of each machine.", 'vi': "Tôi rất vui được kể cho ông nghe về nó. / Nó là một ứng dụng / để giám sát các máy móc trong nhà máy. / Nó xác định các vấn đề trong vận hành / và tạo ra một báo cáo / về hiệu suất của mỗi máy."},
        {'speaker': 'M-Cn', 'en': "That sounds great! / We have about 100 machine operators here. / How much training / would be involved?", 'vi': "Nghe thật tuyệt! / Chúng tôi có khoảng 100 người vận hành máy ở đây. / Sẽ cần bao nhiêu thời gian / để đào tạo?"},
        {'speaker': 'W-Am', 'en': "About an hour's worth. / We provide a video / with step-by-step instructions.", 'vi': "Khoảng một giờ đồng hồ. / Chúng tôi cung cấp một video / với các hướng dẫn từng bước."},
        {'speaker': 'M-Au', 'en': "Excellent. / That’s good to know.", 'vi': "Xuất sắc. / Thật tốt khi biết điều đó."}
    ],
    'focus': [
        {'chunk': 'product your company has developed', 'vi': 'sản phẩm mà công ty bà đã phát triển', 'paraphrase': 'To promote a product', 'q_num': '41'},
        {'chunk': 'application to monitor factory machines', 'vi': 'ứng dụng giám sát máy móc nhà máy', 'paraphrase': 'An application to monitor machines', 'q_num': '42'},
        {'chunk': 'identifies problems in operations', 'vi': 'xác định các vấn đề trong vận hành'},
        {'chunk': 'efficiency of each machine', 'vi': 'hiệu suất của mỗi máy'},
        {'chunk': 'machine operators', 'vi': 'người vận hành máy'},
        {'chunk': 'video with step-by-step instructions', 'vi': 'video với hướng dẫn từng bước', 'paraphrase': 'A training video', 'q_num': '43'}
    ],
    'word_bank': ['developed', 'monitor', 'identifies', 'efficiency', 'operators', 'step-by-step'],
    'filling': [
        {'speaker': 'M-Au', 'text': 'Thanks for meeting with us, Ms. Raj. We\'re excited to learn about the product your company has <input type="text" data-answer="developed" class="input-blank mx-1 w-[120px]"> for factories like ours.'},
        {'speaker': 'W-Am', 'text': 'I’m happy to tell you about it. It’s an application to <input type="text" data-answer="monitor" class="input-blank mx-1 w-[100px]"> factory machines. It <input type="text" data-answer="identifies" class="input-blank mx-1 w-[100px]"> problems in operations and generates a report about the <input type="text" data-answer="efficiency" class="input-blank mx-1 w-[120px]"> of each machine.'},
        {'speaker': 'M-Cn', 'text': 'That sounds great! We have about 100 machine <input type="text" data-answer="operators" class="input-blank mx-1 w-[100px]"> here. How much training would be involved?'},
        {'speaker': 'W-Am', 'text': 'About an hour\'s worth. We provide a video with <input type="text" data-answer="step-by-step" class="input-blank mx-1 w-[130px]"> instructions.'}
    ],
    'explanations': [
        {
            'num': '41', 'question': 'Why is the woman visiting?', 'question_vi': 'Tại sao người phụ nữ đến thăm?',
            'options': {'A': 'To promote a product', 'B': 'To sign a contract', 'C': 'To tour a facility', 'D': 'To inspect some equipment'},
            'options_vi': {'A': 'Để quảng bá một sản phẩm', 'B': 'Để ký hợp đồng', 'C': 'Để tham quan một cơ sở', 'D': 'Để kiểm tra một số thiết bị'},
            'ans': 'A', 'explanation': 'Người đàn ông nói họ hào hứng muốn tìm hiểu về sản phẩm mà công ty cô ấy phát triển. Điều này có nghĩa là cô ấy đến để quảng bá sản phẩm. Đáp án là A.'
        },
        {
            'num': '42', 'question': 'What did the woman’s company design?', 'question_vi': 'Công ty của người phụ nữ đã thiết kế cái gì?',
            'options': {'A': 'A digital security system', 'B': 'A device to lift heavy objects', 'C': 'An application to monitor machines', 'D': 'Protective clothing for workers'},
            'options_vi': {'A': 'Một hệ thống an ninh kỹ thuật số', 'B': 'Một thiết bị để nâng vật nặng', 'C': 'Một ứng dụng để giám sát máy móc', 'D': 'Quần áo bảo hộ cho công nhân'},
            'ans': 'C', 'explanation': 'Người phụ nữ nói: "It’s an application to monitor factory machines" (Nó là một ứng dụng để giám sát máy móc nhà máy). Đáp án là C.'
        },
        {
            'num': '43', 'question': 'What does the woman say her company can provide?', 'question_vi': 'Người phụ nữ nói công ty cô ấy có thể cung cấp điều gì?',
            'options': {'A': 'A new client discount', 'B': 'A training video', 'C': 'An extended warranty', 'D': 'Customer testimonials'},
            'options_vi': {'A': 'Giảm giá cho khách hàng mới', 'B': 'Một video đào tạo', 'C': 'Một bảo hành mở rộng', 'D': 'Lời chứng thực của khách hàng'},
            'ans': 'B', 'explanation': 'Người phụ nữ nói: "We provide a video with step-by-step instructions" (Chúng tôi cung cấp một video với các hướng dẫn từng bước). Đáp án là B.'
        }
    ]
}

# Data for 44-46
content_44_46 = {
    'shadowing': [
        {'speaker': 'W-Am', 'en': "Hi. / l'd like to go / to the Baldwin Theater. / The address is 91 Circle Drive.", 'vi': "Chào ông. / Tôi muốn đến / nhà hát Baldwin. / Địa chỉ là số 91 Circle Drive."},
        {'speaker': 'M-Cn', 'en': "Sure, / but did you know / they're resurfacing Circle Drive? / I just dropped someone off / in that area.", 'vi': "Chắc chắn rồi, / nhưng bà có biết / họ đang thảm lại mặt đường Circle Drive không? / Tôi vừa mới trả một người khách / ở khu vực đó."},
        {'speaker': 'W-Am', 'en': "Oh, really? / I've got a ticket to a play, / and the show starts at seven thirty. / They don't let you in / if you're late.", 'vi': "Ồ, thật sao? / Tôi có vé xem một vở kịch, / và buổi diễn bắt đầu lúc 7 giờ rưỡi. / Họ sẽ không cho vào / nếu bà đến muộn."},
        {'speaker': 'M-Cn', 'en': "Well, let me see. / I can turn onto Felton Street / and cut over to Lancaster Drive. / It's a little out of the way, / but it'll get you close / to the theater.", 'vi': "À, để tôi xem nào. / Tôi có thể rẽ vào phố Felton / và đi tắt qua Lancaster Drive. / Nó hơi xa hơn một chút, / nhưng nó sẽ đưa bà đến gần / nhà hát."}
    ],
    'focus': [
        {'chunk': 'Baldwin Theater', 'vi': 'Nhà hát Baldwin'},
        {'chunk': 'resurfacing Circle Drive', 'vi': 'thảm lại mặt đường Circle Drive', 'paraphrase': 'A road is closed', 'q_num': '45'},
        {'chunk': 'dropped someone off', 'vi': 'vừa trả một người khách', 'paraphrase': 'A taxi driver', 'q_num': '44'},
        {'chunk': 'show starts at seven thirty', 'vi': 'buổi diễn bắt đầu lúc 7:30'},
        {'chunk': 'turn onto Felton Street', 'vi': 'rẽ vào phố Felton'},
        {'chunk': 'cut over to Lancaster Drive', 'vi': 'đi tắt qua Lancaster Drive', 'paraphrase': 'Take a different route', 'q_num': '46'}
    ],
    'word_bank': ['Baldwin Theater', 'resurfacing', 'dropped off', 'starts at', 'turn onto', 'cut over'],
    'filling': [
        {'speaker': 'W-Am', 'text': 'Hi. l\'d like to go to the <input type="text" data-answer="Baldwin Theater" class="input-blank mx-1 w-[150px]">. The address is 91 Circle Drive.'},
        {'speaker': 'M-Cn', 'text': 'Sure, but did you know they\'re <input type="text" data-answer="resurfacing" class="input-blank mx-1 w-[120px]"> Circle Drive? I just <input type="text" data-answer="dropped off" class="input-blank mx-1 w-[120px]"> someone in that area.'},
        {'speaker': 'W-Am', 'text': 'Oh, really? I\'ve got a ticket to a play, and the show <input type="text" data-answer="starts at" class="input-blank mx-1 w-[100px]"> seven thirty. They don\'t let you in if you\'re late.'},
        {'speaker': 'M-Cn', 'text': 'Well, let me see. I can <input type="text" data-answer="turn onto" class="input-blank mx-1 w-[100px]"> Felton Street and <input type="text" data-answer="cut over" class="input-blank mx-1 w-[100px]"> to Lancaster Drive.'}
    ],
    'explanations': [
        {
            'num': '44', 'question': 'Who most likely is the man?', 'question_vi': 'Người đàn ông có khả năng nhất là ai?',
            'options': {'A': 'A theater employee', 'B': 'A taxi driver', 'C': 'A train conductor', 'D': 'A construction worker'},
            'options_vi': {'A': 'Nhân viên nhà hát', 'B': 'Tài xế taxi', 'C': 'Người soát vé tàu', 'D': 'Công nhân xây dựng'},
            'ans': 'B', 'explanation': 'Người phụ nữ đưa địa chỉ và yêu cầu đi đến nhà hát, người đàn ông nói "I just dropped someone off" (tôi vừa mới trả khách xong). Điều này chứng tỏ ông ấy là tài xế taxi. Đáp án là B.'
        },
        {
            'num': '45', 'question': 'What is causing a problem?', 'question_vi': 'Điều gì đang gây ra vấn đề?',
            'options': {'A': 'A truck is too heavy.', 'B': 'An event has been delayed.', 'C': 'A parking area is full.', 'D': 'A road is closed.'},
            'options_vi': {'A': 'Một chiếc xe tải quá nặng.', 'B': 'Một sự kiện đã bị trì hoãn.', 'C': 'Một bãi đậu xe đã đầy.', 'D': 'Một con đường bị đóng.'},
            'ans': 'D', 'explanation': 'Người đàn ông nói: "they\'re resurfacing Circle Drive" (họ đang thảm lại mặt đường Circle Drive). Việc sửa đường thường dẫn đến việc đường bị đóng hoặc hạn chế đi lại. Đáp án là D.'
        },
        {
            'num': '46', 'question': 'What does the man say he will do?', 'question_vi': 'Người đàn ông nói ông ấy sẽ làm gì?',
            'options': {'A': 'Ask for a refund', 'B': 'Take a different route', 'C': 'Postpone a trip', 'D': 'File a complaint'},
            'options_vi': {'A': 'Yêu cầu hoàn tiền', 'B': 'Đi một con đường khác', 'C': 'Hoãn một chuyến đi', 'D': 'Nộp đơn khiếu nại'},
            'ans': 'B', 'explanation': 'Người đàn ông nói ông ấy sẽ đi qua phố Felton và Lancaster Drive thay vì đường thẳng. Điều này nghĩa là đi một con đường khác. Đáp án là B.'
        }
    ]
}

update_html('Test 5/LC-T5-P3-Q38-40.html', content_38_40)
update_html('Test 5/LC-T5-P3-Q41-43.html', content_41_43)
update_html('Test 5/LC-T5-P3-Q44-46.html', content_44_46)

