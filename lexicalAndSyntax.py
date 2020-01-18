import shlex
import re
from collections import deque 
  
#Examen Teoria de Automatas
# Diana Contreras Colunga   A730583 

#Analizador de lexico. Parte I Proyecto Teoría de Autómatas
def lexicalAnalizer():
    #EL texto necesota estar en el mismo path del file 
    filename = "text2.txt"

    with open(filename, 'r') as f:
        body = f.read()
    print('ORIGINAL: {!r}'.format(body))

    print()

    reserved = ["var", "if","then", "output","input"]
    const = re.compile('-?[0-9]{0,10}')
    characters = [".", ",", ";", "{", "}", "=", "(", ")", "+", "-", "<", ">", "=="]   
    tokensArr = []
    s = ''

    print('TOKENS:')
    lexer = shlex.shlex(body)
    for token in lexer:
        if token not in reserved and token not in characters :
            if const.match(token):
            #if token.isdigit() :
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

    return tokensArr




#Funcion para el analizador de sintaxis. Parte II
def readTokens(tokensArr):
    #regex para el ident y const de la gramatica 
    ident = re.compile('[a-zA-Z][a-zA-Z0-9]*')
    const = re.compile('(-?[1-9][0-9]*|0)')
    LPAR = '('
    RPAR = ')'
    LKEY = '{'
    RKEY = '}'
    reserved = {"var", "while", "if","then", "output","input", "do"}
    characters = {".", ",", ";", "{", "}", "=", "(", ")", "+", "-", "<", ">", "=="}
    reservedThen = {"if", "while", "input"}
    opLog = {"<", ">"}
    opMath = {"+", "-"}
    #stack principal
    stack = []
    #stack para variables
    stackIdent = []
    if not tokensArr[0] == 'var' :
        raise Exception("token no valido", tokensArr[0])
    stack.append(tokensArr[0])
    length = len(tokensArr)
    tokensArr.pop(0)
    
    for i in range (length):
        if stack[-1] == 'var':
            if not ident.match(tokensArr[i]):
                raise Exception("token no valido", tokensArr[i])
                
            stack.append(tokensArr[i])
            stackIdent.append(tokensArr[i])

        elif stack[-1] in reserved:
            if stack[-1] == 'input':
                if not ident.match(tokensArr[i]):
                   raise Exception("token no valido", tokensArr[i])
                else:
                    stack.append(tokensArr[i])
                    stackIdent.append(tokensArr[i])
            elif stack[-1] == 'if':
                if not const.match(tokensArr[i]) and not tokensArr[i] in stackIdent:
                    raise Exception("token invalido", tokensArr[i])
                stack.append(tokensArr[i])

            if stack[-1] == 'while':
                if not tokensArr[i] in stackIdent and not tokensArr[i] == LPAR and not const.match(tokensArr[i]):
                    raise Exception("token no valido", tokensArr[i])
                stack.append(tokensArr[i])
            
            if stack[-1] == 'do':
                if not tokensArr[i] == LKEY:
                    raise Exception("token no valido", tokensArr[i])
                stack.append(tokensArr[i])

            elif stack[-1] == 'then':
                if not tokensArr[i] in stackIdent and not tokensArr[i] in reservedThen:
                    raise Exception("token no valido", tokensArr[i])
                stack.append(tokensArr[i])

            elif stack[-1] == 'output':
                if not tokensArr[i] in stackIdent:
                    raise Exception("token no valido", tokensArr[i])
                stack.append(tokensArr[i])   

        elif ident.match(stack[-1]):
            if not stack[-1] in stackIdent:
                raise Exception("token no valido", tokensArr[i])
            if  not tokensArr[i] == ',' and not tokensArr[i] == ';' and not tokensArr[i] == '=' and not tokensArr[i] == '.' and not tokensArr[i] in opLog and not tokensArr[i] == 'do' and not tokensArr[i] == 'then' and not tokensArr[i] in opMath:
                raise Exception("token no valido", tokensArr[i])
            stack.append(tokensArr[i])
            

        elif stack[-1] in characters:
            if stack[-1] == ',':
                if not ident.match(tokensArr[i]):
                    raise Exception("token no valido", tokensArr[i])
                else:
                    stack.append(tokensArr[i])
                    stackIdent.append(tokensArr[i])
            
            elif stack[-1] == ';':
                if not tokensArr[i] in reserved:
                    if ident.match(tokensArr[i]):
                        if not tokensArr[i] in stackIdent:
                            raise Exception("token no valido", tokensArr[i])
                stack.append(tokensArr[i])

            elif stack[-1] == '=':
                if not const.match(tokensArr[i]) and not tokensArr[i] in stackIdent:
                    raise Exception("token no valido", tokensArr[i])
                stack.append(tokensArr[i])

            elif stack[-1] in opLog:
                if not tokensArr[i] in stackIdent and not const.match(tokensArr[i]):                   
                    raise Exception("token invalido", tokensArr[i])
                stack.append(tokensArr[i])

            elif stack[-1] == LKEY:
                if not tokensArr[i] == RKEY and not tokensArr[i] in stackIdent and not tokensArr[i] in reserved:
                    raise Exception("token invalido", tokensArr[i])
                stack.append(tokensArr[i])

            elif stack[-1] in opMath:
                
                if not tokensArr[i] in stackIdent and not const.match(tokensArr[i]):
                    raise Exception("token no valido", tokensArr[i])
                stack.append(tokensArr[i])

            elif stack[-1] == RKEY:
                if i == length:
                    raise Exception("token invalido", tokensArr[i])
                stack.append(tokensArr[i])


        elif const.match(stack[-1]):
            if not tokensArr[i] == ',' and not tokensArr[i] == ';' and not tokensArr[i] == ',' and not tokensArr[i] == RKEY and not tokensArr[i] == RPAR:
                raise Exception("token no valido", tokensArr[i])
            stack.append(tokensArr[i])

        
         
    return stack

arr = lexicalAnalizer()
st = readTokens(arr)
if st[-1] == '.':
    print("El sintaxis del codigo es correcto")
print(st) 
#print(stack.get()) 
#print(stack.get()) 
    
