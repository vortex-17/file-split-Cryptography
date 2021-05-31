from Crypto.Cipher import Blowfish
from Crypto import Random
from struct import pack
import re
import string

bs = Blowfish.block_size
print(bs)
key = str('An arbitrarily long key').encode("latin1")
iv = Random.new().read(bs)
# cipher = Blowfish.new(key, Blowfish.MODE_ECB)
# pt = str('In computer science, cryptography refers to secure information and communication techniques derived fro')
# f = open("sample.txt", "r")
# pt = f.read()
# print(type(pt))
# f.close()
# plaintext = pt.encode("latin1")
# # plaintext = pt.encode("latin1").decode("utf-8").encode()
# plen = bs - divmod(len(plaintext),bs)[1]
# padding = [plen]*plen
# padding = pack('b'*plen, *padding)

# msg = cipher.encrypt(plaintext + padding).decode("latin1")
# print("Encrypted Mssage : ", msg)


# msg = msg.encode("latin1")
# dec_msg = cipher.decrypt(msg)
# print(dec_msg)
# dec_msg = dec_msg.decode("latin1")
# printable = set(string.printable)
# dec_msg = ''.join(list(filter(lambda x: x in printable, dec_msg)))
# # dec_msg = re.sub(r'[^\x00-\x7f]', '', dec_msg)
# # dec_msg = dec_msg.rstrip(r'[^\x20-\x7e]')
# print("PT : ", len(pt))
# print(dec_msg)


# print(dec_msg == pt)

def encrypt(data,key):
    data = str(data)
    # printable = set(string.printable)
    # data = ''.join(list(filter(lambda x: x in printable, data)))
    key = str(key)
    data = data.encode("latin-1")
    key = key.encode("latin-1")
    cipher = Blowfish.new(key, Blowfish.MODE_ECB)
    plen = bs - divmod(len(data),bs)[1]
    padding = [plen]*plen
    padding = pack('b'*plen, *padding)
    print(padding)
    encrypted_text = cipher.encrypt(data + padding)
    # encrypted_text = ""
    # # print("Key : ",key)
    # key = 0
    # for i in str(key)[:5]:
    #     key += ord(i)
    # for i in data:
    #     encrypted_text += chr(ord(i) + key)

    return encrypted_text.decode("latin-1")

def decrypt(data,key):
    key = key.encode("latin-1")
    data = data.encode("latin-1")
    cipher = Blowfish.new(key, Blowfish.MODE_ECB)
    decrypted_text = cipher.decrypt(data)
    decrypted_text = decrypted_text.decode("latin-1")
    printable = set(string.printable)
    decrypted_text = ''.join(list(filter(lambda x: x in printable, decrypted_text)))
    # decrypted_text = re.sub(r'[^\x20-\x7e]', '', decrypted_text)
    # decrypted_text = ""
    # key = 0
    # for i in str(key)[:5]:
    #     key += ord(i)
    # for i in data:
    #     decrypted_text += chr(ord(i) - key)

    return str(decrypted_text)

key = str('An arbitrarily long key')

f = open("sampl1.txt", "r")
data1 = f.read()
f.close()
print("Data :", len(data1))
encrypted_data = encrypt(data1,key)

print("Type of data : ", type(encrypted_data))
print("Encrypted Data : ", encrypted_data)

f = open("enc_sample.txt", "w")
f.write(encrypted_data)
f.close()

f = open("enc_sample.txt", "r")
data2 = f.read()
f.close()

print("Type of data : ", type(data2))
dec_data = decrypt(data2,key)
print("Decrypted Data : ", len(dec_data))

print(data1 == data2)

s1 = 'Cryptography is a method of protecting information and communications through the use of codes, so that only those for whom the information is intended can read and process it. The prefix "crypt-" means "hidden" or "vault" -- and the suffix "-graphy" stands for "writing." In computer science, cryptography refers to secure information and communication techniques derived from mathematical concepts and a set of rule-based calculations called algorithms, to transform messages in ways that are hard to decipher. These deterministic algorithms are used for cryptographic key generation, digital signing, verification to protect data privacy, web browsing on the internet, and confidential communications such as credit card transactions and email.'
s2 = 'Cryptography is a method of protecting information and communications through the use of codes, so that only those for whom the information is i1tcan read and process it. The prefix "crypt-" means "hidden" or "vault" -- and the suffix "-graphy" stands for "writing." In computer science, cryptography refers to secure information and communication techniques derived from mathematical concepts and a set of rule-based calculations called algorithms, to transform messages in ways that are hard to decipher. These deterministic algorithms are used for cryptographic key generation, digital signing, verification to protect data privacy, web browsing on the internet, and confidential communications such as credit card transactions and email.'