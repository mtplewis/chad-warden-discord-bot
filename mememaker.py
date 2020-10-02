import imgflip
import random
import responses
import markov_chain as mc

def meme(made_up: bool = False):
    api = imgflip.Imgflip(username='brolander_bot', password='Brolander55346a')
    memes = api.get_memes()
    meme = random.choice(memes)
    text_array = []
    for i in range(meme.box_count):
        if made_up:
            text_array.append(mc.make_a_sentence(random.choice(responses.chat_wardens).split(" ")[0], responses.chat_wardens))
        else:
            text_array.append(random.choice([item for item in responses.chat_wardens if not item.startswith('http')]))
    result = api.caption_image_boxes(
        meme,
        text_array
    )
    return result['url']