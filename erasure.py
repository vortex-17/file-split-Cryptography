#testing of the erasure coding
#We will do 4-2 Erasure coding

from base64 import b64decode
import sys
from decimal import *
import numpy as np

sys.setrecursionlimit(10000)
getcontext().prec = 20000

def encode(data):
    enc = data.encode("latin1")
    # print(enc)
    data_int = int.from_bytes(enc, "little")
    return data_int

def decode(enc):
    dec = enc.to_bytes((enc.bit_length() + 7) // 8, "little")
    data = dec.decode("latin1")
    return data

def create_parity_block(content):
    """
    p1 = a + b + c + d
    p2 = a + 4b + 6c + 8d
    """
    p1 = 0
    p2 = 0
    for i in range(len(content)):
        p1 += int(Decimal(content[i]))
        p2 += int(Decimal(content[i] * (i+1)*2))

    return p1,p2

def find_inverse(n):
    det = abs((Decimal(n[0][0]) * Decimal(n[1][1])) - (Decimal(n[0][1]) * Decimal(n[1][0])))
    n[0][0], n[1][1] = n[1][1] / det, n[0][0] / det
    n[0][1], n[1][0] = -1 * n[0][1] / det, -1 * n[1][0] / det
    return n

def find_missing(val,p1,p2):
    max_val = max(val)
    max_val = max([max_val,p1,p2])
    getcontext().prec = len(str(max_val)) * 50
    missing_val = [i for i in range(len(val)) if val[i] == 0]
    if len(missing_val) == 1:
        x = p1-sum(val)
        val[missing_val[0]] = x
    elif len(missing_val) == 2:
        c1 = Decimal(p1 - sum(val))
        v = [((i+1) * 2) * val[i] for i in range(len(val))]
        c2 = Decimal(p2 - sum(v))
        C = [[c1],[c2]]
        A = [[Decimal(1.0),Decimal(1.0)]]
        l = [Decimal((i+1)*2) for i in missing_val]
        # A = [[float(1.0),float(1.0)]]
        # l = [float((i+1)**2) for i in missing_val]
        A.append(l)
        inv_A = find_inverse(A)
        # A = np.array(A)
        # # print(A)
        # inv_A = list(np.linalg.inv(A))
        # A = np.array(A)
        # print(A)
        # inv_A = list(np.linalg.inv(A))
        
        # inv_A[0] = list(inv_A[0])
        # inv_A[1] = list(inv_A[1])
        # print(inv_A)

        A1 = []
        for i in inv_A:
            a = []
            for j in i:
                a.append(Decimal(j))
            A1.append(a)

        inv_A = A1
        # print(A1)
        X = [0,0]
        getcontext().prec = len(str(max_val)) * 1000
        X[0] = (inv_A[0][0] * C[0][0]) + (inv_A[0][1] * C[1][0])
        X[1] = (inv_A[1][0] * C[0][0]) + (inv_A[1][1] * C[1][0]) 
        val[missing_val[0]] = int(X[0])
        val[missing_val[1]] = int(X[1])
    else:
        return None

    return val

def find(content,p1,p2):
    """ 
    The content will have few missing entries and
    this will return all the content using
    Erasure Coding
    """
    enc_content = []
    for i in content:
        if i == "":
            enc_content.append(0)
        else:
            enc_content.append(encode(str(i)))
    
    if enc_content.count(0) > 2 :
        return None
    new_content = find_missing(enc_content,p1,p2)
    # print(new_content)
    for i in range(len(new_content)):
        new_content[i] = decode(new_content[i])

    return new_content


# content = ["This is line 1", "This is line 2", "This is line 3", "This is line 4"]
# content = ['q¢\x99¤\x98\x9d\x95¤\x99\x93P\x93\x9f\x94\x99\x9e\x97P\x99£P£¥\xa0\x95¢\x99\x9f¢P\x99\x9eP\x9d\x9f£¤P¢\x95£\xa0\x95\x93¤£P¤\x9fP¤\x98\x95:\x92\x95¤¤\x95¢]\x9b\x9e\x9f§\x9ePx¥\x96\x96\x9d\x91\x9eP\x8b\x9c\x9f\x8dP\x9d\x95¤\x98\x9f\x94^Py¤P¢\x95\xa0¢\x95£\x95\x9e¤£P\x99\x9e\x96\x9f¢\x9d\x91¤\x99\x9f\x9eP\x91¤P\x9c\x95\x91£¤P\x91£P\x93\x9f\x9d\xa0\x91\x93¤\x9c©]£\x9f\x9d\x95¤\x99\x9d\x95£P\x93\x9f\x9e£\x99\x94\x95¢\x91\x92\x9c©P\x9d\x9f¢\x95P£\x9f^Py¤£P\xa0\x95¢\x96\x9f¢\x9d\x91\x9e\x93\x95P\x99£P\x9f\xa0¤\x99\x9d\x91\x9cP§\x99¤\x98\x9f¥¤:¤\x98\x95P\x9e\x95\x95\x94P\x96\x9f¢P\x92\x9c\x9f\x93\x9b\x99\x9e\x97P\x9f\x96P\x99\x9e\xa0¥¤P\x94\x91¤\x91^Py¤P\x95\x9e\x93\x9f¥¢\x91\x97\x95£P\x91:\x93\x9c\x95\x91¢P£\x95\xa0\x91¢\x91¤\x99\x9f\x9eP\x92\x95¤§\x95\x95\x9eP¤\x98\x95P\x9d\x9f\x94\x95\x9cP\x96\x9f¢P¢\x95\xa0¢\x95£\x95\x9e¤\x99\x9e\x97:\x94\x91¤\x91P\x91\x9e\x94P¤\x98\x95P\x95\x9e\x93\x9f\x94\x99\x9e\x97P\x9f\x96P\x99\x9e\x96\x9f¢\x9d\x91¤\x99\x9f\x9eP§\x99¤\x98P¢\x95£\xa0\x95\x93¤P¤\x9f:¤\x98\x91¤P\x9d\x9f\x94\x95\x9c^Py¤P\x91\x93\x93\x9f\x9d\x9d\x9f\x94\x91¤\x95£P\x91\x94\x91\xa0¤\x99¦\x95P\x9d\x9f\x94\x95\x9c£P\x95\x91£\x99\x9c©:\x91\x9e\x94P\x99£P', '\x93\x9f\x9d\xa0¥¤\x91¤\x99\x9f\x9e\x91\x9c\x9c©P\x95\x96\x96\x99\x93\x99\x95\x9e¤^P\x89\x95¤P\x9d\x91\x9e©P\x91¥¤\x98\x9f¢£:\x91\x9e\x94P\xa0¢\x91\x93¤\x99¤\x99\x9f\x9e\x95¢£P£\x95\x95\x9dP¥\x9e\x91§\x91¢\x95P\x9f\x96P¤\x98\x95P¤\x95\x93\x98\x9e\x99¡¥\x95^:y\x9e\x94\x95\x95\x94P¤\x98\x95¢\x95P\x99£P\x91P§\x99\x94\x95£\xa0¢\x95\x91\x94P\x92\x95\x9c\x99\x95\x96P¤\x98\x91¤Px¥\x96\x96\x9d\x91\x9e:\x93\x9f\x94\x99\x9e\x97P\x93\x91\x9e\x9e\x9f¤P\x92\x95P\x99\x9d\xa0¢\x9f¦\x95\x94P¥\xa0\x9f\x9e^\x87\x95P\x91\x99\x9dP¤\x9fP¢\x95\x93¤\x99\x96©P¤\x98\x99£P£\x99¤¥\x91¤\x99\x9f\x9eP\x92©P\xa0¢\x95£\x95\x9e¤\x99\x9e\x97P\x91\x9e:\x91\x93\x93\x95££\x99\x92\x9c\x95P\x99\x9d\xa0\x9c\x95\x9d\x95\x9e¤\x91¤\x99\x9f\x9eP\x9f\x96P\x91¢\x99¤\x98\x9d\x95¤\x99\x93P\x93\x9f\x94\x99\x9e\x97P\x91\x9e\x94:\x92©P\x94\x95¤\x91\x99\x9c\x99\x9e\x97P\x99¤£P\xa0\x95¢\x96\x9f¢\x9d\x91\x9e\x93\x95P\x93\x98\x91¢\x91\x93¤\x95¢\x99£¤\x99\x93£^P\x87\x95P£¤\x91¢¤:\x92©P\x92¢\x99\x95\x96\x9c©P¢\x95¦\x99\x95§\x99\x9e\x97P\x92\x91£\x99\x93P\x93\x9f\x9e\x93\x95\xa0¤£P\x9f\x96P\x94\x91¤\x91P\x93\x9f\x9d\xa0¢\x95££\x99\x9f\x9eP\x91\x9e\x94P\x99\x9e¤¢\x9f\x94¥\x93\x99\x9e\x97P¤\x98\x95P\x9d\x9f\x94\x95\x9c]\x92\x91£\x95\x94P\x91\xa0', '\xa0¢\x9f\x91\x93\x98P¤\x98\x91¤:¥\x9e\x94\x95¢\x9c\x99\x95£P\x9d\x9f£¤P\x9d\x9f\x94\x95¢\x9eP¤\x95\x93\x98\x9e\x99¡¥\x95£^P\x87\x95P¤\x98\x95\x9eP\x9f¥¤\x9c\x99\x9e\x95:¤\x98\x95P\x99\x94\x95\x91P\x9f\x96P\x91¢\x99¤\x98\x9d\x95¤\x99\x93P\x93\x9f\x94\x99\x9e\x97P¥£\x99\x9e\x97P\x91P£\x99\x9d\xa0\x9c\x95P\x95¨\x91\x9d\xa0\x9c\x95\\P\x92\x95\x96\x9f¢\x95P\xa0¢\x95£\x95\x9e¤\x99\x9e\x97P\xa0¢\x9f\x97¢\x91\x9d£P\x96\x9f¢P\x92\x9f¤\x98P\x95\x9e\x93\x9f\x94\x99\x9e\x97:\x91\x9e\x94P\x94\x95\x93\x9f\x94\x99\x9e\x97^Py\x9eP¤\x98\x95£\x95P\xa0¢\x9f\x97¢\x91\x9d£P¤\x98\x95P\x9d\x9f\x94\x95\x9cP\x9f\x93\x93¥\xa0\x99\x95£:\x91P£\x95\xa0\x91¢\x91¤\x95P\x9d\x9f\x94¥\x9c\x95P£\x9fP¤\x98\x91¤P\x94\x99\x96\x96\x95¢\x95\x9e¤P\x9d\x9f\x94\x95\x9c£P\x93\x91\x9eP\x95\x91£\x99\x9c©:\x92\x95P¥£\x95\x94^P~\x95¨¤P§\x95P\x94\x99£\x93¥££P¤\x98\x95P\x93\x9f\x9e£¤¢¥\x93¤\x99\x9f\x9eP\x9f\x96P\x96\x99¨\x95\x94:\x91\x9e\x94P\x91\x94\x91\xa0¤\x99¦\x95P\x9d\x9f\x94\x95\x9c£P\x91\x9e\x94P\x94\x95¤\x91\x99\x9cP¤\x98\x95P\x93\x9f\x9d\xa0¢\x95££\x99\x9f\x9e:\x95\x96\x96\x99\x93\x99\x95\x9e\x93©P\x91\x98\x97\x96\x97\x96\x95¨\x95\x93¥¤\x99\x9f\x9eP¤\x99\x9d\x95P\x9f\x96P¤\x98\x95P\xa0¢\x9f\x97¢\x91\x9d£\\:\x99\x9e\x93\x9c¥\x94', "'q¢\x99¤\x98\x9d\x95¤\x99\x93P\x93\x9f\x94\x99\x9e\x97P\x99£P£¥\xa0\x95¢\x99\x9f¢P\x99\x9eP\x9d\x9f£¤P¢\x95£\xa0\x95\x93¤£P¤\x9fP¤\x98\x95:\x92\x95¤¤\x95¢]\x9b\x9e\x9f§\x9ePx¥\x96\x96\x9d\x91\x9eP\x8b\x9c\x9f\x8dP\x9d\x95¤\x98\x9f\x94^Py¤P¢\x95\xa0¢\x95£\x95\x9e¤£P\x99\x9e\x96\x9f¢\x9d\x91¤\x99\x9f\x9eP\x91¤P\x9c\x95\x91£¤P\x91£P\x93\x9f\x9d\xa0\x91\x93¤\x9c©]£\x9f\x9d\x95¤\x99\x9d\x95£P\x93\x9f\x9e£\x99\x94\x95¢\x91\x92\x9c©P\x9d\x9f¢\x95P£\x9f^Py¤£P\xa0\x95¢\x96\x9f¢\x9d\x91\x9e\x93\x95P\x99£P\x9f\xa0¤\x99\x9d\x91\x9cP§\x99¤\x98\x9f¥¤:¤\x98\x95P\x9e\x95\x95\x94P\x96\x9f¢P\x92\x9c\x9f\x93\x9b\x99\x9e\x97P\x9f\x96P\x99\x9e\xa0¥¤P\x94\x91¤\x91^Py¤P\x95\x9e\x93\x9f¥¢\x91\x97\x95£P\x91:\x93\x9c\x95\x91¢P£\x95\xa0\x91¢\x91¤\x99\x9f\x9eP\x92\x95¤§\x95\x95\x9eP¤\x98\x95P\x9d\x9f\x94\x95\x9cP\x96\x9f¢P¢\x95\xa0¢\x95£\x95\x9e¤\x99\x9e\x97:\x94\x91¤\x91P\x91\x9e\x94P¤\x98\x95P\x95\x9e\x93\x9f\x94\x99\x9e\x97P\x9f\x96P\x99\x9e\x96\x9f¢\x9d\x91¤\x99\x9f\x9eP§\x99¤\x98P¢\x95£\xa0\x95\x93¤P¤\x9f:¤\x98\x91¤P\x9d\x9f\x94\x95\x9c^Py¤P\x91\x93\x93\x9f\x9d\x9d\x9f\x94\x91¤\x95£P\x91\x94\x91\xa0¤\x99¦\x95P\x9d\x9f\x94\x95\x9c£P\x95\x91£\x99\x9c©:\x91\x9e\x94P\x99£P'"]
# content = ['£P£PPa:', '£P£PPb:', '£P£PPc:', '£P£PPdS']
# enc_content = [encode(i) for i in content]
# print(enc_content)
# p1,p2 = create_parity_block(enc_content)
# # p1 = 12363004624434286804498302116693800162352998200044097235730309500187505197812606286109253690783845847419328082978083715071997972275358103880868071722357276523921116170540228549238141415478177682657932125270178493778525644085489908585626133937804445033616655136079422109299134996051699597939470179822255703756411161666950389256565986607074027503972084092395165686654482712853536687731895085354011891118555555887106365860030408525547085518937151337442828871718919700958614661828207450109077851452110740999306219475854579937615125968864115451645852215103510238741648674746034566680926909956660079012577104949927159799901786017578556804607963828809220184763293602717256060127792295163334528894220898127393026205275170918534061881821887612940825334995090374648096694578050490326050008648572254616369847724150079628395013144766462476242386433580834745001383064296053845388887125514607083908549386228396185251939811162552651293566694697011946757865032169474283828233755914316944769057056087713911252840581763932471933
# # p2 = 85893381224786080479861365561563804090797114808907958737942132214509487985776283042848748011623717668884605148482902325548235716444105017512123057512436081594682375343687847541140465204821538953521736834504534970293797902817562835407210024989696540575614972266830757198365638306170081926130609734831434468341513574758303800822577572607913405078929137002518515029422879395293433556750437230878445733286423574018472997059516132742401939498735716725118451074747391718981438962856370656060728694094753319350076638151596203944244329083320187108728529854345306907661885185505007799688829274192176653426490355168285243363919627917235494226148910390198142886835332189328747886874932003114528280953126221279118105985845202740271847396384564561066345002048173779628492831433702844321540489321198816051486911742445615457353595194775019275330010115947609857720345724936809101109567355837573923415017417138653239829597264163197966927568573953346324938022604560667660736239427158122982256099576773764398809759510332396608589
# content[2] = ''
# content[3] = ''
# dec = find(content,p1,p2)
# print(dec)