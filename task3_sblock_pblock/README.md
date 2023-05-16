## S-box and P-box implementation by scratch

For S-box implementation used encryption and decryption tables from the Rijndael S-box (https://en.wikipedia.org/wiki/Rijndael_S-box).
For S-box implementation, input 8-bit value splitted for two 4bit value from left to the right
```
E.g. 0111|0101
```
The table is 16 by 16 values, where intersection is 8bit value.
So, to encrypt the 01110101 value, we should choose value from the table by row_idx 0111 and column_idx 0101.

To decryption, the same process is used, by another table for decryption.

For P-box implementation, used two arrays of positions of bits to encryption and decryption:
```
    ENCRYPT_POS = (1, 5, 2, 0, 3, 7, 4, 6)
    DECRYPT_POS = (3, 0, 2, 4, 6, 1, 7, 5)
```
So, to encrypt 01110101 value, we should move bit by 1 index, to the 0 place, bit of 5 index to the 1 place etc.
