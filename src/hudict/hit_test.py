import re

WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9'’-]*")


def nearest_word(lines, mouse_image_x, mouse_image_y):
    candidates = []
    for line_index, line in enumerate(lines):
        for word_index, word in enumerate(line.words):
            if not WORD_RE.fullmatch(word.text):
                continue
            line_pad = max(line.box.height * 1.25, word.box.height)
            if not (line.box.top - line_pad <= mouse_image_y <= line.box.bottom + line_pad):
                continue
            word_pad = max(line.box.height * 0.75, word.box.height)
            if not (word.box.top - word_pad <= mouse_image_y <= word.box.bottom + word_pad):
                continue
            if not (word.box.left <= mouse_image_x <= word.box.right):
                continue
            candidates.append((word.box.distance_sq_to(mouse_image_x, mouse_image_y), line_index, word_index, word))
    if not candidates:
        return None
    return min(candidates, key=lambda item: (item[0], item[1], item[2]))[3]
