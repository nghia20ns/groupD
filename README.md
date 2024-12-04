# Install app

#### `git clone https://github.com/nghia20ns/TextSteago.git`

# run app

### using GUI

#### `python main.py`

![alt text](image.png)

### using command line

#### `python SteagoNoGUI.py`

![alt text](image-1.png)

# Zero-With algorithm

## Chuyển đổi văn bản sang nhị phân và mã hóa

Đoạn mã này thực hiện việc mã hóa văn bản bằng cách chuyển đổi các ký tự trong văn bản sang mã nhị phân và sử dụng các ký tự Zero-Width để giấu thông tin:

```python
def txt_encode(text):
    l = len(text)
    i = 0
    add = ''
    while i < l:
        t = ord(text[i])
        if 32 <= t <= 64:
            t1 = t + 48
            t2 = t1 ^ 170  # 170: 10101010
            res = bin(t2)[2:].zfill(8)
            add += "0011" + res
        else:
            t1 = t - 48
            t2 = t1 ^ 170
            res = bin(t2)[2:].zfill(8)
            add += "0110" + res
        i += 1
    res1 = add + "111111111111"  # Delimiter to indicate end of message
    print("The string after binary conversion appyling all the transformation :- " + res1)
    length = len(res1)
    print("Length of binary after conversion:- ", length)
    HM_SK = ""
    ZWC = {"00": u'\u200C', "01": u'\u202C', "11": u'\u202D', "10": u'\u200E'}
    file1 = open("cover_text.txt", "r+")
    nameoffile = input("\nEnter the name of the Stego file after Encoding(with extension):- ")
    file3 = open(nameoffile, "w+", encoding="utf-8")
    word = []
    for line in file1:
        word += line.split()
    i = 0
    while i < len(res1):
        s = word[int(i / 12)]
        j = 0
        x = ""
        HM_SK = ""
        while j < 12:
            x = res1[j + i] + res1[i + j + 1]
            HM_SK += ZWC[x]
            j += 2
        s1 = s + HM_SK
        file3.write(s1)
        file3.write(" ")
        i += 12
    t = int(len(res1) / 12)
    while t < len(word):
        file3.write(word[t])
        file3.write(" ")
        t += 1
    file3.close()
    file1.close()
    print("\nStego file has successfully generated")
```

## Kiểm tra khả năng mã hóa và thực hiện mã hóa

Đoạn mã này kiểm tra xem có đủ không gian trong văn bản để giấu thông tin hay không, nếu có thì tiến hành mã hóa thông tin:

```python
def encode_txt_data():
    count2 = 0
    file1 = open("cover_text.txt", "r")
    for line in file1:
        for word in line.split():
            count2 += 1
    file1.close()
    bt = int(count2)
    print("Maximum number of words that can be inserted :- ", int(bt / 6))
    text1 = input("\nEnter data to be encoded:- ")
    l = len(text1)
    if l <= bt:
        print("\nInputed message can be hidden in the cover file\n")
        txt_encode(text1)
    else:
        print("\nString is too big please reduce string size")
        encode_txt_data()
```

# Chuyển đổi nhị phân sang thập phân

Đoạn mã này chuyển đổi chuỗi nhị phân thành số thập phân:

```python
def BinaryToDecimal(binary):
    string = int(binary, 2)
    return string
```

## Giải mã thông tin từ văn bản

Đoạn mã này giải mã thông tin từ văn bản "Stego" bằng cách trích xuất và chuyển đổi các ký tự Zero-Width trở lại dạng nhị phân và sau đó chuyển đổi từ nhị phân về ký tự gốc:

```python
def decode_txt_data():
    ZWC_reverse = {u'\u200C': "00", u'\u202C': "01", u'\u202D': "11", u'\u200E': "10"}
    stego = input("\nPlease enter the stego file name(with extension) to decode the message:- ")
    file4 = open(stego, "r", encoding="utf-8")
    temp = ''
    for line in file4:
        for words in line.split():
            T1 = words
            binary_extract = ""
            for letter in T1:
                if letter in ZWC_reverse:
                    binary_extract += ZWC_reverse[letter]
            if binary_extract == "111111111111":
                break
            else:
                temp += binary_extract
    print("\nEncrypted message presented in code bits:", temp)
    lengthd = len(temp)
    print("\nLength of encoded bits:- ", lengthd)
    i = 0
    a = 0
    b = 4
    c = 4
    d = 12
    final = ''
    while i < len(temp):
        t3 = temp[a:b]
        a += 12
        b += 12
        i += 12
        t4 = temp[c:d]
        c += 12
        d += 12
        if t3 == '0110':
            decimal_data = BinaryToDecimal(t4)
            final += chr((decimal_data ^ 170) + 48)
        elif t3 == '0011':
            decimal_data = BinaryToDecimal(t4)
            final += chr((decimal_data ^ 170) - 48)
    print("\nMessage after decoding from the stego file:- ", final)
```

### Chương trình này thực hiện việc giấu thông tin trong văn bản một cách tinh vi bằng cách sử dụng các ký tự Zero-Width, giúp thông tin được giấu kín mà không làm thay đổi đáng kể nội dung văn bản gốc.
"# groupD" 
