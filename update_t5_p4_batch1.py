import json
import os
import re
from update_t5_p4 import update_html

# Data for 71-73
content_71_73 = {
    'shadowing': [
        {'speaker': 'M-Au', 'en': "Hi, Ms. Cho. / I’m calling from Springdale Lights. / Yesterday, you ordered / 24 of our purple solar lanterns / for your upcoming event.", 'vi': "Chào bà Cho. / Tôi gọi từ Springdale Lights. / Hôm qua, bà đã đặt / 24 chiếc đèn lồng năng lượng mặt trời màu tím / cho sự kiện sắp tới của mình."},
        {'speaker': 'M-Au', 'en': "Unfortunately, our supplier / won't be able to get us / purple lanterns / for another three weeks, / so we only have yellow ones / in stock.", 'vi': "Thật không may, nhà cung cấp của chúng tôi / sẽ không thể giao / đèn lồng màu tím / trong ba tuần tới, / vì vậy chúng tôi chỉ còn loại màu vàng / trong kho."},
        {'speaker': 'M-Au', 'en': "We would like to offer you / a ten percent discount on them / to apologize for this. / Please call us back / to confirm / whether you'd like the yellow solar lights, / and we'll set them aside for you.", 'vi': "Chúng tôi muốn đề nghị giảm giá / mười phần trăm cho chúng / để xin lỗi về việc này. / Vui lòng gọi lại cho chúng tôi / để xác nhận / liệu bà có muốn lấy đèn năng lượng mặt trời màu vàng không, / và chúng tôi sẽ để riêng chúng cho bà."}
    ],
    'focus': [
        {'chunk': 'ordered 24 purple solar lanterns', 'vi': 'đã đặt 24 đèn lồng năng lượng mặt trời tím', 'paraphrase': 'She placed an order', 'q_num': '71'},
        {'chunk': 'upcoming event', 'vi': 'sự kiện sắp tới'},
        {'chunk': 'supplier won\'t be able to get us', 'vi': 'nhà cung cấp không thể giao cho chúng tôi', 'paraphrase': 'A product is not available', 'q_num': '72'},
        {'chunk': 'yellow ones in stock', 'vi': 'màu vàng có sẵn trong kho'},
        {'chunk': 'ten percent discount', 'vi': 'giảm giá 10%', 'paraphrase': 'A discount', 'q_num': '73'},
        {'chunk': 'set them aside', 'vi': 'để riêng chúng ra/giữ hàng'}
    ],
    'word_bank': ['ordered', 'lanterns', 'upcoming', 'supplier', 'discount', 'confirm'],
    'filling': [
        {'speaker': 'M-Au', 'text': 'Hi, Ms. Cho. I’m calling from Springdale Lights. Yesterday, you <input type="text" data-answer="ordered" class="input-blank mx-1 w-[100px]"> 24 of our purple solar <input type="text" data-answer="lanterns" class="input-blank mx-1 w-[100px]"> for your <input type="text" data-answer="upcoming" class="input-blank mx-1 w-[120px]"> event.'},
        {'speaker': 'M-Au', 'text': 'Unfortunately, our <input type="text" data-answer="supplier" class="input-blank mx-1 w-[100px]"> won\'t be able to get us purple lanterns for another three weeks, so we only have yellow ones in stock.'},
        {'speaker': 'M-Au', 'text': 'We would like to offer you a ten percent <input type="text" data-answer="discount" class="input-blank mx-1 w-[100px]"> on them to apologize for this. Please call us back to <input type="text" data-answer="confirm" class="input-blank mx-1 w-[100px]"> whether you\'d like the yellow solar lights.'}
    ],
    'explanations': [
        {
            'num': '71', 'question': 'What did the listener do yesterday?', 'question_vi': 'Người nghe đã làm gì vào hôm qua?',
            'options': {'A': 'She placed an order.', 'B': 'She scheduled an event.', 'C': 'She called a manager.', 'D': 'She painted some rooms.'},
            'options_vi': {'A': 'Bà ấy đã đặt hàng.', 'B': 'Bà ấy đã lên lịch một sự kiện.', 'C': 'Bà ấy đã gọi cho một người quản lý.', 'D': 'Bà ấy đã sơn một số phòng.'},
            'ans': 'A', 'explanation': 'Người nói bắt đầu bằng: "Yesterday, you ordered 24 of our purple solar lanterns" (Hôm qua, bà đã đặt 24 chiếc đèn lồng năng lượng mặt trời màu tím của chúng tôi). Đáp án là A.'
        },
        {
            'num': '72', 'question': 'What problem does the speaker mention?', 'question_vi': 'Người nói đề cập đến vấn đề gì?',
            'options': {'A': 'A price has increased.', 'B': 'A machine needs to be repaired.', 'C': 'A product is not available.', 'D': 'A performance has been canceled.'},
            'options_vi': {'A': 'Giá đã tăng.', 'B': 'Một chiếc máy cần được sửa chữa.', 'C': 'Một sản phẩm không có sẵn.', 'D': 'Một buổi biểu diễn đã bị hủy.'},
            'ans': 'C', 'explanation': 'Người nói giải thích rằng nhà cung cấp không thể giao đèn màu tím trong 3 tuần tới, vì vậy họ không có sẵn hàng màu tím. Đáp án là C.'
        },
        {
            'num': '73', 'question': 'What does the speaker offer the listener?', 'question_vi': 'Người nói đề nghị điều gì với người nghe?',
            'options': {'A': 'Expedited shipping', 'B': 'A full refund', 'C': 'A free consultation', 'D': 'A discount'},
            'options_vi': {'A': 'Vận chuyển nhanh', 'B': 'Hoàn tiền đầy đủ', 'C': 'Tư vấn miễn phí', 'D': 'Một khoản chiết khấu/giảm giá'},
            'ans': 'D', 'explanation': 'Người nói đề nghị: "a ten percent discount on them to apologize for this" (một khoản giảm giá 10% cho chúng để xin lỗi vì điều này). Đáp án là D.'
        }
    ]
}

# Data for 74-76
content_74_76 = {
    'shadowing': [
        {'speaker': 'M-Au', 'en': "Welcome to Osterwind Estate. / The former owner, Ms. Yuping Wei, / was a famous painter. / What's special about this estate / is that Ms. Wei designed it herself, / including the landscaping.", 'vi': "Chào mừng các bạn đến với Trang dinh Osterwind. / Người chủ cũ, bà Yuping Wei, / là một họa sĩ nổi tiếng. / Điều đặc biệt về trang dinh này / là chính bà Wei đã tự thiết kế nó, / bao gồm cả phần cảnh quan."},
        {'speaker': 'M-Au', 'en': "We're asking volunteers / to clear debris / from the walkways / around the gardens / in preparation / for the estate’s first season / as a public park.", 'vi': "Chúng tôi đang yêu cầu các tình nguyện viên / dọn sạch các mảnh vụn / khỏi các lối đi / xung quanh các khu vườn / để chuẩn bị / cho mùa đầu tiên của trang dinh / với tư cách là một công viên công cộng."},
        {'speaker': 'M-Au', 'en': "You can pick up a bag and gloves / from the patio area. / And remember, / be sure to see me / as you check out / before you leave.", 'vi': "Các bạn có thể lấy túi và găng tay / từ khu vực sân thượng. / Và hãy nhớ, / chắc chắn phải gặp tôi / khi các bạn làm thủ tục ra về / trước khi rời đi."},
        {'speaker': 'M-Au', 'en': "All volunteers are eligible / for a complimentary visitor pass / that you can use / to access the estate / and attend any events / held here / all summer long.", 'vi': "Tất cả các tình nguyện viên đều đủ điều kiện / nhận một thẻ tham quan miễn phí / mà các bạn có thể sử dụng / để vào trang dinh / và tham gia bất kỳ sự kiện nào / được tổ chức ở đây / trong suốt cả mùa hè."}
    ],
    'focus': [
        {'chunk': 'designed it herself', 'vi': 'tự thiết kế nó', 'paraphrase': 'It was designed by its owner', 'q_num': '74'},
        {'chunk': 'including the landscaping', 'vi': 'bao gồm cả cảnh quan'},
        {'chunk': 'clear debris from the walkways', 'vi': 'dọn sạch mảnh vụn khỏi lối đi', 'paraphrase': 'To clean up some gardens', 'q_num': '75'},
        {'chunk': 'preparation for the first season', 'vi': 'chuẩn bị cho mùa đầu tiên'},
        {'chunk': 'public park', 'vi': 'công viên công cộng'},
        {'chunk': 'complimentary visitor pass', 'vi': 'thẻ tham quan miễn phí', 'paraphrase': 'Free passes', 'q_num': '76'}
    ],
    'word_bank': ['famous', 'designed', 'volunteers', 'debris', 'preparation', 'complimentary'],
    'filling': [
        {'speaker': 'M-Au', 'text': 'Welcome to Osterwind Estate. The former owner, Ms. Yuping Wei, was a <input type="text" data-answer="famous" class="input-blank mx-1 w-[100px]"> painter. What\'s special about this estate is that Ms. Wei <input type="text" data-answer="designed" class="input-blank mx-1 w-[100px]"> it herself.'},
        {'speaker': 'M-Au', 'text': 'We\'re asking <input type="text" data-answer="volunteers" class="input-blank mx-1 w-[120px]"> to clear <input type="text" data-answer="debris" class="input-blank mx-1 w-[100px]"> from the walkways around the gardens in <input type="text" data-answer="preparation" class="input-blank mx-1 w-[140px]"> for the estate’s first season as a public park.'},
        {'speaker': 'M-Au', 'text': 'All volunteers are eligible for a <input type="text" data-answer="complimentary" class="input-blank mx-1 w-[160px]"> visitor pass.'}
    ],
    'explanations': [
        {
            'num': '74', 'question': 'According to the speaker, what is special about Osterwind Estate?', 'question_vi': 'Theo người nói, điều gì đặc biệt ở Trang dinh Osterwind?',
            'options': {'A': 'It houses many historic paintings.', 'B': 'It was designed by its owner.', 'C': 'It includes a botanical garden.', 'D': 'It is used as a museum.'},
            'options_vi': {'A': 'Nó chứa nhiều bức tranh lịch sử.', 'B': 'Nó được thiết kế bởi chính người chủ.', 'C': 'Nó bao gồm một vườn bách thảo.', 'D': 'Nó được sử dụng như một bảo tàng.'},
            'ans': 'B', 'explanation': 'Người nói cho biết: "What\'s special about this estate is that Ms. Wei designed it herself" (Điều đặc biệt về trang dinh này là bà Wei đã tự mình thiết kế nó). Đáp án là B.'
        },
        {
            'num': '75', 'question': 'Why are the listeners at Osterwind Estate?', 'question_vi': 'Tại sao những người nghe lại ở Trang dinh Osterwind?',
            'options': {'A': 'To attend an awards ceremony', 'B': 'To apply for landscaping jobs', 'C': 'To take a tour of a building', 'D': 'To clean up some gardens'},
            'options_vi': {'A': 'Để tham dự một lễ trao giải', 'B': 'Để nộp đơn xin việc làm cảnh quan', 'C': 'Để tham gia một chuyến tham quan tòa nhà', 'D': 'Để dọn dẹp một số khu vườn'},
            'ans': 'D', 'explanation': 'Người nói đang yêu cầu các tình nguyện viên dọn dẹp các mảnh vụn từ các lối đi trong khu vườn ("clear debris from the walkways around the gardens"). Đáp án là D.'
        },
        {
            'num': '76', 'question': 'What will the listeners receive?', 'question_vi': 'Những người nghe sẽ nhận được gì?',
            'options': {'A': 'Gift-shop coupons', 'B': 'Free passes', 'C': 'Lunch boxes', 'D': 'T-shirts'},
            'options_vi': {'A': 'Phiếu giảm giá tại cửa hàng quà tặng', 'B': 'Thẻ tham quan miễn phí', 'C': 'Hộp cơm trưa', 'D': 'Áo phông'},
            'ans': 'B', 'explanation': 'Người nói thông báo: "All volunteers are eligible for a complimentary visitor pass" (Tất cả các tình nguyện viên đều đủ điều kiện nhận thẻ tham quan miễn phí). Đáp án là B.'
        }
    ]
}

# Data for 77-79
content_77_79 = {
    'shadowing': [
        {'speaker': 'M-Cn', 'en': "Good morning, Ms. Espinosa. / This is Marcel Fournier. / It's Saturday morning, / and I'm on my way / to the airport.", 'vi': "Chào buổi sáng, bà Espinosa. / Tôi là Marcel Fournier. / Bây giờ là sáng thứ Bảy, / và tôi đang trên đường / ra sân bay."},
        {'speaker': 'M-Cn', 'en': "This is a little out of the ordinary, / but l'm calling / because in my haste / I left a note / with Mr. Hang's mobile phone number / on my office desk.", 'vi': "Việc này hơi khác thường một chút, / nhưng tôi gọi điện / bởi vì trong lúc vội vã / tôi đã để quên một mẩu giấy / có số điện thoại di động của ông Hang / trên bàn làm việc của mình."},
        {'speaker': 'M-Cn', 'en': "He's picking me up / from the airport, / and I'll be stuck / if I can't reach him. / I'll need you / to go into the office / and text me / with the number. / I know this is inconvenient.", 'vi': "Ông ấy sẽ đón tôi / từ sân bay, / và tôi sẽ gặp rắc rối / nếu không thể liên lạc được với ông ấy. / Tôi sẽ cần bà / vào văn phòng / và nhắn tin cho tôi / số điện thoại đó. / Tôi biết việc này thật bất tiện."},
        {'speaker': 'M-Cn', 'en': "I'll check my messages / once I land in San Diego.", 'vi': "Tôi sẽ kiểm tra tin nhắn / ngay khi tôi hạ cánh xuống San Diego."}
    ],
    'focus': [
        {'chunk': 'on my way to the airport', 'vi': 'đang trên đường ra sân bay'},
        {'chunk': 'left a note on my office desk', 'vi': 'để quên mẩu giấy trên bàn làm việc', 'paraphrase': 'An administrative assistant', 'q_num': '77'},
        {'chunk': 'mobile phone number', 'vi': 'số điện thoại di động'},
        {'chunk': 'text me with the number', 'vi': 'nhắn tin cho tôi số đó'},
        {'chunk': 'I know this is inconvenient', 'vi': 'tôi biết việc này thật bất tiện', 'paraphrase': 'To apologize for a request', 'q_num': '78'},
        {'chunk': 'land in San Diego', 'vi': 'hạ cánh ở San Diego', 'paraphrase': 'Retrieve his messages', 'q_num': '79'}
    ],
    'word_bank': ['ordinary', 'haste', 'mobile', 'stuck', 'inconvenient', 'land'],
    'filling': [
        {'speaker': 'M-Cn', 'text': 'This is a little out of the <input type="text" data-answer="ordinary" class="input-blank mx-1 w-[100px]">, but l\'m calling because in my <input type="text" data-answer="haste" class="input-blank mx-1 w-[100px]"> I left a note with Mr. Hang\'s <input type="text" data-answer="mobile" class="input-blank mx-1 w-[100px]"> phone number on my office desk.'},
        {'speaker': 'M-Cn', 'text': 'He\'s picking me up from the airport, and I\'ll be <input type="text" data-answer="stuck" class="input-blank mx-1 w-[100px]"> if I can\'t reach him. I\'ll need you to go into the office and text me with the number. I know this is <input type="text" data-answer="inconvenient" class="input-blank mx-1 w-[140px]">.'},
        {'speaker': 'M-Cn', 'text': 'I\'ll check my messages once I <input type="text" data-answer="land" class="input-blank mx-1 w-[100px]"> in San Diego.'}
    ],
    'explanations': [
        {
            'num': '77', 'question': 'Who most likely is the listener?', 'question_vi': 'Người nghe có khả năng nhất là ai?',
            'options': {'A': 'A travel agent', 'B': 'An administrative assistant', 'C': 'A flight attendant', 'D': 'A security guard'},
            'options_vi': {'A': 'Một đại lý du lịch', 'B': 'Một trợ lý hành chính', 'C': 'Một tiếp viên hàng không', 'D': 'Một nhân viên bảo vệ'},
            'ans': 'B', 'explanation': 'Người nói nhờ người nghe vào văn phòng của mình để tìm một mẩu giấy trên bàn làm việc. Đây là công việc của một trợ lý hành chính. Đáp án là B.'
        },
        {
            'num': '78', 'question': 'Why does the speaker say, “I know this is inconvenient”?', 'question_vi': 'Tại sao người nói lại nói: "Tôi biết việc này thật bất tiện"?',
            'options': {'A': 'To suggest a deadline extension', 'B': 'To report on an additional cost', 'C': 'To offer an alternative solution', 'D': 'To apologize for a request'},
            'options_vi': {'A': 'Để đề xuất gia hạn thời hạn', 'B': 'Để báo cáo về một chi phí bổ sung', 'C': 'Để đưa ra một giải pháp thay thế', 'D': 'Để xin lỗi vì một lời yêu cầu'},
            'ans': 'D', 'explanation': 'Người nói đang nhờ người nghe làm một việc vào sáng thứ Bảy (ngày nghỉ), vì vậy ông ấy nói câu này để xin lỗi vì lời yêu cầu gây phiền hà. Đáp án là D.'
        },
        {
            'num': '79', 'question': 'What will the speaker do when he arrives in San Diego?', 'question_vi': 'Người nói sẽ làm gì khi ông ấy đến San Diego?',
            'options': {'A': 'Retrieve his messages', 'B': 'Check in to a hotel', 'C': 'Change a flight reservation', 'D': 'Visit a company office'},
            'options_vi': {'A': 'Kiểm tra các tin nhắn của mình', 'B': 'Làm thủ tục nhận phòng khách sạn', 'C': 'Thay đổi đặt chỗ chuyến bay', 'D': 'Ghé thăm văn phòng công ty'},
            'ans': 'A', 'explanation': 'Người nói cho biết: "I\'ll check my messages once I land in San Diego" (Tôi sẽ kiểm tra tin nhắn khi hạ cánh xuống San Diego). Đáp án là A.'
        }
    ]
}

# Data for 80-82
content_80_82 = {
    'shadowing': [
        {'speaker': 'W-Am', 'en': "Hi, everyone! / Thanks for watching today. / If you're new to my channel, / you should know / that my videos focus on ways / that we can repurpose / common objects / so that they don’t end up / in landfills.", 'vi': "Chào mọi người! / Cảm ơn các bạn đã xem ngày hôm nay. / Nếu bạn là người mới đến với kênh của tôi, / bạn nên biết / rằng các video của tôi tập trung vào những cách / mà chúng ta có thể tái sử dụng / các vật dụng thông thường / để chúng không bị vứt / ra bãi rác."},
        {'speaker': 'W-Am', 'en': "In this video, / you'll learn how to make candles / from old and leftover crayons. / Your first step / is to collect the items you'll need.", 'vi': "Trong video này, / các bạn sẽ học cách làm nến / từ những chiếc bút màu cũ và còn sót lại. / Bước đầu tiên của các bạn / là thu thập các vật dụng cần thiết."},
        {'speaker': 'W-Am', 'en': "You may already have / some old crayons around the house, / or you can ask / your friends and neighbors / for theirs.", 'vi': "Bạn có thể đã có sẵn / một số bút màu cũ quanh nhà, / hoặc bạn có thể hỏi / bạn bè và hàng xóm / để xin những cái của họ."},
        {'speaker': 'W-Am', 'en': "I'll be covering a lot of steps, / but don’t worry, / a full written version / of the instructions / is available on my Web site.", 'vi': "Tôi sẽ thực hiện rất nhiều bước, / nhưng đừng lo lắng, / một bản hướng dẫn đầy đủ / bằng văn bản / có sẵn trên trang web của tôi."},
        {'speaker': 'W-Am', 'en': "I recommend / downloading those later / for future reference.", 'vi': "Tôi khuyên các bạn / hãy tải chúng xuống sau / để tham khảo trong tương lai."}
    ],
    'focus': [
        {'chunk': 'repurpose common objects', 'vi': 'tái sử dụng vật dụng thông thường', 'paraphrase': 'How to reuse items', 'q_num': '80'},
        {'chunk': 'end up in landfills', 'vi': 'vứt ra bãi rác'},
        {'chunk': 'make candles from old crayons', 'vi': 'làm nến từ bút màu cũ'},
        {'chunk': 'collect the items you\'ll need', 'vi': 'thu thập các vật dụng cần thiết', 'paraphrase': 'Gathering supplies', 'q_num': '81'},
        {'chunk': 'full written version of the instructions', 'vi': 'bản hướng dẫn đầy đủ bằng văn bản', 'paraphrase': 'Download some instructions', 'q_num': '82'},
        {'chunk': 'future reference', 'vi': 'tham khảo trong tương lai'}
    ],
    'word_bank': ['repurpose', 'common', 'landfills', 'candles', 'crayons', 'instructions'],
    'filling': [
        {'speaker': 'W-Am', 'text': 'If you\'re new to my channel, you should know that my videos focus on ways that we can <input type="text" data-answer="repurpose" class="input-blank mx-1 w-[120px]"> <input type="text" data-answer="common" class="input-blank mx-1 w-[100px]"> objects so that they don’t end up in <input type="text" data-answer="landfills" class="input-blank mx-1 w-[120px]">.'},
        {'speaker': 'W-Am', 'text': 'In this video, you\'ll learn how to make <input type="text" data-answer="candles" class="input-blank mx-1 w-[100px]"> from old and leftover <input type="text" data-answer="crayons" class="input-blank mx-1 w-[100px]">.'},
        {'speaker': 'W-Am', 'text': 'I\'ll be covering a lot of steps, but don’t worry, a full written version of the <input type="text" data-answer="instructions" class="input-blank mx-1 w-[140px]"> is available on my Web site.'}
    ],
    'explanations': [
        {
            'num': '80', 'question': 'What does the speaker say her videos are usually about?', 'question_vi': 'Người nói cho biết các video của cô ấy thường nói về điều gì?',
            'options': {'A': 'How to plan trips', 'B': 'How to reuse items', 'C': 'How to organize closets', 'D': 'How to draw landscapes'},
            'options_vi': {'A': 'Cách lên kế hoạch cho các chuyến đi', 'B': 'Cách tái sử dụng các món đồ', 'C': 'Cách sắp xếp tủ quần áo', 'D': 'Cách vẽ phong cảnh'},
            'ans': 'B', 'explanation': 'Người nói cho biết các video của cô tập trung vào việc "repurpose common objects" (tái sử dụng các vật dụng thông thường). Điều này tương ứng với việc tái sử dụng đồ vật. Đáp án là B.'
        },
        {
            'num': '81', 'question': 'What first step does the speaker mention?', 'question_vi': 'Bước đầu tiên mà người nói đề cập là gì?',
            'options': {'A': 'Writing a list', 'B': 'Finding coupons', 'C': 'Gathering supplies', 'D': 'Looking at images online'},
            'options_vi': {'A': 'Viết một danh sách', 'B': 'Tìm phiếu giảm giá', 'C': 'Thu thập vật tư', 'D': 'Xem hình ảnh trực tuyến'},
            'ans': 'C', 'explanation': 'Người nói cho biết: "Your first step is to collect the items you\'ll need" (Bước đầu tiên của bạn là thu thập các vật dụng bạn sẽ cần). Đáp án là C.'
        },
        {
            'num': '82', 'question': 'According to the speaker, what can the listeners do on a Web site?', 'question_vi': 'Theo người nói, người nghe có thể làm gì trên trang web?',
            'options': {'A': 'Enter a contest', 'B': 'Subscribe to a video channel', 'C': 'Submit some photographs', 'D': 'Download some instructions'},
            'options_vi': {'A': 'Tham gia một cuộc thi', 'B': 'Đăng ký một kênh video', 'C': 'Gửi một số bức ảnh', 'D': 'Tải xuống một số hướng dẫn'},
            'ans': 'D', 'explanation': 'Người nói cho biết: "a full written version of the instructions is available on my Web site. I recommend downloading those..." (một bản hướng dẫn đầy đủ bằng văn bản có sẵn trên trang web của tôi. Tôi khuyên bạn nên tải chúng xuống...). Đáp án là D.'
        }
    ]
}

update_html('Test 5/LC-T5-P4-Q71-73.html', content_71_73)
update_html('Test 5/LC-T5-P4-Q74-76.html', content_74_76)
update_html('Test 5/LC-T5-P4-Q77-79.html', content_77_79)
update_html('Test 5/LC-T5-P4-Q80-82.html', content_80_82)

