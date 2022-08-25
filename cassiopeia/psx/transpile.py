
import ast
from lib2to3.pgen2.tokenize import generate_tokens
from tokenize import tokenize, untokenize
import token as _token_types

class ListReader:
    def __init__(self, lines):
        self.lines = lines
        self.idx   = -1
    def __call__(self):
        self.idx += 1
        if self.idx < len(self.lines): raise StopIteration()

        return self.lines[self.idx]

ITEM_CREATION_NAMES = [
    "return"
]

def is_item_creation_name(token):
    if token.type != _token_types.NAME: return False

    return token.string in ITEM_CREATION_NAMES

def is_psx_start_token(tokens, idx):
    if tokens[idx].type   != _token_types.OP: return False
    if tokens[idx].string != "<": return False
    if idx == 0: return True

    last_token = tokens[idx - 1]
    next_token = None
    if idx + 1 != len(tokens): next_token = tokens[idx + 1]

    return (
        last_token.type == _token_types.OP or is_item_creation_name(last_token)
        or (next_token != None and next_token.type == _token_types.OP and next_token.string == "/")
    )

def transpile_file(path):
    with open(path, 'rb') as file:
        tokens     = list(tokenize(file.readline))
        new_tokens = []
        depth      = 0

        idx = 0
        while idx < len(tokens):
            token = tokens[idx]

            if not is_psx_start_token(tokens, idx):
                new_tokens.append(token)
                idx += 1
            else:
                idx += 1
                
                if idx < len(tokens) and tokens[idx].string == "/":
                    depth -= 1
                    new_tokens.append(
                        (_token_types.OP, ")", token.start, token.start, token.line)
                    )
                    idx += 1

                    while idx < len(tokens) and tokens[idx].string != ">":
                        idx += 1
                    idx += 1
                else:
                    if depth != 0:
                        new_tokens.append(
                            (_token_types.OP, ",", token.start, token.start, token.line)
                        )

                    new_tokens.extend([
                        (_token_types.NAME, "psx",        token.start, token.start, token.line),
                        (_token_types.OP,    ".",         token.start, token.start, token.line),
                        (_token_types.NAME, "createNode", token.start, token.start, token.line),
                        (_token_types.OP,    "(",         token.start, token.start, token.line),
                        (_token_types.OP,    "'",         token.start, token.start, token.line),

                        (_token_types.NAME, tokens[idx].string, token.start, token.start, token.line),

                        (_token_types.OP,    "'",         token.start, token.start, token.line)
                    ])
                    idx += 1

                    while idx < len(tokens) and tokens[idx].string != ">":
                        idx += 1
                    idx += 1
                    depth += 1
        
        return untokenize(new_tokens)
