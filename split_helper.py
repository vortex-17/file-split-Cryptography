import hashlib
import os
import sys
from mongo_utils import insert_into_mongo, find_mongo
import erasure
import glob

def encrypt(data,key):
    encrypted_text = ""
    # print("Key : ",key)
    key = 0
    for i in str(key)[:5]:
        key += ord(i)
    for i in data:
        encrypted_text += chr(ord(i) + key)

    return encrypted_text

def decrypt(data,key):
    decrypted_text = ""
    key = 0
    for i in str(key)[:5]:
        key += ord(i)
    for i in data:
        decrypted_text += chr(ord(i) - key)

    return decrypted_text

def hash_data(data):
    result = hashlib.sha1(data.encode()) 
    return result.hexdigest()

def key_gen(data):
    #temp solution
    key_text = data[:10]
    return hash_data(key_text)

def string_xor(string1,string2):
    num1 = ""
    for i in string1:
        num1 += str(ord(i))
    num2 = ""
    for i in string2:
        num2 += str(ord(i))
    # print(string1,string2,num1,num2)
    return int(num1) ^ int(num2)

def check_file_string(filename):
    pass

# def create_merkle_DAG(chunks):
#     chunk_hash = []
#     root_hash = hash_data(str(chunks[0]))
#     chunk_hash.append(root_hash)
#     prev_hash = root_hash
#     for i in range(1,len(chunks)):
#         curr_hash = str(hash_data(chunks[i] + str(prev_hash)))
#         chunk_hash.append(curr_hash)
#         prev_hash = curr_hash

#     return chunk_hash
    
def create_merkle_root(chunks):
    """
    This function will calculate the merkle root of the file 
    and this will be used to compare with the merkle root saved in 
    DB to check whether the file has been modified.
    """
    # print(chunks)
    if len(chunks) == 1:
        root = chunks[0]
        return root

    chunk_hash = []
    for i in range(0,int(len(chunks)/2)):
        chunk_hash.append(str(hash_data(chunks[2*i] + chunks[2*i+1])))

    return create_merkle_root(chunk_hash)

    

def split_into_chunks(filename, n_chunks = 4):
    """
    This function reads from the given file and
    divides them into chunks. It also provides padding if required.
    """
    f = open(filename, "r")
    file_data = f.read()
    length_of_file = len(file_data)
    print("The total characters in the file is : ",length_of_file)

    data_list = [] #The list will contain the chunks of data
    size_of_chunk = int(length_of_file/n_chunks) + 1
    print("Size of each chunk : ", size_of_chunk)

    for i in range(n_chunks):
        data_list.append(file_data[i * size_of_chunk : (i+1) * size_of_chunk])

    # print(len(data_list))
    if len(data_list[-1]) < size_of_chunk :     #To have all chunks of equal length. 
        data_list[-1] +=  "#" * (size_of_chunk - len(data_list[-1]))

    f.close()
    return data_list

def proof_of_storage():
    pass

def proof_of_auth(filename, merkle_root):
    root = find_mongo(filename)
    if root == None:
        print("No file found with that name.")
        return False
    if merkle_root == root:
        return True
    else:
        return False


#this will create the name of the chunks 
def create_filename(file_string, pwd = "password", n = 1):
    file_list = []
    x = string_xor(file_string,pwd)
    for i in range(n):
        x += i
        file_hash = str(hash_data(str(x))) + ".txt"
        file_list.append(file_hash)

    return file_list

def create_parity_files(filename, p1,p2):
    filename_p1 = hash_data(filename + "parity1") + ".txt"
    filename_p2 = hash_data(filename + "parity2") + ".txt"
    f = open(filename_p1, "w")
    f.write(str(p1))
    f.close()

    f = open(filename_p2, "w")
    f.write(str(p2))
    f.close()

def read_parity(filename):
    filename_p1 = hash_data(filename + "parity1") + ".txt"
    filename_p2 = hash_data(filename + "parity2") + ".txt"
    f = open(filename_p1, "r")
    p1 = int(f.read())
    f.close()

    f = open(filename_p2, "r")
    p2 = int(f.read())
    f.close()

    return p1,p2

    
def write_file(file_name,pwd,n,file_chunks):
    if file_name == "":
        exit(1)
    hash_of_data = []
    enc_data = []
    filename = file_name
    file_name = file_name
    # print(len(file_chunks))
    for data in file_chunks:
        print(data)
        # enc_data.append(erasure.encode(data))
        key = key_gen(data)
        hash_of_data.append(str(hash_data(data)))
        file_list = create_filename(file_name,pwd,1)
        for file_ in file_list:
            f = open(file_, "w")
            enc_d = encrypt(data,key)
            f.write(enc_d)
            enc_data.append(erasure.encode(enc_d))
            print(enc_d + "/")
            f.close()
        
        file_name = file_list[0]
    
    merkle_root = create_merkle_root(hash_of_data)
    print("Merkle Root after Encryption :  ",merkle_root)
    
    #Creating Parity Bits
    # print("Encoded version : ", enc_data)
    p1,p2 = erasure.create_parity_block(enc_data)
    # print("Parity Bits : ", p1,p2)
    create_parity_files(filename,p1,p2)


    insert_into_mongo(filename, merkle_root)
    return merkle_root


def retrieve_chunk(filename, pwd):
    if filename == "":
        exit(1)

    # print(filename)
    root_filename = string_xor(filename, pwd)
    # print(root_filename)
    found = False
    root_chunk = None
    for i in range(1): #Max redundancy is 4
        root = root_filename
        root += i
        root_chunk = str(hash_data(str(root))) + ".txt"
        found = find_file(root_chunk)
        if found == True:
            return True,root_chunk

    
    if found == False:
        print("None of the chunks of the file could be found. Somebody has tampered with your file system.")
        return False,root_chunk
        # exit(1)

    return False,root_chunk

def retrieve_all_chunks(filename, pwd):
    all_chunks = []
    no_of_chunks = 4
    file_chunk = filename
    for i in range(no_of_chunks):
        valid,file_ = retrieve_chunk(file_chunk,pwd)
        # print(file_)
        if valid == False:
            print("Chunk Missing")
            all_chunks.append("")
        elif valid == True:
            all_chunks.append(file_)
            
        else:
            print("Could not retrieve the file. File Chunk Missing.")
            exit(1)
        file_chunk = file_
    
    missing = all_chunks.count("")

    # print(all_chunks)
    return all_chunks

def read_chunk(filename,chunks):
    data = []
    for i in chunks:
        if i != "":
            f = open(i, "r")
            data.append(f.read())
            f.close()

        else:
            data.append("")

    # print("Data : ", data)
    missing = data.count("")
    if missing > 0 and missing <= 2:
        p1,p2 = read_parity(filename)
        # print("Data : ", data)
        # print("Parity 1 : ", p1)
        # print()
        # print("Parity 2 : ", p2)
        data = erasure.find(data,p1,p2)

    return data

def join_chunks(filename,chunks_list,pwd):
    original_text = ""
    chunks_of_data = []
    key = pwd

    #finding missing values
    for i in chunks_list:
        data = decrypt(i,key)
        chunks_of_data.append(hash_data(data))
        original_text += data
        key = key_gen(data)


    merkle_root = create_merkle_root(chunks_of_data)
    print("Merkle Root after Decryption :  ",merkle_root)
    #check the Mongo DB for the merkle root
    valid = proof_of_auth(filename, merkle_root)
    if valid == False:
        print("There has been some tampering with the File.")

    return original_text

# def join_chunks(filename,chunks_list,pwd):
#     original_text = ""
#     chunks_of_data = []
#     key = pwd

#     #finding missing values
#     missing = chunks_list.count("")
#     if missing > 0 and missing <= 2:
#         print("Missing Chunks")
#         for i in chunks_list:
#             pass

#     for i in chunks_list:
#         f = open(i, "r")
#         encrypted_data = f.read()
#         data = decrypt(encrypted_data,key)
#         chunks_of_data.append(hash_data(data))
#         original_text += data
#         key = key_gen(data)
#         f.close()


#     merkle_root = create_merkle_root(chunks_of_data)
#     print("Merkle Root after Decryption :  ",merkle_root)
#     #check the Mongo DB for the merkle root
#     valid = proof_of_auth(filename, merkle_root)
#     if valid == False:
#         print("There has been some tampering with the File.")

#     return original_text


def find_file(filename):
    file_list = list(glob.glob("*.txt"))
    if filename in file_list:
        return True
    else:
        return False


def logs():
    pass