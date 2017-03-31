
from collections import namedtuple

OpData = namedtuple('OpData', 'name operandCount operandNames')

OpData('define reference value', 2, ['name', 'value'])
'''
List of codes for the join language.
This is the list of codes. The all will take parameters.
'''
# No notion of type is here preserved.
# As no notion of type, no notion of immutabilty, reference, or other annotaion is preserved.
# Somewhat explicit, NOT universal bytecode. 
# It is assumed these ideas are resoved before this stage e.g. an immutable value is tested never to be altered. A value type may be resolved to be a literal or a reference, dependant on if the platform is able to handle the size. 
# 'slots' are used for setting up parameters. 'slots' may be registers or stack, depending on call convention
# Unlike other intermediate codes, this therefore assumes decisions have been made about how to handle types. For examle, on x64, anything less than 64bit inteers may be on slots. But bigger number types will be handled by calls. 
# Operations have variable parameters count 0, 1, or 2
# need ops for local vars, SSE, MME, 3DNow, arrays, strings...
#! longer references preserved as byte-sequences?
#! build robustness into the code, state the number of operands expected?
#! how to handle return/ program exit? Using a builtin method? 
#! return from global code? Automatic,  or return required?
codeDataMap = {
0 : OpData('error', 0, []),
1 : OpData('defconst', 2, ['const name', 'constant']),
2 : OpData('defspace', 2, ['space name', 'byteSize']),
3 : OpData('declExtenalFunc', 1, ['name']),

10 : OpData('toReg', 2, ['register idx', 'address/constant']),
11 : OpData('fromReg', 2, ['register idx', 'value']),
12 : OpData('toParam', 2, ['param idx', 'address/constant']),
#! op2 is more usefully register or constant? but how to parse that?
13 : OpData('toSpace', 2, ['space name', 'address/constant']),
14 : OpData('fromCallReturn', 1, ['register/address']),
# Both will usually use stack. But we don't care, just protect the value.
18 : OpData('slot protect', 1, ['param idx']),
19 : OpData('slot recover', 1, ['param idx']),


30 : OpData('add', 2, ['register/address', 'address/constant']), #constant/label, constant/label
31 : OpData('sub', 2,  ['register/address', 'address/constant']),
32 : OpData('mult', 2,  ['register/address', 'address/constant']),
33 : OpData('div', 2,  ['register/address', 'address/constant']),
35 : OpData('remainder', 2,  ['value1', 'value2']),
36 : OpData('inc', 1,  ['register/address']), #label
37 : OpData('dec', 1, ['register/address']), #label

40 : OpData('shift left', 1, ['address']),
41 : OpData('shift right', 1, ['address']),
50 : OpData('or', 2,  ['register idx', 'value2']),
51 : OpData('and', 2,  ['register idx', 'value2']),
52 : OpData('not', 1,  ['register idx']),
53 : OpData('xor', 2,  ['register idx', 'value2']),

70 : OpData('unconditional jump', 2, ['name', 'value']), #label
71 : OpData('unconditional long jump', 2, ['name', 'value']), #label
# in other words, cascaded switch. Other jump code may make a 'c'-style switch 
# has several parameters
72 : OpData('indexed jump', 2, ['name', 'value']), #label
73 : OpData('jump on comparison success', 2, ['name', 'value']),

80 : OpData('cmp', 2, ['name', 'value']), #slot/constant


100 : OpData('call', 1, ['name']), #label
101 : OpData('return', 2, ['name', 'value'])

#100 : OpData('if', 2, ['name', 'value']),
#101 : OpData('while', 2, ['name', 'value']),

}

codeToOperandCount = {k : v.operandCount for k, v in codeDataMap.items()}

codeToName = {k : v.name for k, v in codeDataMap.items()}

#tokenToString =  {}
#for k, v in tokens.items():
#    tokenToString[v] = k
nameToCode = {v.name : k for k, v in codeDataMap.items()}

# I do not know if this linear array of tokens is a good datatype---ragged array, but of references. Awkward to step, but likely fast, if that's all we need?
def toString(tokenArray):
  b = []
  i = 0
  limit = len(tokenArray)
  while i < limit:
    token = tokenArray[i]
    b.append(codeToName[token])
    i += 1
    limit2 = i + codeToOperandCount[token]
    while i < limit2:
      b.append(' ')
      b.append(str(tokenArray[i]))
      i += 1
    b.append('\n')

  return ''.join(b)
