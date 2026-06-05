import json
import os
import re
from update_t6_p4 import update_html

# Data for 71-73
content_71_73 = {
    'shadowing': [
        {'speaker': 'M-Au', 'en': "Hi, everyone—big news. / Our clinic is getting / a check-in kiosk. / What this means / is that patients / will be able to check themselves in / to their medical appointments / by clicking through / some buttons in the kiosk.", 'vi': "Chào mọi người—tin quan trọng đây. / Phòng khám của chúng ta / sẽ có một ki-ốt tự đăng ký. / Điều này có nghĩa là / bệnh nhân / sẽ có thể tự mình đăng ký / cho các cuộc hẹn khám bệnh của họ / bằng cách nhấp qua / một số nút bấm trong ki-ốt."},
        {'speaker': 'M-Au', 'en': "You will no longer / have to do it for them. / I know all of you / have been very busy / answering phones, / scheduling appointments, / and checking patients in, / so hopefully, this helps / to make your work easier.", 'vi': "Các bạn sẽ không còn / phải làm việc đó cho họ nữa. / Tôi biết tất cả các bạn / đã rất bận rộn / với việc trả lời điện thoại, / lên lịch hẹn, / và làm thủ tục cho bệnh nhân, / vì vậy hy vọng điều này / sẽ giúp công việc của các bạn dễ dàng hơn."},
        {'speaker': 'M-Au', 'en': "We'll have / a very short training session / next Tuesday / on how the check-in kiosk works.", 'vi': "Chúng ta sẽ có / một buổi đào tạo rất ngắn / vào thứ Ba tới / về cách thức hoạt động của ki-ốt tự đăng ký."}
    ],
    'focus': [
        {'chunk': 'clinic', 'vi': 'phòng khám', 'paraphrase': 'At a medical clinic', 'q_num': '71'},
        {'chunk': 'check-in kiosk', 'vi': 'ki-ốt tự đăng ký', 'paraphrase': 'An electronic check-in system', 'q_num': '72'},
        {'chunk': 'check themselves in', 'vi': 'tự mình làm thủ tục đăng ký'},
        {'chunk': 'scheduling appointments', 'vi': 'lên lịch hẹn'},
        {'chunk': 'make your work easier', 'vi': 'giúp công việc dễ dàng hơn'},
        {'chunk': 'training session next Tuesday', 'vi': 'buổi đào tạo vào thứ Ba tới', 'paraphrase': 'A training session will take place', 'q_num': '73'}
    ],
    'word_bank': ['clinic', 'check-in', 'kiosk', 'appointments', 'scheduling', 'training'],
    'filling': [
        {'speaker': 'M-Au', 'text': 'Hi, everyone—big news. Our <input type="text" data-answer="clinic" class="input-blank mx-1 w-[100px]"> is getting a <input type="text" data-answer="check-in" class="input-blank mx-1 w-[100px]"> <input type="text" data-answer="kiosk" class="input-blank mx-1 w-[100px]">.'},
        {'speaker': 'M-Au', 'text': 'I know all of you have been very busy answering phones, <input type="text" data-answer="scheduling" class="input-blank mx-1 w-[120px]"> <input type="text" data-answer="appointments" class="input-blank mx-1 w-[120px]">, and checking patients in.'},
        {'speaker': 'M-Au', 'text': 'We\'ll have a very short <input type="text" data-answer="training" class="input-blank mx-1 w-[100px]"> session next Tuesday.'}
    ],
    'explanations': [
        {
            'num': '71', 'question': 'Where does the talk most likely take place?', 'question_vi': 'Bài nói chuyện có khả năng nhất diễn ra ở đâu?',
            'options': {'A': 'At a medical clinic', 'B': 'At an airport', 'C': 'At a fitness center', 'D': 'At a bank'},
            'options_vi': {'A': 'Tại một phòng khám y tế', 'B': 'Tại sân bay', 'C': 'Tại một trung tâm thể dục', 'D': 'Tại một ngân hàng'},
            'ans': 'A', 'explanation': 'Người nói nhắc đến "Our clinic" (phòng khám của chúng ta) và "medical appointments" (các cuộc hẹn y tế). Đáp án là A.'
        },
        {
            'num': '72', 'question': 'What is mainly being discussed?', 'question_vi': 'Vấn đề gì chủ yếu đang được thảo luận?',
            'options': {'A': 'A hiring decision', 'B': 'A marketing campaign', 'C': 'A customer satisfaction survey', 'D': 'An electronic check-in system'},
            'options_vi': {'A': 'Một quyết định tuyển dụng', 'B': 'Một chiến dịch tiếp thị', 'C': 'Một khảo sát sự hài lòng của khách hàng', 'D': 'Một hệ thống đăng ký điện tử'},
            'ans': 'D', 'explanation': 'Chủ đề chính là về việc phòng khám có thêm "check-in kiosk" để bệnh nhân tự đăng ký. Đây là một hệ thống đăng ký điện tử. Đáp án là D.'
        },
        {
            'num': '73', 'question': 'What will happen next Tuesday?', 'question_vi': 'Điều gì sẽ xảy ra vào thứ Ba tới?',
            'options': {'A': 'A new security system will be installed.', 'B': 'A branch location will open.', 'C': 'A training session will take place.', 'D': 'A product will be delivered.'},
            'options_vi': {'A': 'Một hệ thống an ninh mới sẽ được lắp đặt.', 'B': 'Một chi nhánh sẽ mở cửa.', 'C': 'Một buổi đào tạo sẽ diễn ra.', 'D': 'Một sản phẩm sẽ được giao.'},
            'ans': 'C', 'explanation': 'Người nói thông báo: "We\'ll have a very short training session next Tuesday" (Chúng ta sẽ có một buổi đào tạo rất ngắn vào thứ Ba tới). Đáp án là C.'
        }
    ]
}

# Data for 74-76
content_74_76 = {
    'shadowing': [
        {'speaker': 'W-Br', 'en': "Welcome to a new episode / of Tomorrow's Technology. / Today we'll be talking / about drones. / If you're planning / to buy your first drone, / here are a few things / you need to know.", 'vi': "Chào mừng các bạn đến với một tập mới / của Công nghệ Ngày mai. / Hôm nay chúng ta sẽ thảo luận / về máy bay không người lái (drone). / Nếu bạn đang có kế hoạch / mua chiếc drone đầu tiên của mình, / đây là một vài điều / bạn cần biết."},
        {'speaker': 'W-Br', 'en': "To begin with, / if you want to use the device / for commercial purposes, / such as photography / or videography, / then you'll need / to apply for a license.", 'vi': "Trước hết, / nếu bạn muốn sử dụng thiết bị / cho mục đích thương mại, / chẳng hạn như chụp ảnh / hoặc quay phim, / thì bạn sẽ cần / phải xin giấy phép."},
        {'speaker': 'W-Br', 'en': "I'll share some resources / at the end of this podcast / to guide / your application process.", 'vi': "Tôi sẽ chia sẻ một số tài nguyên / ở cuối podcast này / để hướng dẫn / quá trình nộp đơn của bạn."}
    ],
    'focus': [
        {'chunk': "Tomorrow's Technology", 'vi': 'Công nghệ Ngày mai', 'paraphrase': 'Technology enthusiasts', 'q_num': '74'},
        {'chunk': 'drones', 'vi': 'máy bay không người lái'},
        {'chunk': 'commercial purposes', 'vi': 'mục đích thương mại'},
        {'chunk': 'apply for a license', 'vi': 'xin giấy phép', 'paraphrase': 'A license', 'q_num': '75'},
        {'chunk': 'share some resources', 'vi': 'chia sẻ một số tài nguyên', 'paraphrase': 'Application instructions', 'q_num': '76'},
        {'chunk': 'application process', 'vi': 'quá trình nộp đơn'}
    ],
    'word_bank': ['episode', 'technology', 'drones', 'commercial', 'license', 'resources'],
    'filling': [
        {'speaker': 'W-Br', 'text': 'Welcome to a new <input type="text" data-answer="episode" class="input-blank mx-1 w-[100px]"> of Tomorrow\'s <input type="text" data-answer="technology" class="input-blank mx-1 w-[120px]">. Today we\'ll be talking about <input type="text" data-answer="drones" class="input-blank mx-1 w-[100px]">.'},
        {'speaker': 'W-Br', 'text': 'If you want to use the device for <input type="text" data-answer="commercial" class="input-blank mx-1 w-[120px]"> purposes, then you\'ll need to apply for a <input type="text" data-answer="license" class="input-blank mx-1 w-[100px]">.'},
        {'speaker': 'W-Br', 'text': 'I\'ll share some <input type="text" data-answer="resources" class="input-blank mx-1 w-[120px]"> at the end of this podcast.'}
    ],
    'explanations': [
        {
            'num': '74', 'question': 'Who is the podcast intended for?', 'question_vi': 'Podcast này dành cho đối tượng nào?',
            'options': {'A': 'Party organizers', 'B': 'Travel agents', 'C': 'Technology enthusiasts', 'D': 'Carpenters'},
            'options_vi': {'A': 'Những người tổ chức tiệc', 'B': 'Các đại lý du lịch', 'C': 'Những người đam mê công nghệ', 'D': 'Thợ mộc'},
            'ans': 'C', 'explanation': 'Chương trình có tên là "Tomorrow\'s Technology" (Công nghệ Ngày mai) và thảo luận về drone. Đây là chủ đề dành cho những người đam mê công nghệ. Đáp án là C.'
        },
        {
            'num': '75', 'question': 'According to the speaker, what will some listeners need?', 'question_vi': 'Theo người nói, một số người nghe sẽ cần gì?',
            'options': {'A': 'An insurance policy', 'B': 'A letter of recommendation', 'C': 'An event venue', 'D': 'A license'},
            'options_vi': {'A': 'Một đơn bảo hiểm', 'B': 'Một thư giới thiệu', 'C': 'Một địa điểm tổ chức sự kiện', 'D': 'Một giấy phép'},
            'ans': 'D', 'explanation': 'Người nói cho biết: "if you want to use the device for commercial purposes... then you\'ll need to apply for a license" (nếu bạn muốn sử dụng thiết bị cho mục đích thương mại... thì bạn sẽ cần phải xin giấy phép). Đáp án là D.'
        },
        {
            'num': '76', 'question': 'What information will the speaker share?', 'question_vi': 'Thông tin nào người nói sẽ chia sẻ?',
            'options': {'A': 'Application instructions', 'B': 'Retail locations', 'C': 'Names of instructors', 'D': 'User reviews'},
            'options_vi': {'A': 'Hướng dẫn nộp đơn', 'B': 'Các địa điểm bán lẻ', 'C': 'Tên của các giảng viên', 'D': 'Đánh giá của người dùng'},
            'ans': 'A', 'explanation': 'Người nói cho biết cô ấy sẽ chia sẻ các tài nguyên để "guide your application process" (hướng dẫn quá trình nộp đơn của bạn). Đáp án là A.'
        }
    ]
}

# Data for 77-79
content_77_79 = {
    'shadowing': [
        {'speaker': 'M-Au', 'en': "Attention, exhibitors. / Welcome to the Digital Signage Expo, / where representatives / selling digital billboards / and video displays / can interact / directly with buyers.", 'vi': "Xin lưu ý, các nhà triển lãm. / Chào mừng các bạn đến với Triển lãm Biển báo Kỹ thuật số, / nơi những người đại diện / bán biển quảng cáo kỹ thuật số / và màn hình hiển thị video / có thể tương tác / trực tiếp với người mua."},
        {'speaker': 'M-Au', 'en': "The exhibit hall / will open in fifteen minutes. / To ensure everyone's safety, / we request / that you clear your exhibit area / of boxes and debris / and be sure cables / and electrical cords / are securely taped / to the floor.", 'vi': "Sảnh triển lãm / sẽ mở cửa sau mười lăm phút nữa. / Để đảm bảo an toàn cho mọi người, / chúng tôi yêu cầu / các bạn dọn dẹp khu vực triển lãm của mình / sạch các thùng hộp và mảnh vụn / và đảm bảo các loại cáp / và dây điện / được dán chặt / xuống sàn."},
        {'speaker': 'M-Au', 'en': "And remember, / the exhibit hall will close / at five p.m. today / so that exhibitors / can attend this evening’s reception. / That will be held / in the building’s main lobby.", 'vi': "Và hãy nhớ, / sảnh triển lãm sẽ đóng cửa / lúc 5 giờ chiều nay / để các nhà triển lãm / có thể tham dự buổi chiêu đãi tối nay. / Buổi đó sẽ được tổ chức / tại sảnh chính của tòa nhà."}
    ],
    'focus': [
        {'chunk': 'exhibitors', 'vi': 'nhà triển lãm', 'paraphrase': 'Trade show participants', 'q_num': '77'},
        {'chunk': 'Digital Signage Expo', 'vi': 'Triển lãm Biển báo Kỹ thuật số'},
        {'chunk': 'ensure everyone\'s safety', 'vi': 'đảm bảo an toàn cho mọi người', 'paraphrase': 'Take safety precautions', 'q_num': '78'},
        {'chunk': 'cables and electrical cords', 'vi': 'cáp và dây điện'},
        {'chunk': 'securely taped to the floor', 'vi': 'dán chặt xuống sàn'},
        {'chunk': 'this evening’s reception', 'vi': 'buổi chiêu đãi tối nay', 'paraphrase': 'A reception', 'q_num': '79'}
    ],
    'word_bank': ['exhibitors', 'signage', 'representatives', 'interact', 'ensure', 'reception'],
    'filling': [
        {'speaker': 'M-Au', 'text': 'Attention, <input type="text" data-answer="exhibitors" class="input-blank mx-1 w-[100px]">. Welcome to the Digital <input type="text" data-answer="signage" class="input-blank mx-1 w-[100px]"> Expo, where <input type="text" data-answer="representatives" class="input-blank mx-1 w-[140px]"> can <input type="text" data-answer="interact" class="input-blank mx-1 w-[100px]"> directly with buyers.'},
        {'speaker': 'M-Au', 'text': 'To <input type="text" data-answer="ensure" class="input-blank mx-1 w-[100px]"> everyone\'s safety, we request that you clear your exhibit area.'},
        {'speaker': 'M-Au', 'text': 'The exhibit hall will close so that exhibitors can attend this evening’s <input type="text" data-answer="reception" class="input-blank mx-1 w-[100px]">.'}
    ],
    'explanations': [
        {
            'num': '77', 'question': 'Who are the listeners?', 'question_vi': 'Những người nghe là ai?',
            'options': {'A': 'Mechanical engineers', 'B': 'Trade show participants', 'C': 'Government officials', 'D': 'Laboratory assistants'},
            'options_vi': {'A': 'Các kỹ sư cơ khí', 'B': 'Những người tham gia triển lãm thương mại', 'C': 'Các quan chức chính phủ', 'D': 'Các trợ lý phòng thí nghiệm'},
            'ans': 'B', 'explanation': 'Người nói mở đầu bằng: "Attention, exhibitors" (Xin lưu ý, các nhà triển lãm) và nhắc đến việc bán hàng tại triển lãm. Đây là những người tham gia triển lãm thương mại. Đáp án là B.'
        },
        {
            'num': '78', 'question': 'What does the speaker request that the listeners do?', 'question_vi': 'Người nói yêu cầu người nghe làm gì?',
            'options': {'A': 'Take safety precautions', 'B': 'Sign a registration sheet', 'C': 'Wear name tags', 'D': 'Move their vehicles'},
            'options_vi': {'A': 'Thực hiện các biện pháp phòng ngừa an toàn', 'B': 'Ký vào tờ đăng ký', 'C': 'Đeo thẻ tên', 'D': 'Di chuyển phương tiện của họ'},
            'ans': 'A', 'explanation': 'Người nói yêu cầu: "To ensure everyone\'s safety, we request that you clear your exhibit area... be sure cables... are securely taped" (Để đảm bảo an toàn, chúng tôi yêu cầu dọn dẹp... dán chặt dây cáp). Đây là các biện pháp an toàn. Đáp án là A.'
        },
        {
            'num': '79', 'question': 'What will take place in the evening?', 'question_vi': 'Điều gì sẽ diễn ra vào buổi tối?',
            'options': {'A': 'A debate', 'B': 'An award ceremony', 'C': 'A film screening', 'D': 'A reception'},
            'options_vi': {'A': 'Một cuộc tranh luận', 'B': 'Một lễ trao giải', 'C': 'Một buổi chiếu phim', 'D': 'Một buổi chiêu đãi'},
            'ans': 'D', 'explanation': 'Người nói nhắc đến: "this evening’s reception" (buổi chiêu đãi tối nay). Đáp án là D.'
        }
    ]
}

# Data for 80-82
content_80_82 = {
    'shadowing': [
        {'speaker': 'M-Cn', 'en': "Welcome to Money Reveals, / the podcast / for smart investors. / This week, / I'll be discussing the best tips / for amateur investors, / if you're just getting started.", 'vi': "Chào mừng đến với Money Reveals, / podcast / dành cho những nhà đầu tư thông thái. / Tuần này, / tôi sẽ thảo luận về những lời khuyên tốt nhất / cho các nhà đầu tư nghiệp dư, / nếu bạn vừa mới bắt đầu."},
        {'speaker': 'M-Cn', 'en': "But first, / this episode / is brought to you / by CodeWord. / Don’t search online / for discount coupons / any longer!", 'vi': "Nhưng trước tiên, / tập này / được mang đến cho các bạn / bởi CodeWord. / Đừng tìm kiếm trực tuyến / các mã giảm giá / thêm nữa!"},
        {'speaker': 'M-Cn', 'en': "CodeWord is a software application / that scans the Internet / for promotional codes / and applies them / to your online shopping cart. / If CodeWord finds any discounts, / an Apply Coupon button / will automatically appear / at checkout.", 'vi': "CodeWord là một ứng dụng phần mềm / quét Internet / để tìm các mã khuyến mại / và áp dụng chúng / vào giỏ hàng trực tuyến của bạn. / Nếu CodeWord tìm thấy bất kỳ khoản chiết khấu nào, / một nút Áp dụng mã giảm giá / sẽ tự động xuất hiện / khi thanh toán."},
        {'speaker': 'M-Cn', 'en': "What's more, / the first 100 listeners / to use the download link / on my Web site / will receive / free music festival tickets.", 'vi': "Hơn thế nữa, / 100 người nghe đầu tiên / sử dụng liên kết tải xuống / trên trang web của tôi / sẽ nhận được / vé tham dự lễ hội âm nhạc miễn phí."}
    ],
    'focus': [
        {'chunk': 'Money Reveals', 'vi': 'Tên podcast (Tiết lộ về Tiền bạc)', 'paraphrase': 'A podcast host', 'q_num': '80'},
        {'chunk': 'amateur investors', 'vi': 'nhà đầu tư nghiệp dư'},
        {'chunk': 'discount coupons / promotional codes', 'vi': 'phiếu giảm giá / mã khuyến mại', 'paraphrase': 'Searching for discounts', 'q_num': '81'},
        {'chunk': 'scans the Internet', 'vi': 'quét Internet'},
        {'chunk': 'shopping cart', 'vi': 'giỏ hàng'},
        {'chunk': 'download link on my Web site', 'vi': 'liên kết tải xuống trên trang web của tôi', 'paraphrase': 'By clicking on a link', 'q_num': '82'}
    ],
    'word_bank': ['investors', 'amateur', 'episode', 'discount', 'promotional', 'automatically'],
    'filling': [
        {'speaker': 'M-Cn', 'text': 'Welcome to Money Reveals, the podcast for smart <input type="text" data-answer="investors" class="input-blank mx-1 w-[100px]">. This week, I\'ll be discussing the best tips for <input type="text" data-answer="amateur" class="input-blank mx-1 w-[100px]"> investors.'},
        {'speaker': 'M-Cn', 'text': 'But first, this <input type="text" data-answer="episode" class="input-blank mx-1 w-[100px]"> is brought to you by CodeWord.'},
        {'speaker': 'M-Cn', 'text': 'CodeWord is a software application that scans the Internet for <input type="text" data-answer="promotional" class="input-blank mx-1 w-[120px]"> codes. If CodeWord finds any <input type="text" data-answer="discount" class="input-blank mx-1 w-[100px]">, a button will <input type="text" data-answer="automatically" class="input-blank mx-1 w-[140px]"> appear.'}
    ],
    'explanations': [
        {
            'num': '80', 'question': 'Who most likely is the speaker?', 'question_vi': 'Người nói có khả năng nhất là ai?',
            'options': {'A': 'A customer service representative', 'B': 'A software developer', 'C': 'A podcast host', 'D': 'An event coordinator'},
            'options_vi': {'A': 'Một đại diện dịch vụ khách hàng', 'B': 'Một nhà phát triển phần mềm', 'C': 'Một người dẫn chương trình podcast', 'D': 'Một điều phối viên sự kiện'},
            'ans': 'C', 'explanation': 'Người nói bắt đầu bằng: "Welcome to Money Reveals, the podcast for smart investors" (Chào mừng đến với Money Reveals, podcast dành cho các nhà đầu tư thông thái). Điều này chỉ ra ông ấy là người dẫn chương trình podcast. Đáp án là C.'
        },
        {
            'num': '81', 'question': 'According to the speaker, what can a software application be used for?', 'question_vi': 'Theo người nói, một ứng dụng phần mềm có thể được sử dụng để làm gì?',
            'options': {'A': 'Making travel reservations', 'B': 'Uploading documents', 'C': 'Managing subscriptions', 'D': 'Searching for discounts'},
            'options_vi': {'A': 'Đặt chỗ du lịch', 'B': 'Tải tài liệu lên', 'C': 'Quản lý các đăng ký', 'D': 'Tìm kiếm các khoản giảm giá'},
            'ans': 'D', 'explanation': 'Người nói mô tả ứng dụng CodeWord giúp người dùng không phải tìm kiếm "discount coupons" (mã giảm giá) vì nó tự động quét Internet để tìm mã khuyến mại. Đáp án là D.'
        },
        {
            'num': '82', 'question': 'How can the listeners receive some free tickets?', 'question_vi': 'Làm thế nào người nghe có thể nhận được một số vé miễn phí?',
            'options': {'A': 'By clicking on a link', 'B': 'By signing up for a newsletter', 'C': 'By buying a product in-store', 'D': 'By writing a review'},
            'options_vi': {'A': 'Bằng cách nhấp vào một liên kết', 'B': 'Bằng cách đăng ký nhận bản tin', 'C': 'Bằng cách mua sản phẩm tại cửa hàng', 'D': 'Bằng cách viết một đánh giá'},
            'ans': 'A', 'explanation': 'Người nói cho biết 100 người nghe đầu tiên sử dụng "the download link on my Web site" (liên kết tải xuống trên trang web của tôi) sẽ nhận được vé. Sử dụng liên kết tương ứng với việc nhấp vào liên kết đó. Đáp án là A.'
        }
    ]
}

update_html('Test 6/LC-T6-P4-Q71-73.html', content_71_73)
update_html('Test 6/LC-T6-P4-Q74-76.html', content_74_76)
update_html('Test 6/LC-T6-P4-Q77-79.html', content_77_79)
update_html('Test 6/LC-T6-P4-Q80-82.html', content_80_82)

