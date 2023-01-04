from typing import Any, Text, Dict, List

from rasa_sdk.events import SlotSet
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


if not firebase_admin._apps:
    cred = credentials.Certificate(
        '../actions/rasabooks-1b511-firebase-adminsdk-66sy6-b3ddb5738e.json')
    default_app = firebase_admin.initialize_app(cred)

db = firestore.client()


def get_theloai():
    docs = db.collection(u'dstheloai').stream()
    dstheloai = []
    for doc in docs:
        dstheloai.append(doc.to_dict())
    return dstheloai


def get_ttbooks():
    docs = db.collection(u'ttbooks').stream()
    ttbooks = []
    for doc in docs:
        ttbooks.append(doc.to_dict())
    return ttbooks


def get_shipcost():
    docs = db.collection(u'vanchuyen').stream()
    ttbooks = []
    for doc in docs:
        ttbooks.append(doc.to_dict())
    return ttbooks


allbooks = get_ttbooks()
allcates = get_theloai()
allcostships = get_shipcost()


class ActionGetcostship(Action):

    def name(self) -> Text:
        return "action_cost_ship"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        ten_tinh = tracker.get_slot("ten_tinh")
        if not ten_tinh:
            dispatcher.utter_message(text="Xin lỗi tôi không biết")
        else:
            findtinh = ""
            cost = ""
            for ttinh in allcostships:
                if ttinh["tentinh"] == ten_tinh.lower():
                    findtinh = ttinh["tentinh"].title()
                    cost = ttinh["phi"]
            if findtinh == "":
                dispatcher.utter_message(
                    text="Phí vận chuyển cho các tỉnh từ 1->3$")
            else:
                dispatcher.utter_message(
                    text=f"Phí vận chuyển đến tỉnh {findtinh} là {cost}")
        return []


class ActionSayWithName(Action):

    def name(self) -> Text:
        return "action_say_with_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        cust_name = tracker.get_slot("cust_name")
        in_cust_name = cust_name.title()
        if not cust_name:
            dispatcher.utter_message(text="Xin lỗi tôi không biết")
        else:
            dispatcher.utter_message(
                text=f"Chào {in_cust_name}! Tôi giúp gì được cho bạn?")
        return []


class ActionCategories(Action):

    def name(self) -> Text:
        return "action_categories"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        index = 1
        firsttheloai = "Hiện tại thư viện chúng tôi có các thể loại"
        dispatcher.utter_message(text=firsttheloai)
        for ttheloai in allcates:
            dispatcher.utter_message(text=f"{index}. {ttheloai['tentheloai']}")
            index += 1
        dispatcher.utter_message(text="Bạn thích đọc sách thuộc thể loại nào?")
        return []


class ActionGetbookHistory(Action):

    def name(self) -> Text:
        return "action_book_history"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        bookHIs = []
        for tbook in allbooks:
            if(tbook["theloai"] == "lịch sử"):
                bookHIs.append(tbook)

        message = {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [
                    {
                        "title": bookHIs[0]["tensach"],
                        "subtitle": bookHIs[0]["theloai"],
                        "image_url": bookHIs[0]["hinhanh"],
                        "buttons": [
                            {
                                "title": bookHIs[0]["tacgia"],
                                "url": "https://en.wikipedia.org/wiki/Zecharia_Sitchin",
                                "type": "web_url"
                            }
                        ]
                    },
                    {
                        "title": bookHIs[1]["tensach"],
                        "subtitle": bookHIs[1]["theloai"],
                        "image_url": bookHIs[1]["hinhanh"],
                        "buttons": [
                            {
                                "title": bookHIs[1]["tacgia"],
                                "url": "https://en.wikipedia.org/wiki/Aldon_Morris",
                                "type": "web_url"
                            }
                        ]
                    },
                    {
                        "title": bookHIs[2]["tensach"],
                        "subtitle": bookHIs[2]["theloai"],
                        "image_url": bookHIs[2]["hinhanh"],
                        "buttons": [
                            {
                                "title": bookHIs[2]["tacgia"],
                                "url": "https://en.wikipedia.org/wiki/Simon_Winchester",
                                "type": "web_url"
                            }
                        ]
                    }
                ]
            }
        }
        dispatcher.utter_message(
            text="Một vài quyển sách lịch sử bạn có thể tham khảo")
        dispatcher.utter_message(attachment=message)

        return []


class ActionGetbookFiction(Action):

    def name(self) -> Text:
        return "action_book_fiction"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        bookFic = []
        for tbook in allbooks:
            if(tbook["theloai"] == "viễn tưởng"):
                bookFic.append(tbook)

        message = {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [
                    {
                        "title": bookFic[0]["tensach"],
                        "subtitle": bookFic[0]["theloai"],
                        "image_url": bookFic[0]["hinhanh"],
                        "buttons": [
                            {
                                "title": bookFic[0]["tacgia"],
                                "url": "https://en.wikipedia.org/wiki/Terry_Pratchett",
                                "type": "web_url"
                            }
                        ]
                    },
                    {
                        "title": bookFic[1]["tensach"],
                        "subtitle": bookFic[1]["theloai"],
                        "image_url": bookFic[1]["hinhanh"],
                        "buttons": [
                            {
                                "title": bookFic[1]["tacgia"],
                                "url": "https://vi.wikipedia.org/wiki/Meg_Cabot",
                                "type": "web_url"
                            }
                        ]
                    },
                    {
                        "title": bookFic[2]["tensach"],
                        "subtitle": bookFic[2]["theloai"],
                        "image_url": bookFic[2]["hinhanh"],
                        "buttons": [
                            {
                                "title": bookFic[2]["tacgia"],
                                "url": "https://en.wikipedia.org/wiki/Dan_Simmons",
                                "type": "web_url"
                            }
                        ]
                    }
                ]
            }
        }
        dispatcher.utter_message(
            text="Một vài quyển sách viễn tưởng bạn có thể tham khảo")
        dispatcher.utter_message(attachment=message)

        return []


class ActionGetbookLiteraryCriticsm(Action):

    def name(self) -> Text:
        return "action_book_LiteraryCriticsm"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        bookLite = []
        for tbook in get_ttbooks():
            if(tbook["theloai"] == "phê bình văn học"):
                bookLite.append(tbook)

        message = {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [
                    {
                        "title": bookLite[0]["tensach"],
                        "subtitle": bookLite[0]["theloai"],
                        "image_url": bookLite[0]["hinhanh"],
                        "buttons": [
                            {
                                "title": bookLite[0]["tacgia"],
                                "url": "https://en.wikipedia.org/wiki/Nicholas_A._Basbanes",
                                "type": "web_url"
                            }
                        ]
                    },
                    {
                        "title": bookLite[1]["tensach"],
                        "subtitle": bookLite[1]["theloai"],
                        "image_url": bookLite[1]["hinhanh"],
                        "buttons": [
                            {
                                "title": bookLite[1]["tacgia"],
                                "url": "https://en.wikipedia.org/wiki/Mark_Twain",
                                "type": "web_url"
                            }
                        ]
                    },
                    {
                        "title": bookLite[2]["tensach"],
                        "subtitle": bookLite[2]["theloai"],
                        "image_url": bookLite[2]["hinhanh"],
                        "buttons": [
                            {
                                "title": bookLite[2]["tacgia"],
                                "url": "https://en.wikipedia.org/wiki/Friedrich_Nietzsche",
                                "type": "web_url"
                            }
                        ]
                    }
                ]
            }
        }
        dispatcher.utter_message(
            text="Sách phê bình văn học bạn có thể tham khảo")
        dispatcher.utter_message(attachment=message)

        return []


class ActionGetbookBiographyAutobiography(Action):

    def name(self) -> Text:
        return "action_book_BiographyAutobiography"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        bookBio = []
        for tbook in allbooks:
            if(tbook["theloai"] == "tiểu sử và tự truyện"):
                bookBio.append(tbook)

        message = {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [
                    {
                        "title": bookBio[0]["tensach"],
                        "subtitle": bookBio[0]["theloai"],
                        "image_url": bookBio[0]["hinhanh"],
                        "buttons": [
                            {
                                "title": bookBio[0]["tacgia"],
                                "url": "https://en.wikipedia.org/wiki/Neil_Strauss",
                                "type": "web_url"
                            }
                        ]
                    },
                    {
                        "title": bookBio[1]["tensach"],
                        "subtitle": bookBio[1]["theloai"],
                        "image_url": bookBio[1]["hinhanh"],
                        "buttons": [
                            {
                                "title": bookBio[1]["tacgia"],
                                "url": "https://en.wikipedia.org/wiki/Christopher_Hitchens",
                                "type": "web_url"
                            }
                        ]
                    },
                    {
                        "title": bookBio[2]["tensach"],
                        "subtitle": bookBio[2]["theloai"],
                        "image_url": bookBio[2]["hinhanh"],
                        "buttons": [
                            {
                                "title": bookBio[2]["tacgia"],
                                "url": "https://en.wikipedia.org/wiki/Sam_Weller_(character)",
                                "type": "web_url"
                            }
                        ]
                    }
                ]
            }
        }
        dispatcher.utter_message(
            text="Sách tiểu sử và tự truyện bạn có thể tham khảo")
        dispatcher.utter_message(attachment=message)

        return []


class ActionGetbookJuvenileFiction(Action):

    def name(self) -> Text:
        return "action_book_JuvenileFiction"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        bookJuv = []
        for tbook in allbooks:
            if(tbook["theloai"] == "tiểu thuyết vị thành niên"):
                bookJuv.append(tbook)

        message = {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [
                    {
                        "title": bookJuv[0]["tensach"],
                        "subtitle": bookJuv[0]["theloai"],
                        "image_url": bookJuv[0]["hinhanh"],
                        "buttons": [
                            {
                                "title": bookJuv[0]["tacgia"],
                                "url": "https://en.wikipedia.org/wiki/Terry_Pratchett",
                                "type": "web_url"
                            }
                        ]
                    },
                    {
                        "title": bookJuv[1]["tensach"],
                        "subtitle": bookJuv[1]["theloai"],
                        "image_url": bookJuv[1]["hinhanh"],
                        "buttons": [
                            {
                                "title": bookJuv[1]["tacgia"],
                                "url": "https://en.wikipedia.org/wiki/Peter_Abrahams",
                                "type": "web_url"
                            }
                        ]
                    },
                    {
                        "title": bookJuv[2]["tensach"],
                        "subtitle": bookJuv[2]["theloai"],
                        "image_url": bookJuv[2]["hinhanh"],
                        "buttons": [
                            {
                                "title": bookJuv[2]["tacgia"],
                                "url": "https://en.wikipedia.org/wiki/Sid_Fleischman",
                                "type": "web_url"
                            }
                        ]
                    }
                ]
            }
        }
        dispatcher.utter_message(
            text="Sách tiểu thuyết vị thành niên bạn có thể tham khảo")
        dispatcher.utter_message(attachment=message)

        return []


class Actionstartmuonsach(Action):

    def name(self) -> Text:
        return "action_start_muonsach"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(
            text="Đầu tiên bạn cần đăng ký tài khoản hệ thống và làm theo các bước")
        dispatcher.utter_message(
            text="Bước 1. Tìm kiếm quyển sách mà bạn muốn thuê (mượn)")
        dispatcher.utter_message(
            text="Bước 2. Xem thông tin sách -> Thêm vào giỏ")
        dispatcher.utter_message(
            text="Bước 3. Chọn giỏ hàng và tiến hành lập phiếu thuê sách")
        dispatcher.utter_message(
            text="Sau khi lập phiếu thuê bạn có thể xem lại ở trang cá nhân")

        return []

# class ActionFallback(Action):

#     def name(self) -> Text:
#         return "action_default_fallback"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(
#             text="Xin lỗi tôi không nhận được ý định của bạn!!!")

#         return [UserUtteranceReverted()]
