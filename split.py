from split_helper import write_file, split_into_chunks, retrieve_all_chunks, join_chunks, read_chunk

def split(filename,pwd,n):
    chunks = split_into_chunks(filename,4)
    # print("The chunks are : ", chunks)
    write_file(filename,pwd,n,chunks)

def recreate_file(filename,pwd):
    chunks = retrieve_all_chunks(filename,pwd)
    data_chunk = read_chunk(filename,chunks)
    data = join_chunks(filename,data_chunk,pwd)

    print(data)