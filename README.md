# File Split Cryptography

File security has become one of the most important aspects of cyber-security. As the value of data soares, data files are becoming more and more vulnerable. Database systems are becoming targets for hackers to get data. Surprisingly, personal laptops are becoming new targets as well. Personal laptops are a source of great personal data. Ransomwares are a common thing now which affects all systems part of the network as well as personal laptops. Current systems of protection for files are primitive and not sufficient to keep the files away from wrong files. As the estimation of information soares, information files are getting increasingly defenseless. Information base frameworks like Databases are turning out to be focused for programmers to get information. Surprisingly, individual workstations are turning out to be new focuses also.

We are proposing a new system of protecting files where the file is split into chunks and each chunk is encrypted. This prevents the hacker from getting the data even if he manages to hack the computer. When the user wants to access the file, all the chunks are then brought together to recreate the original file.The file system, thus only allows the user when they know the exact combination of the filename and password to open the file. Also, since we are using a symmetric encryption key algorithm, no keys will be made public and thus no malicious hackers can eavesdrop or break into the system to tamper with files. Even in the case of loss of files or chunks, we can retrieve original file contents by use of parity blocks and erasure coding when a threshold of 2 files or less have been lost or deleted. The system is expected to offer the highest level of security to files and their integrity with the best possible encryption and hashing mechanisms in practice.

##  Methodology
### METHODOLOGY COMPONENTS:
1. File-splitting – Each file will be broken into 4 chunks and each chunk will be of the same size. If the content size is not a multiple of 4, we pad the content with extra bytes.
2. Filename generation – Our file system creates the name of the file on the go. This makes it less vulnerable and hard to guess. The name of the chunk is created as a random string.
```
Root filename = hash(filename XOR password)
chunk<i> = hash(chunk<i-1> XOR Password) ( 1 <i< 4 )
```
3. File Encryption – All files will be encrypted individually i.e. no same key will be used for all the chunks. We borrow an essential component from blockchain for our file encryption. Each chunk’s decryption key will be generated from the previous chunk. This makes it difficult for the attacker to access files at random and try to decrypt.
4. Merkle Tree – From the content of the 4 chunks, we create a merkle root and save it in MongoDB. We can check this merkle root while recreating the chunk to check whether the
5. Erasure coding – We have implemented 4-2 erasure coding. We encode all the chunks and using 2 predefined linear equations, we create 2 parity blocks and save them in the file system. Even the parity files are uniquely named. This is used as a redundancy method.
If a maximum of 2 files are tampered or deleted from the filesystem, we can recreate the missing chunks using parity blocks and erasure coding.

## Flowchart
![Sharding](/misc/shard.png)
![Recreating](/misc/recreate.png)



### The report has full details about the project (/report.pdf)


