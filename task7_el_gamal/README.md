Provided code contains two classes, that implements ElGamel signature and encryption.
The main contains test for verification the implementation.

Code output:
```Verify string to int convertion (and backwards)
Original str: hello; Converted: 448378203247; Encrypted: hello

I. ElGamelSignature
Private key: 72757217426062277; Public key: 142903843160289740

 1. Test: original priv_key, original pub_key, original message
Verify validation for original pub_key and message: True

 2. Test: original priv_key, original pub_key, another message:
	Original message=803971281974815818693763305215424696387865746139
	Updated message=803971281974815818693763305215424696387865746140
Verify validation for original pub_key, but another message: False

 3. Test: another priv_key, original pub_key (not that calculates from the current priv_key), orig message:
Verify validation for wrong pub_key (another priv_key used): False


II. ElGamelEncryption
Private key: 17612; Public key: 1253
Original message: 12345
Encrypted message (two components): (58386, 49503)
Encrypted message: 12345
Does original message equal to encrypted True


1. Test: Encrypt and decrypt by original priv and pub key pairs
Original message: Distribution lab the best!
Encrypted message (two components): [(25905, 31928), (54179, 65820), (24151, 25075), (18352, 8766), (70688, 71672), (67146, 30986), (4278, 84825), (55232, 75830), (84525, 41300), (9794, 42100), (16101, 30249), (74385, 68216), (74614, 31044)]
Encrypted message: Distribution lab the best!
Does original message equal to encrypted True


2. Test: Encrypt by original priv and pub key pairs, but try to encrypt by another priv key
Original message: Distribution lab the best!
Encrypted message (two components): [(24262, 49814), (81734, 26251), (87385, 47159), (85838, 783), (61851, 63235), (25215, 83170), (83920, 76844), (77286, 72095), (64612, 46870), (49352, 60169), (72769, 81005), (85459, 62773), (17333, 86383)]
Orig priv key: 17612; Wrong priv_key: 17622
Encrypted message: ZÂcþÕÝ´DXVÖ³±éq@®
Does original message equal to encrypted False```
