
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import hashlib

# AES128-ECB模式加密
def AES128_en(data, key):
  print("加密前data:" + data)
  print("加密key:" + key)
  BS = AES.block_size
  pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
  AESCipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
  data = pad(data).encode('utf-8')
  encryptcipher = str(b2a_hex(AESCipher.encrypt(data)), "utf-8")
  return encryptcipher


# AES128-ECB模式解密
def AES128_de(data, key):
  # key = bytes(key, 'utf-8')
  unpad = lambda s: s[:-ord(s[len(s) - 1:])]
  AESCipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
  paint = unpad(AESCipher.decrypt(a2b_hex(data)))
  # print(str(paint, encoding="utf-8"))
  return bytes.decode(paint)  # bytes类型转成string类型


# oder=aes128encrypt（oder,aes128decrypt(key, md5（appKey）的前16位)）key是登陆返回的

'''
data1 = "-90,90,1,0,86,0,32,0,59,0,0,0,80,0,55,16,1,2,23,20,-45,88,0,0,0,-65,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-86,29,-84,0,0,0,0,0,2,2,-80,2,26,0,1,1,60,2,8,1,2,102,102,54,0,0,0,113,-74,-13,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
data2 = "ebd036cd241dc82a9f67795b65978ecf187c944f79041a1b4b632650e1b4aed9"
Iot_key = "ad0ee21d48a64bf49f4fb583ab76e799"
md5key = hashlib.md5()
md5key.update(Iot_key.encode('utf-8'))
md5_key = md5key.hexdigest()
print(md5_key)
md5_key = md5_key[0:16]
print(md5_key)
AES128_1 = AES128_de(data2, md5_key)
AES128_2 = AES128_en(data1, AES128_1)
print("加密后的内容", AES128_2)
'''
data1 = "c5db3c04b26b67602400e54ee8bf0a95187c944f79041a1b4b632650e1b4aed9"
# data3 = "377cb30aa4b829dd919c8c48df635f77a1f9452bd0b3a9c21d9fe9814c0dc5df"   # 国际美居key
data2 = "cdadbd7bbb86abbb775eb29dcd31152497d9d67e36b2435de014508d0dfff8c473e6e6284b6cf824af98a7699c9ca479ae40fc163789b5da66bee4d842d878cf0a585a85b716eb2d8d99df1adc2acbd468caabb3c45d7b63d24d12d164703309ae6599f062d41555110460ceceb402c139f216928c3a7b519468d043f2bdb9f62b6817a08ca424b9a468023652cf60719e49aa0b29f28f95d87f1d8844ac599b68caabb3c45d7b63d24d12d164703309c8379e99730f633f39d8033a868c6e6c75acaa0e9c949861f132314ecc87b9cffaff80d4a869a89398b067403a7c52cda8df8b7db49d7438ddf146f52d405f9fc823eca043bb3b5f32af3daff2a56762b550e38b5b81f12ed49dec8ba10ac984"
md5_Iotkey = "96c7acdfdb8af79a"
re1 = AES128_de(data1, md5_Iotkey)
print(re1)
re2 = AES128_de(data2, re1)
print(re2)
print(type(re2))