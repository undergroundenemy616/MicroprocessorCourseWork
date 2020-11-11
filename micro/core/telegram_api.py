import json
import logging

import requests
from django.utils.translation import gettext as _

from micro import settings

logger = logging.getLogger(__name__)


def invoke_telegram(method, **kwargs):
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/{method}"
    # logger.info(f"Requesting {url} {kwargs}")
    resp = requests.post(url, data=kwargs, timeout=(3.05, 27))
    # logger.info(f"Response {resp.status_code} {resp.content}")
    return resp


def make_inline_keyboard():
    return {'inline_keyboard': []}


def add_button_to_ik(keyboard, name, field, data):
    button_row = [{'text': _(name),
                   field: data}]
    keyboard['inline_keyboard'].append(button_row)
    return keyboard


def make_task_switch_keyboard():
    keyboard = make_inline_keyboard()
    keyboard_data = {'on': _('On'),
                     'off': _('Off')}

    for action, name in keyboard_data.items():
        keyboard = add_button_to_ik(keyboard, name, 'callback_data', action)
    return keyboard


def hide_keyboard_by_chat_msg(chat_id, msg_id):
    keyboard = make_inline_keyboard()
    res = invoke_telegram('editMessageReplyMarkup', chat_id=chat_id, message_id=msg_id, reply_markup=json.dumps(keyboard))
    return res


def delete_messages(chat_id, msg_id):
    res = invoke_telegram('deleteMessage', chat_id=chat_id, message_id=msg_id)
    return res
