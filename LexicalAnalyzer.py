import shlex
import re

#Analizador de sintaxis. Parte I Proyecto Teoría de Autómatas

filename = "text.txt"

with open(filename, 'r') as f:
    body = f.read()
print('ORIGINAL: {!r}'.format(body))

print()

reserved = ["var", "if","then", "output","input"]
characters = [".", ",", ";", "{", "}", "=", "(", ")", "+", "-", "<", ">", "=="]
tokensArr = []
s = ''

print('TOKENS:')
lexer = shlex.shlex(body)
for token in lexer:
    if token not in reserved and token not in characters :
        if token.isdigit() :
            s += "<const>    " + token
        else :
            s += "<ident>    " + token
    
    else :
        s += token
    s += "\n"
    tokensArr.append(token) 
   
print (s)

with open("Output.txt", "w") as text_file:
    print(f"TOKEN:    valor asociado \n{s}", file=text_file)

#print(tokensArr)