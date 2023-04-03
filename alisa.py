import random

import founder


class Alisa:
    def __init__(self, request, response):
        self.event, self.answer, self.response = request, response["response"], response
        self.intents = self.event.get("request", {}).get("nlu", {}).get("intents", {})
        self.command = self.event.get("request", {}).get("command", {})
        self.state_session = self.event.get("state", {}).get("session", {})
        self.application_state = self.event.get("state", {}).get("application", {})
        self.user_state = self.event.get("state", {}).get("user", {})
        self.original_utterance = self.event.get("request", {}).get(
            "original_utterance"
        )

    def is_new_session(self):
        return self.event["session"]["new"]

    def get_state(self):
        return self.event["state"]

    def get_original_utterance(self):
        return self.original_utterance

    def add_to_session_state(self, key, value):
        self.response["session_state"] = self.response.get("session_state", {})
        self.response["session_state"][key] = value

    def end_session(self):
        self.answer["end_session"] = True

    def suggest(self, title, url=None, payload=None):
        if payload is None:
            payload = {}
        self.button(title, True, url, payload)

    def button(self, title, hide=False, url=None, payload=None):
        if payload is None:
            payload = {}
        self.answer["buttons"] = self.answer.get("buttons", [])
        button = {"title": title, "payload": payload, "hide": hide}
        if url:
            button["url"] = url
        self.answer["buttons"].append(button)

    def get_button_payload_value(self, value):
        return self.event.get("request", {}).get("payload", {}).get(value, {})

    def text(self, tts):
        self.answer["text"] = self.answer.get("text", "") + tts

    def tts(self, tts):
        self.answer["tts"] = self.answer.get("tts", "") + tts

    def tts_with_text(self, tts):
        self.answer["text"] = self.answer.get("text", "") + tts
        self.answer["tts"] = self.answer.get("tts", "") + tts

    def has_intent(self, intent):
        return self.intents.get(intent)


class Dialog:
    def __init__(self):
        pass

    def handle_dialog(self, alisa):
        if alisa.is_new_session():
            return self.greetings(alisa)

        if alisa.has_intent("YANDEX.HELP"):
            return self.help(alisa)

        if alisa.has_intent("YANDEX.WHAT_CAN_YOU_DO"):
            return self.what_you_can_do(alisa)

        # Формат ссылки на маршрут: https://yandex.ru/maps/?mode=routes&rtext=широта(от)%2Cдолгота(от)~широта(до)%2Cдолгота(до)
        if alisa.get_button_payload_value("type") == "restart":
            return self.greetings(alisa)

        if alisa.get_state().get("session", {}).get("stage") == 2:
            alisa.add_to_session_state("city", str(alisa.get_original_utterance()))
            alisa.suggest("Госпиталь", payload={"type": 1})
            alisa.suggest("Народный фронт", payload={"type": 2})
            alisa.suggest("Пункт расселения беженцев", payload={"type": 3})
            alisa.suggest("Назад", payload={"type": "restart"})
            alisa.text(
                f"Ваш город: {str(alisa.get_original_utterance())} \n"
                f"Выберите необходимое место: Госпиталь, Народный фронт, Пункт расселения беженцев или Бомбоубежища. \n"
                f"Если выбран неправильный город, скажите: Назад"
            )
            alisa.add_to_session_state("stage", 3)

        if alisa.get_state().get("session", {}).get("stage") == 3:
            city = str(alisa.get_state().get("session", {}).get("city"))
            if alisa.get_button_payload_value("type") == 1 or alisa.has_intent(
                "hospital"
            ):
                coords, address = founder.get_hospital(city)
                if coords == "error":
                    alisa.add_to_session_state("stage", 2)
                    return alisa.tts_with_text(
                        "Ошибка поиска, попробуйте выбрать город ещё раз"
                    )
                city_coords = founder.get_city_coords(city)
                alisa.suggest(
                    "Маршрут",
                    url=f"https://yandex.ru/maps/?mode=routes&rtext={city_coords[0]}%2C{city_coords[1]}~{coords[1]}%2C{coords[0]}",
                )
                return alisa.tts_with_text(
                    f"Адрес ближайшего к центру вашего города госпиталя: {address}."
                )
            if alisa.get_button_payload_value("type") == 2 or alisa.has_intent("front"):
                coords, address = founder.front(city)
                city_coords = founder.get_city_coords(city)
                alisa.suggest(
                    "Маршрут",
                    url=f"https://yandex.ru/maps/?mode=routes&rtext={city_coords[0]}%2C{city_coords[1]}~{coords[1]}%2C{coords[0]}",
                )
                return alisa.tts_with_text(
                    f"Адрес ближайшего к центру вашего города народного фронта: {address}."
                )
            if alisa.get_button_payload_value("type") == 3 or alisa.has_intent(
                "bezenec"
            ):
                coords, address = founder.bezhenc(city)
                city_coords = founder.get_city_coords(city)
                alisa.suggest(
                    "Маршрут",
                    url=f"https://yandex.ru/maps/?mode=routes&rtext={city_coords[0]}%2C{city_coords[1]}~{coords[1]}%2C{coords[0]}",
                )
                return alisa.tts_with_text(
                    f"Адрес ближайшего к центру вашего города пункта расселения беженцев: {address}."
                )
            else:
                alisa.add_to_session_state("stage", 2)
                return alisa.tts_with_text("Я вас не поняла, введите город ещё раз")

        # else:
        #     alisa.end_session()

    def greetings(self, alisa: Alisa):
        alisa.tts_with_text(
            "Я  - Рука помощи! Моя задача заключается  бомбоубежищ, а также пунктов гуманитарной помощи.\nДля начала работы навыка скажите название вашего города"
        )
        alisa.add_to_session_state("stage", 2)

    def random_help(self):
        texts = [
            "В связи актуальными событиями, был создан я - навык под названием Рука помощи. "
            "Главная моя задача при использовании - помочь найти вам нужное строении в одной из 3-х категорий. "
            "Это госпитали, народные фронты, а также пункты расселения беженцев. ",
            "В последнее время в мире происходят разные вещи. И не всегда они несут добро, отчего многие начали искать себе убежище."
            "Данный навык был создан для облегчения поиска безопасного места. "
            "Я могу искать такие места, как госпитали, народные фронты, а также пункты расселения беженцев. ",
            "На данный момент, обстановка в мире немного накалилась, поэтому для сохранения жизни нужно найти безопасное и крепкое место. "
            "Как раз в этом и заключается моя задача. Я могу искать такие места, как госпитали, народные фронты, а также пункты расселения беженцев. "
            "В эти категории входят: госпитали, бомбоубежища, общежития, пункты с гуманитарной помощью",
        ]

        return random.choice(texts)

    def help(self, alisa):
        alisa.tts_with_text(self.random_help())

    def what_you_can_do(self, alisa):
        alisa.tts_with_text(self.random_help())
