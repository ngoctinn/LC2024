import json
import os
import re
from update_t5_p4 import update_html

# Data for 83-85
content_83_85 = {
    'shadowing': [
        {'speaker': 'W-Br', 'en': "Thank you all for coming / to this press conference. / As you know, / the Grand Falls Bridge / improvement work / has been underway / for almost a year.", 'vi': "Cảm ơn tất cả các bạn đã đến / buổi họp báo này. / Như các bạn đã biết, / công việc cải tạo / Cầu Grand Falls / đã được triển khai / trong gần một năm nay."},
        {'speaker': 'W-Br', 'en': "We're nearing the final stage / of sanding and painting / the newly built portions.", 'vi': "Chúng tôi đang tiến gần đến giai đoạn cuối / là chà nhám và sơn / các phần mới được xây dựng."},
        {'speaker': 'W-Br', 'en': "I know the fishing community / has expressed concern / over the potential environmental impact / of this project / on our local marine life.", 'vi': "Tôi biết cộng đồng đánh cá / đã bày tỏ sự lo ngại / về tác động môi trường tiềm tàng / của dự án này / đối với sinh vật biển địa phương của chúng ta."},
        {'speaker': 'W-Br', 'en': "Well, all required studies / were conducted a year ago. / I'll take some questions now.", 'vi': "Vâng, tất cả các nghiên cứu cần thiết / đã được tiến hành cách đây một năm. / Bây giờ tôi sẽ trả lời một số câu hỏi."},
        {'speaker': 'W-Br', 'en': "After that, / our special-events coordinator / will discuss / the bridge-opening ceremony / that’s being planned.", 'vi': "Sau đó, / điều phối viên sự kiện đặc biệt của chúng tôi / sẽ thảo luận về / lễ khánh thành cầu / đang được lên kế hoạch."}
    ],
    'focus': [
        {'chunk': 'Grand Falls Bridge improvement work', 'vi': 'công việc cải tạo cầu Grand Falls', 'paraphrase': 'A construction project', 'q_num': '83'},
        {'chunk': 'sanding and painting', 'vi': 'chà nhám và sơn'},
        {'chunk': 'potential environmental impact', 'vi': 'tác động môi trường tiềm tàng'},
        {'chunk': 'required studies were conducted', 'vi': 'các nghiên cứu yêu cầu đã được tiến hành', 'paraphrase': 'To provide reassurance', 'q_num': '84'},
        {'chunk': 'special-events coordinator', 'vi': 'điều phối viên sự kiện đặc biệt'},
        {'chunk': 'bridge-opening ceremony', 'vi': 'lễ khánh thành cầu', 'paraphrase': 'A ceremony', 'q_num': '85'}
    ],
    'word_bank': ['conference', 'improvement', 'underway', 'environmental', 'conducted', 'ceremony'],
    'filling': [
        {'speaker': 'W-Br', 'text': 'Thank you all for coming to this press <input type="text" data-answer="conference" class="input-blank mx-1 w-[120px]">. As you know, the Grand Falls Bridge <input type="text" data-answer="improvement" class="input-blank mx-1 w-[120px]"> work has been <input type="text" data-answer="underway" class="input-blank mx-1 w-[120px]"> for almost a year.'},
        {'speaker': 'W-Br', 'text': 'I know the fishing community has expressed concern over the potential <input type="text" data-answer="environmental" class="input-blank mx-1 w-[140px]"> impact of this project. Well, all required studies were <input type="text" data-answer="conducted" class="input-blank mx-1 w-[120px]"> a year ago.'},
        {'speaker': 'W-Br', 'text': 'After that, our special-events coordinator will discuss the bridge-opening <input type="text" data-answer="ceremony" class="input-blank mx-1 w-[120px]"> that’s being planned.'}
    ],
    'explanations': [
        {
            'num': '83', 'question': 'What is the speech mainly about?', 'question_vi': 'Bài phát biểu chủ yếu về điều gì?',
            'options': {'A': 'A financial report', 'B': 'A round of promotions', 'C': 'A product prototype', 'D': 'A construction project'},
            'options_vi': {'A': 'Một báo cáo tài chính', 'B': 'Một đợt thăng chức', 'C': 'Một nguyên mẫu sản phẩm', 'D': 'Một dự án xây dựng'},
            'ans': 'D', 'explanation': 'Người nói đang nói về "Grand Falls Bridge improvement work" (công việc cải tạo Cầu Grand Falls). Đây là một dự án xây dựng. Đáp án là D.'
        },
        {
            'num': '84', 'question': 'Why does the speaker say, “all required studies were conducted a year ago”?', 'question_vi': 'Tại sao người nói lại nói: "tất cả các nghiên cứu cần thiết đã được thực hiện cách đây một năm"?',
            'options': {'A': 'To correct a timeline error', 'B': 'To provide reassurance', 'C': 'To deny responsibility for a problem', 'D': 'To argue that a new study is needed'},
            'options_vi': {'A': 'Để sửa một lỗi về mốc thời gian', 'B': 'Để trấn an', 'C': 'Để phủ nhận trách nhiệm về một vấn đề', 'D': 'Để lập luận rằng một nghiên cứu mới là cần thiết'},
            'ans': 'B', 'explanation': 'Trước đó, người nói đề cập đến sự lo ngại về tác động môi trường từ phía cộng đồng đánh cá. Câu nói này nhằm khẳng định các nghiên cứu đã được làm để trấn an họ rằng vấn đề môi trường đã được xem xét. Đáp án là B.'
        },
        {
            'num': '85', 'question': 'What will the next speaker discuss?', 'question_vi': 'Người nói tiếp theo sẽ thảo luận về điều gì?',
            'options': {'A': 'A job fair', 'B': 'A school opening', 'C': 'A ceremony', 'D': 'A sporting event'},
            'options_vi': {'A': 'Một hội chợ việc làm', 'B': 'Một buổi khai giảng trường học', 'C': 'Một buổi lễ', 'D': 'Một sự kiện thể thao'},
            'ans': 'C', 'explanation': 'Người nói cho biết người tiếp theo sẽ thảo luận về "bridge-opening ceremony" (lễ khánh thành cầu). Đáp án là C.'
        }
    ]
}

# Data for 86-88
content_86_88 = {
    'shadowing': [
        {'speaker': 'W-Am', 'en': "Hello, Mr. Smith. / I hope you’re getting settled / into your office space / in our building. / I’m calling / about some large packages / that arrived for your company / last week.", 'vi': "Xin chào, ông Smith. / Tôi hy vọng ông đang dần ổn định / trong không gian văn phòng của mình / tại tòa nhà của chúng tôi. / Tôi gọi điện / về một số kiện hàng lớn / đã được gửi đến cho công ty ông / vào tuần trước."},
        {'speaker': 'W-Am', 'en': "We're keeping them for you / in the storage room downstairs. / The lease agreement says / management will hold packages / for five days. / It's been ten days.", 'vi': "Chúng tôi đang giữ chúng cho ông / trong kho ở tầng dưới. / Hợp đồng thuê nhà quy định rằng / ban quản lý sẽ giữ các kiện hàng / trong năm ngày. / Nhưng hiện tại đã được mười ngày rồi."},
        {'speaker': 'W-Am', 'en': "Please give me a call / and let me know / when you can come down / to claim them / so I can be there / to open the storage room door / for you.", 'vi': "Vui lòng gọi lại cho tôi / và cho tôi biết / khi nào ông có thể xuống / để nhận chúng / để tôi có thể ở đó / mở cửa phòng kho / cho ông."}
    ],
    'focus': [
        {'chunk': 'office space in our building', 'vi': 'không gian văn phòng trong tòa nhà chúng tôi', 'paraphrase': 'A building manager', 'q_num': '86'},
        {'chunk': 'large packages', 'vi': 'các kiện hàng lớn'},
        {'chunk': 'storage room downstairs', 'vi': 'phòng kho ở tầng dưới'},
        {'chunk': 'lease agreement', 'vi': 'hợp đồng thuê nhà'},
        {'chunk': 'It\'s been ten days', 'vi': 'đã mười ngày trôi qua', 'paraphrase': 'To point out a problem', 'q_num': '87'},
        {'chunk': 'open the storage room door', 'vi': 'mở cửa phòng kho', 'paraphrase': 'Open the door to a room', 'q_num': '88'}
    ],
    'word_bank': ['settled', 'packages', 'storage', 'management', 'agreement', 'claim'],
    'filling': [
        {'speaker': 'W-Am', 'text': 'Hello, Mr. Smith. I hope you’re getting <input type="text" data-answer="settled" class="input-blank mx-1 w-[100px]"> into your office space in our building. I’m calling about some large <input type="text" data-answer="packages" class="input-blank mx-1 w-[120px]"> that arrived for your company last week.'},
        {'speaker': 'W-Am', 'text': 'We\'re keeping them for you in the <input type="text" data-answer="storage" class="input-blank mx-1 w-[100px]"> room downstairs. The lease <input type="text" data-answer="agreement" class="input-blank mx-1 w-[120px]"> says <input type="text" data-answer="management" class="input-blank mx-1 w-[120px]"> will hold packages for five days.'},
        {'speaker': 'W-Am', 'text': 'Please give me a call and let me know when you can come down to <input type="text" data-answer="claim" class="input-blank mx-1 w-[100px]"> them.'}
    ],
    'explanations': [
        {
            'num': '86', 'question': 'Who most likely is the speaker?', 'question_vi': 'Người nói có khả năng nhất là ai?',
            'options': {'A': 'A salesperson', 'B': 'A government official', 'C': 'An interior designer', 'D': 'A building manager'},
            'options_vi': {'A': 'Một người bán hàng', 'B': 'Một quan chức chính phủ', 'C': 'Một nhà thiết kế nội thất', 'D': 'Một người quản lý tòa nhà'},
            'ans': 'D', 'explanation': 'Người nói nhắc đến "our building" (tòa nhà của chúng tôi), "lease agreement" (hợp đồng thuê) và "management" (ban quản lý). Điều này chỉ ra bà ấy là người quản lý tòa nhà. Đáp án là D.'
        },
        {
            'num': '87', 'question': 'Why does the speaker say, “It’s been ten days”?', 'question_vi': 'Tại sao người nói lại nói: "Đã mười ngày rồi"?',
            'options': {'A': 'To explain an expense', 'B': 'To point out a problem', 'C': 'To make an offer', 'D': 'To thank a colleague'},
            'options_vi': {'A': 'Để giải thích một khoản chi phí', 'B': 'Để chỉ ra một vấn đề', 'C': 'Để đưa ra một lời đề nghị', 'D': 'Để cảm ơn một đồng nghiệp'},
            'ans': 'B', 'explanation': 'Bà ấy nói quy định chỉ giữ hàng 5 ngày nhưng hàng đã ở đó 10 ngày. Câu nói này nhằm chỉ ra vấn đề rằng các kiện hàng đã quá hạn lưu kho. Đáp án là B.'
        },
        {
            'num': '88', 'question': 'What does the speaker offer to do?', 'question_vi': 'Người nói đề nghị làm gì?',
            'options': {'A': 'Open the door to a room', 'B': 'Reset a password', 'C': 'Send a copy of a document', 'D': 'Refund a payment'},
            'options_vi': {'A': 'Mở cửa một căn phòng', 'B': 'Đặt lại mật khẩu', 'C': 'Gửi một bản sao tài liệu', 'D': 'Hoàn trả một khoản thanh toán'},
            'ans': 'A', 'explanation': 'Bà ấy nói: "I can be there to open the storage room door for you" (tôi có thể ở đó để mở cửa phòng kho cho ông). Đáp án là A.'
        }
    ]
}

# Data for 89-91
content_89_91 = {
    'shadowing': [
        {'speaker': 'M-Au', 'en': "Our next story / concerns Ferndale Valley. / It’s well-known / that the area / is one of the windiest locations / in the region, / and one company / would like to take advantage / of that natural energy source.", 'vi': "Câu chuyện tiếp theo của chúng tôi / liên quan đến Thung lũng Ferndale. / Ai cũng biết rằng / khu vực này / là một trong những địa điểm lộng gió nhất / trong vùng, / và một công ty / muốn tận dụng / nguồn năng lượng tự nhiên đó."},
        {'speaker': 'M-Au', 'en': "Breeze Capture / hopes to install / dozens of wind turbines / by the end of next year. / The company is looking / for local farmers / who are interested / in leasing some of their land / for the project.", 'vi': "Công ty Breeze Capture / hy vọng sẽ lắp đặt / hàng tá tua-bin gió / vào cuối năm tới. / Công ty đang tìm kiếm / những người nông dân địa phương / quan tâm đến việc / cho thuê một phần đất của họ / cho dự án."},
        {'speaker': 'M-Au', 'en': "In addition / to being paid / for the land use, / participants / will also be compensated / for the energy / that is generated / by the turbines.", 'vi': "Ngoài việc / được trả tiền / cho việc sử dụng đất, / những người tham gia / cũng sẽ được đền bù / cho nguồn năng lượng / được tạo ra / bởi các tua-bin."}
    ],
    'focus': [
        {'chunk': 'one of the windiest locations', 'vi': 'một trong những nơi lộng gió nhất', 'paraphrase': 'It is very windy', 'q_num': '89'},
        {'chunk': 'take advantage of natural energy', 'vi': 'tận dụng năng lượng tự nhiên'},
        {'chunk': 'wind turbines', 'vi': 'tua-bin gió'},
        {'chunk': 'local farmers', 'vi': 'nông dân địa phương', 'paraphrase': 'Farmers', 'q_num': '90'},
        {'chunk': 'leasing some of their land', 'vi': 'cho thuê một phần đất'},
        {'chunk': 'compensated for the energy', 'vi': 'được đền bù/trả phí cho năng lượng', 'paraphrase': 'Financial compensation', 'q_num': '91'}
    ],
    'word_bank': ['concerns', 'locations', 'advantage', 'turbines', 'leasing', 'compensated'],
    'filling': [
        {'speaker': 'M-Au', 'text': 'Our next story <input type="text" data-answer="concerns" class="input-blank mx-1 w-[100px]"> Ferndale Valley. It’s well-known that the area is one of the windiest <input type="text" data-answer="locations" class="input-blank mx-1 w-[100px]"> in the region.'},
        {'speaker': 'M-Au', 'text': 'Breeze Capture hopes to install dozens of wind <input type="text" data-answer="turbines" class="input-blank mx-1 w-[100px]"> by the end of next year. The company is looking for local farmers who are interested in <input type="text" data-answer="leasing" class="input-blank mx-1 w-[100px]"> some of their land.'},
        {'speaker': 'M-Au', 'text': 'In addition to being paid for the land use, participants will also be <input type="text" data-answer="compensated" class="input-blank mx-1 w-[140px]"> for the energy.'}
    ],
    'explanations': [
        {
            'num': '89', 'question': 'What is mentioned about Ferndale Valley?', 'question_vi': 'Điều gì được nhắc đến về Thung lũng Ferndale?',
            'options': {'A': 'It is heavily forested.', 'B': 'It attracts many tourists.', 'C': 'It is developing quickly.', 'D': 'It is very windy.'},
            'options_vi': {'A': 'Nó có rừng rậm bao phủ.', 'B': 'Nó thu hút nhiều khách du lịch.', 'C': 'Nó đang phát triển nhanh chóng.', 'D': 'Nó rất lộng gió.'},
            'ans': 'D', 'explanation': 'Người nói cho biết: "the area is one of the windiest locations in the region" (khu vực này là một trong những địa điểm lộng gió nhất trong vùng). Đáp án là D.'
        },
        {
            'num': '90', 'question': 'Who will participate in a project?', 'question_vi': 'Ai sẽ tham gia vào dự án?',
            'options': {'A': 'Biologists', 'B': 'Farmers', 'C': 'Airline pilots', 'D': 'Real estate agents'},
            'options_vi': {'A': 'Các nhà sinh vật học', 'B': 'Những người nông dân', 'C': 'Các phi công hàng không', 'D': 'Các đại lý bất động sản'},
            'ans': 'B', 'explanation': 'Người nói cho biết công ty đang tìm kiếm "local farmers who are interested in leasing some of their land" (các nông dân địa phương quan tâm đến việc cho thuê đất). Đáp án là B.'
        },
        {
            'num': '91', 'question': 'What will the participants receive?', 'question_vi': 'Những người tham gia sẽ nhận được gì?',
            'options': {'A': 'Tickets to an industry event', 'B': 'Technical assistance', 'C': 'Financial compensation', 'D': 'Advertising advice'},
            'options_vi': {'A': 'Vé tham dự một sự kiện trong ngành', 'B': 'Hỗ trợ kỹ thuật', 'C': 'Bồi thường/đền bù tài chính', 'D': 'Lời khuyên về quảng cáo'},
            'ans': 'C', 'explanation': 'Người nói cho biết những người tham gia sẽ "be paid for the land use" và "be compensated for the energy" (được trả tiền thuê đất và đền bù cho năng lượng). Đây là các hình thức đền bù tài chính. Đáp án là C.'
        }
    ]
}

# Data for 92-94
content_92_94 = {
    'shadowing': [
        {'speaker': 'M-Cn', 'en': "Hello, Mr. Kimura. / l'm calling / from Feras Portable Storage. / You recently ordered / a container / to store and move / your household belongings in.", 'vi': "Xin chào, ông Kimura. / Tôi gọi điện / từ Feras Portable Storage. / Gần đây ông đã đặt / một thùng chứa / để lưu trữ và vận chuyển / đồ dùng gia đình của mình."},
        {'speaker': 'M-Cn', 'en': "I'm calling to confirm / that your container / will be delivered tomorrow morning / at nine o'clock. / The driver / will place it / in your driveway.", 'vi': "Tôi gọi điện để xác nhận rằng / thùng chứa của ông / sẽ được giao vào sáng mai / lúc chín giờ. / Tài xế / sẽ đặt nó / ở lối vào ga-ra của ông."},
        {'speaker': 'M-Cn', 'en': "After the delivery, / if you could, / please complete / the customer feedback survey / that we'll e-mail you. / It will help us / to improve our service. Thanks.", 'vi': "Sau khi giao hàng, / nếu ông có thể, / vui lòng hoàn thành / bản khảo sát ý kiến khách hàng / mà chúng tôi sẽ gửi e-mail cho ông. / Nó sẽ giúp chúng tôi / cải thiện dịch vụ của mình. Cảm ơn ông."}
    ],
    'focus': [
        {'chunk': 'Feras Portable Storage', 'vi': 'Tên công ty lưu trữ di động', 'paraphrase': 'A storage company', 'q_num': '92'},
        {'chunk': 'store and move household belongings', 'vi': 'lưu trữ và vận chuyển đồ đạc gia đình'},
        {'chunk': 'delivered tomorrow morning', 'vi': 'giao vào sáng mai', 'paraphrase': 'To confirm a delivery', 'q_num': '93'},
        {'chunk': 'driveway', 'vi': 'lối vào ga-ra/đường lái xe vào nhà'},
        {'chunk': 'customer feedback survey', 'vi': 'khảo sát ý kiến khách hàng', 'paraphrase': 'Complete a survey', 'q_num': '94'},
        {'chunk': 'improve our service', 'vi': 'cải thiện dịch vụ của chúng tôi'}
    ],
    'word_bank': ['portable', 'belongings', 'confirm', 'delivered', 'driveway', 'survey'],
    'filling': [
        {'speaker': 'M-Cn', 'text': 'Hello, Mr. Kimura. l\'m calling from Feras <input type="text" data-answer="portable" class="input-blank mx-1 w-[100px]"> Storage. You recently ordered a container to store and move your household <input type="text" data-answer="belongings" class="input-blank mx-1 w-[120px]"> in.'},
        {'speaker': 'M-Cn', 'text': 'I\'m calling to <input type="text" data-answer="confirm" class="input-blank mx-1 w-[100px]"> that your container will be <input type="text" data-answer="delivered" class="input-blank mx-1 w-[120px]"> tomorrow morning. The driver will place it in your <input type="text" data-answer="driveway" class="input-blank mx-1 w-[120px]">.'},
        {'speaker': 'M-Cn', 'text': 'After the delivery, please complete the customer feedback <input type="text" data-answer="survey" class="input-blank mx-1 w-[100px]"> that we\'ll e-mail you.'}
    ],
    'explanations': [
        {
            'num': '92', 'question': 'What kind of business does the speaker work for?', 'question_vi': 'Người nói làm việc cho loại hình kinh doanh nào?',
            'options': {'A': 'A construction firm', 'B': 'A landscaping service', 'C': 'A storage company', 'D': 'An auto repair shop'},
            'options_vi': {'A': 'Một công ty xây dựng', 'B': 'Một dịch vụ cảnh quan', 'C': 'Một công ty kho bãi/lưu trữ', 'D': 'Một tiệm sửa xe'},
            'ans': 'C', 'explanation': 'Người nói cho biết ông gọi từ "Feras Portable Storage". Đây là một công ty về kho bãi và lưu trữ. Đáp án là C.'
        },
        {
            'num': '93', 'question': 'Why is the speaker calling?', 'question_vi': 'Tại sao người nói lại gọi điện?',
            'options': {'A': 'To apologize for a cancellation', 'B': 'To confirm a delivery', 'C': 'To share a price quote', 'D': 'To update some contact information'},
            'options_vi': {'A': 'Để xin lỗi vì một sự hủy bỏ', 'B': 'Để xác nhận việc giao hàng', 'C': 'Để chia sẻ một báo giá', 'D': 'Để cập nhật một số thông tin liên lạc'},
            'ans': 'B', 'explanation': 'Người nói cho biết: "I\'m calling to confirm that your container will be delivered tomorrow morning" (Tôi gọi để xác nhận rằng thùng chứa của ông sẽ được giao vào sáng mai). Đáp án là B.'
        },
        {
            'num': '94', 'question': 'What does the speaker ask the listener to do?', 'question_vi': 'Người nói yêu cầu người nghe làm gì?',
            'options': {'A': 'Purchase a warranty', 'B': 'Complete a survey', 'C': 'Clean up an area', 'D': 'Apply for a permit'},
            'options_vi': {'A': 'Mua bảo hành', 'B': 'Hoàn thành một bản khảo sát', 'C': 'Dọn dẹp một khu vực', 'D': 'Xin giấy phép'},
            'ans': 'B', 'explanation': 'Người nói yêu cầu: "please complete the customer feedback survey" (vui lòng hoàn thành bản khảo sát phản hồi của khách hàng). Đáp án là B.'
        }
    ]
}

update_html('Test 5/LC-T5-P4-Q83-85.html', content_83_85)
update_html('Test 5/LC-T5-P4-Q86-88.html', content_86_88)
update_html('Test 5/LC-T5-P4-Q89-91.html', content_89_91)
update_html('Test 5/LC-T5-P4-Q92-94.html', content_92_94)

