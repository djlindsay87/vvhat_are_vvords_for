import regex as re

reggie = {
    "bracket": r"[\[<][^\]>]+[>\]](?# brackets)",

    "between": r"(?<=[^\W\d])[^\s,()\"]+(?=[^\W\d])(?# one or more non-space characters between letters)",
    "digs": r"(?<=[^\W\d])\d+|\d+(?=[^\W\d])(?# leading and trailing numbers)",
    "acs": r"(?<=(?=\S*\.\w)\S\S[^\W\d])\.(?# period at end if there is a period at most two before)",
    "aps": r"(?<!\S\.|\.[^\W\d])(?:(?<=[^\W\d])'|'(?=[^\W\d]))(?!\S*\.\w)(?# apostrophe if not acronym)",

    "currency": r"[$¢£¤¥֏؋৲৳৻૱௹฿៛\u20a0-\u20bd\ua838\ufdfc\ufe69\uff04\uffe0\uffe1\uffe5\uffe6]",
    "nums": r"\d|(?<=\d)[.,]{1,2}(?=\d)(?# decimal, comma between numbers)"
}

words = f'[^\W\d](?# letter)|{reggie["between"]}|{reggie["digs"]}|{reggie["acs"]}|{reggie["aps"]}'
uComp = f"(?u){reggie['bracket']}|(?:{words})+(?# one or more)|{reggie['currency']}*\.*(?:{reggie['nums']})+\.?"


def tokenize(text):
    pattern = re.compile(uComp)
    tokens = [pattern.findall(text.lower())]
    return tokens


song = """Cry baby cry
Make your mother sigh
She's old enough to know better
So cry baby cry
The King of Marigold was in the kitchen cooking breakfast for the queen
The queen was in the parlour playing piano for the children of the king
Cry baby cry
Make your mother sigh
She's old enough to know better
So cry baby cry
The king was in the garden picking flowers for a friend who came to play
The queen was in the playroom painting pictures for the children's holiday
Cry baby cry
Make your mother sigh
She's old enough to know better
So cry baby cry
The Duchess of Kircaldy always smiling and arriving late for tea
The duke was having problems with a message at the local Bird and Bee
Cry baby cry
Make your mother sigh
She's old enough to know better
So cry baby cry
At Twelve o'clock a meeting 'round the table for a seance in the dark
With voices out of nowhere put on specially by the children for a lark
Cry baby cry
Make your mother sigh
She's old enough to know better
So cry baby cry
Cry baby cry cry cry baby
Make your mother sigh
She's old enough to know better
So cry baby cry cry cry cry
Make your mother sigh
She's old enough to know better
So cry baby cry
"""
