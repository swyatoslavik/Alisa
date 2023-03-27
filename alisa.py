import random


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

        # Формат ссылки на маршрут: https://yandex.ru/maps/39/rostov-na-donu/?mode=routes&rtext=широта(от)%2Cдолгота(от)~широта(до)%2Cдолгота(до)
        # Я сейчас сижу в 2 часа ночи и ни хуя не вдупляю, почему между координатами %2C понять не смогу
        # Максимально сокращаю просто делая вид, что у нас готово что-то, на самом деле я просто вставляю готовый текст

        if alisa.get_state().get("session", {}).get("stage") == 2:
            if alisa.get_button_payload_value("type") == 1:
                alisa.suggest(
                    "Маршрут",
                    url="https://yandex.ru/maps/39/rostov-na-donu/?mode=routes&rtext=47.228369%2C39.714788~47.220303%2C39.720510",
                )
                return alisa.text(
                    "Поскольку это тестовая версия, я выбрала ваше место вместо вас - Ростов-на-Дону\n"
                    "Ближайший к вам центр гуманитарной помощи находится по адресу Ворошиловский проспект, 12/85."
                )
            if alisa.get_button_payload_value("type") == 2:
                alisa.suggest(
                    "Маршрут",
                    url="https://yandex.ru/maps/39/rostov-na-donu/?mode=routes&rtext=47.228369%2C39.714788~47.219477%2C39.717914",
                )
                return alisa.text(
                    "Поскольку это тестовая версия, я выбрала ваше место вместо вас - Ростов-на-Дону\n"
                    "Ближайший к вам центр госпиталь находится по адресу ул. Московская, 77."
                )
            if alisa.get_button_payload_value("type") == 3:
                alisa.suggest(
                    "Маршрут",
                    url="https://yandex.ru/maps/39/rostov-na-donu/?mode=routes&rtext=47.228369%2C39.714788~46.098711%2C47.735666",
                )
                return alisa.text(
                    "Поскольку это тестовая версия, я выбрала ваше место вместо вас - Ростов-на-Дону\n"
                    "Ближайший к вам центр гуманитарной помощи находится по адресу Икряное, 1 Мая ул, 19"
                )

        else:
            alisa.end_session()

    def greetings(self, alisa: Alisa):
        alisa.tts_with_text(
            "Я  - Рука помощи! Моя задача заключается  бомбоубежищ, а также пунктов гуманитарной помощи.\nДля начала работы навыка нужно выбрать тип помощи кнопками ниже\n\n(pre-alpha)"
        )
        alisa.suggest("Найди центр гуманитарной помощи", payload={"type": 1})
        alisa.suggest("Найди госпиталь", payload={"type": 2})
        alisa.suggest("Найди место временного размещения", payload={"type": 3})
        alisa.add_to_session_state("stage", 2)

    def random_help(self):
        texts = [
            "Скоро здесь будет текст для помощи, и даже несколько (1/3)",
            "Скоро здесь будет текст для помощи, и даже несколько (2/3)",
            "Скоро здесь будет текст для помощи, и даже несколько (3/3)",
        ]

        return random.choice(texts)

    def help(self, alisa):
        alisa.tts_with_text(self.random_help())

    def what_you_can_do(self, alisa):
        alisa.tts_with_text(self.random_help())
