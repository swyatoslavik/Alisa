from flask import Flask, request
from alisa import Dialog, Alisa
import json


class StartDialog(Dialog):
    def handle_dialog(self, alisa):
        if alisa.is_new_session():
            return self.greetings(alisa)

        if alisa.has_intent("YANDEX.HELP"):
            return self.help(alisa)

        if alisa.has_intent("YANDEX.WHAT_CAN_YOU_DO"):
            return self.what_you_can_do(alisa)


app = Flask(__name__)
dialog = StartDialog()


@app.route("/alice", methods=["POST"])
def resp():
    text = request.json.get("request", {}).get("command")
    response = {"response": {"end_session": True}, "version": "1.0"}

    dialog.handle_dialog(Alisa(request.json, response))

    return json.dumps(response, ensure_ascii=False, indent=2)


app.run(threaded=True, debug=True)
