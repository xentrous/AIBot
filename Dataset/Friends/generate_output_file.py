import sys
inp=open('input.txt','r')
out=open('output.txt','w')
sys.stdout=out
sys.stdin=inp
print '{\n"friends":\n[\n['
for i in range(1,291380):#291380
    dialog=raw_input()
    if dialog=='' or dialog[0]>='0' and dialog[0]<='9':
        continue
    if 'Shared' in dialog or 'Downloaded' in dialog or 'font color' in dialog:
        continue
    dialog=dialog.replace("\"","'")
    if(dialog[0]>='A' and dialog[0]<='Z' or dialog[0]=="-"):
        print '",',
        print '\n',
        dialog='"'+dialog
    print dialog,
print '"\n]\n]\n}'
