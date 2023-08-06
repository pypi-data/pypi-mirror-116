# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['vktools']
setup_kwargs = {
    'name': 'vktools',
    'version': '1.0.1',
    'description': 'https://github.com/Fsoky/vktools',
    'long_description': '# vktools\nTools for vk_api for comfort work\n\n![example imports](https://github.com/Fsoky/vktools/blob/main/images/Screenshot_0.png)\n\n![example keyboard](https://github.com/Fsoky/vktools/blob/main/images/Screenshot_1.png)\n\n![example code of keyboard](https://github.com/Fsoky/vktools/blob/main/images/Screenshot_2.png)\n\n![example carousel](https://github.com/Fsoky/vktools/blob/main/images/Screenshot_3.png)\n\n![example code of carousel](https://github.com/Fsoky/vktools/blob/main/images/Screenshot_4.png)\n\n## Example code\n```py\nimport vk_api\nfrom vk_api.longpoll import VkLongPoll, VkEventType\n\n\nfrom vktools import Keyboard, KeyboardButton, Carousel, CarouselButton\n\nvk = vk_api.VkApi(token="token")\n\n\ndef send_message(user_id, message, keyboard=None, carousel=None):\n\tvalues = {\n\t\t"user_id": user_id,\n\t\t"message": message,\n\t\t"random_id": 0\n\t}\n\n\tif keyboard is not None:\n\t\tvalues["keyboard"] = keyboard.add_keyboard()\n\tif carousel is not None:\n\t\tvalues["template"] = carousel.add_carousel()\n\n\tvk.method("messages.send", values)\n\nfor event in VkLongPoll(vk).listen():\n\tif event.type == VkEventType.MESSAGE_NEW and event.to_me:\n\t\ttext = event.text.lower()\n\t\tuser_id = event.user_id\n\n\t\tif text == "test":\n\t\t\tkeyboard = Keyboard(\n\t\t\t\t[\n\t\t\t\t\t[\n\t\t\t\t\t\tKeyboardButton().text("RED", "negative"),\n\t\t\t\t\t\tKeyboardButton().text("GREEN", "positive"),\n\t\t\t\t\t\tKeyboardButton().text("BLUE", "primary"),\n\t\t\t\t\t\tKeyboardButton().text("WHITE")\n\t\t\t\t\t],\n\t\t\t\t\t[\n\t\t\t\t\t\tKeyboardButton().openlink("YouTube", "https://youtube.com/c/Фсоки")\n\t\t\t\t\t],\n\t\t\t\t\t[\n\t\t\t\t\t\tKeyboardButton().location()\n\t\t\t\t\t]\n\t\t\t\t]\n\t\t\t)\n\n\t\t\tsend_message(user_id, "VkTools Keyboard by Fsoky ~", keyboard)\n\t\telif text == "test carousel":\n\t\t\tcarousel = Carousel(\n\t\t\t\t[\n\t\t\t\t\tCarouselButton().openlink(\n\t\t\t\t\t\t[\n\t\t\t\t\t\t\tCarouselButton().element(\n\t\t\t\t\t\t\t\ttitle="Title 1",\n\t\t\t\t\t\t\t\tdescription="Description 1",\n\t\t\t\t\t\t\t\tphoto_id="-203980592_457239030",\n\t\t\t\t\t\t\t\tlink="https://vk.com/fsoky",\n\t\t\t\t\t\t\t\tbuttons=[KeyboardButton().text("Button 1", "positive")]\n\t\t\t\t\t\t\t),\n\t\t\t\t\t\t\tCarouselButton().element(\n\t\t\t\t\t\t\t\ttitle="Title 2",\n\t\t\t\t\t\t\t\tdescription="Description 2",\n\t\t\t\t\t\t\t\tphoto_id="-203980592_457239029",\n\t\t\t\t\t\t\t\tlink="https://vk.com/fsoky",\n\t\t\t\t\t\t\t\tbuttons=[KeyboardButton().text("Button 2", "negative")]\n\t\t\t\t\t\t\t)\n\t\t\t\t\t\t]\n\t\t\t\t\t)\n\t\t\t\t]\n\t\t\t)\n\n\t\t\tsend_message(user_id, "VkTools Carousel by Fsoky ~", carousel=carousel)\n```',
    'author': 'Fsoky',
    'author_email': 'cyberuest0x12@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
