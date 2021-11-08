import blake3

hash1 = str(blake3.blake3(b"Vivek Mehta").digest().hex())
f = open(hash1 + ".txt", "w")
f.close()
print(len(hash1))