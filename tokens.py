
'''
Tokens are not the same as expression symbols. Sometimes
there is a one-one map e.g. 'intNum' 'intNum'.  Sometimes names are revised e.g. '+' : 'add'. Sometimes symbols exist where no one token matches e.g. 'type-annotation'.
Sometimes symbols do not exist where tokens exist e.g. '(' ')'.
'''
LINE_FEED = 10
HASH = 35
PLUS = 43
HYPHEN_MINUS = 45
ICOMMAS = 34
ICOMMA = 39
PERIOD = 46
COMMA = 44
COLON = 58
SEMI_COLON = 59
SOLIDUS = 47
UNDERSCORE = 95
LEFT_BRACKET = 40
RIGHT_BRACKET = 41
LEFT_CURLY = 123
RIGHT_CURLY = 125
LEFT_SQR = 91
RIGHT_SQR = 93


tokens = {
'empty' : 0,
'EOF' : 1,
'identifier' : 2,

# constants
'intNum' : 5,
'floatNum' : 6,
'string' : 7,
'multilineComment': 8,
'comment' : 9,

'and' : 10,
'or' : 11,
'not' : 12,
'xor' : 13,
'+' : 20,
'-' : 21,
'%' : 22,
'*' : 23,
'<<' : 24,
'>>' : 25,
'=' : 31,
#''
# floatlit
#intlit
# blockend

'period' : 40,
'colon' : 41,
'lbracket' : 42,
'rbracket' : 43,
'lcurly' : 44,
'rcurly' : 45,
'lsquare' : 46,
'rsquare' : 47,
'solidus' : 48,
'linefeed' : 49,

'val' : 100,
'fnc' : 102,

'if' : 110,
'while' : 111
}

tokenToString =  {}
for k, v in tokens.items():
    tokenToString[v] = k


def tokensToString(tokens, sep = ', '):
    b = []
    for t in tokens:
       b.append(tokenToString[t])
    return sep.join(b)

#def tokensToString(tokens):
#    return tokensToString(tokens, ',')
