import os
import re
import sys

def memu():
    print('''usage:
    Make a new floder, put the elf, libc, ld and this file in .
    python resetlibc.py [elf_name]
    python3 resetlibc.py [elf_name] --skipld
    (Use --skipld only replace libc and skip ld)''')
if __name__=='__main__':
    if len(sys.argv)==1:
        memu()
        sys.exit()
    arg1=sys.argv[1]
    elfname=arg1
    arg2=sys.argv[2]
    isnold=(arg2!="--skipld")
    #elfname="./work" #choose elf in this is also fine.
    lddres=os.popen('ldd '+elfname).readlines()
    print(lddres)
    if len(lddres)<2:
        print("file error")
        sys.exit()
    for oneline in lddres:
        print(oneline)
        if "00" in oneline:
            if "libc" in oneline:
                print("111",oneline)
                libcname=re.findall(r"\s*([\S]*)\s",oneline)[0]
            elif "ld-" in oneline:
                ldname=re.findall(r"\s*([\S]*)\s",oneline)[0]
    print("---",libcname,ldname)
    libcnamelen=len(libcname)
    if libcnamelen>6:
        newlibcname='./libc'+'a'*(libcnamelen-6)
    else:
        newlibcname='./'+'a'*(libcnamelen-2)

    ldnamelen=len(ldname)
    if ldnamelen>4:
        newldname='./ld'+'b'*(ldnamelen-4)
    else:
        newldname='./'+'b'*(ldnamelen-2)

    replacecommand1='sed -i s#'+libcname+'#'+newlibcname+'#g ./'+elfname
    replacecommand2='sed -i s#'+ldname+'#'+newldname+'#g ./'+elfname
    print("Please rename the libc and ld file as this:")
    print("libc: "+newlibcname[2:])
    os.system(replacecommand1)
    if isnold:
        os.system(replacecommand2)
        print("ld: "+newldname[2:])
    try:
        filelist=os.listdir('./')
        for onefile in filelist:
            if "libc" in onefile and 'so' in onefile:
                os.rename(onefile,newlibcname[2:])
            if "ld-" in onefile and isnold:
                os.rename(onefile,newldname[2:])
    except:
        pass
    print('Done!')
