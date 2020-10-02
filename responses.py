def get_words(input, strip_emojis=False):
    words = []
    for each in input:
        indv_words = each.split(" ")
        for word in indv_words:
            if strip_emojis:
                if word[0] != ":" and word[-1] != ":":
                    words.append(word)
            else:
                words.append(word)
    return words


def get_end_words(input, strip_emojis=False):
    words = []
    for each in input:
        indv_words = each.split()
        end_word = indv_words[-1]
        if strip_emojis:
            if end_word[0] != ":" and end_word[-1] != ":":
                words.append(end_word)
        else:
            words.append(end_word)
    return words

chat_wardens = [
    'its ya boi chaaad warden!!!',
    'im talkin bout that PS QUINTOUPLE!',
    'Xbox SeX?? man that controller look like a DIL DO',
    'Xbox aint got no gameS!!!',
    'i aint talkin about that wii... shitt... people be talkin about its all... \'new\' n shit',
    'i aint tryna play my games with no DIL DO',
    'Warioware: shove it up yo own ass game NOT IN STOCK',
    'xbox palyers cant do shit except SUCK DICK',
    'sony is true shit',
    'FUCK gears of war, more like TEARS of war. lil bitch ass cryn all the time',
    'True games have some 50 cent in the background.. some fat joe.. some BALLIN',
    'Chad warden wipes his ASS with 600 dollars',
    'girls are only good for suckin DICK',
    'playstation got final fantasy SEVEN!',
    'microSOFT spent all this time and effort at #e3 to say that project Scarlett is powerful, only for the PScinco to be stronger',
    'Good evening to all the ballin’ and superior gaming systems that didn’t have a pathetic showing at #E3 today.',
    'I LOVE SONY SO FUCKING MUCH BRUH THEY SOME HARD ASS NIGGAS IN THE FUCKING PAINT',
    'IMA JUST SIT HERE AND CRY BRUH',
    'do xbox got a fucking shoe? thought so hoe',
    'sup bitches',
    'Sony always win, baby. Always win.'
]

chat_warden_vid = 'https://youtu.be/vyufDxxWIsM',