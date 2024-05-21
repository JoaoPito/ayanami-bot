import re

def split_phrases(raw_text, max_chars):
    phrases_idx = []
    for match in re.finditer('.*?[.!?]', raw_text, flags=re.DOTALL):
        phrases_idx.append((match.start(), match.end()))
    text_pieces = []
    cur_piece = ""

    for start,end in phrases_idx:
        phrase = raw_text[start:end]
        if len(cur_piece + phrase) <= max_chars:
            cur_piece += phrase
        else:
            text_pieces.append(cur_piece.strip())
            cur_piece = phrase

    if cur_piece:
        text_pieces.append(cur_piece.strip())

    last_piece = raw_text[end:]
    if not last_piece.isspace() and not last_piece == '':
        text_pieces.append(last_piece)

    return text_pieces