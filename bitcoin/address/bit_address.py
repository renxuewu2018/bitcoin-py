#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: xwren
# @Email:  seektolive@gmail.com
# @Date:   2018-01-26 09:00:25
# @Last Modified by:   xwren
# @Last Modified time: 2018-02-02 09:54:56


import hashlib
from binascii import hexlify,unhexlify
from base58 import b58encode,b58encode_check
import os
import ecdsa
import base58

# 普通地址P2PKH的版本默认值是0，P2SH类型的地址版本默认值是5
version = 0
'''
根据公钥生成比特币地址，椭圆曲线签名算法里的私钥由32字节随机数组成，
通过私钥可以算出公钥，公钥经过一系列哈希算法及编码算法就得到了比特币中的地址。
因此地址其实是公钥的另一种表现形式，可以理解为公钥的摘要。
hexlify：先把字符串转换成二进制数据然后在用十六进制表示
unhexlify：与hexlify相反
'''
def generate_btcaddress(pub_key):
	ripemd160 = hashlib.new('ripemd160')
	ripemd160.update(hashlib.sha256(unhexlify(pub_key)).digest())
	hashed_public_key = b"00" + hexlify(ripemd160.digest())
	checksum = hexlify(hashlib.sha256(hashlib.sha256(unhexlify(hashed_public_key)).digest()).digest()[:4])
	binary_addr = unhexlify(hashed_public_key + checksum)
	address = base58.b58encode(binary_addr)
	return address

def generate_address():
	pik = generate_privatekey()
	puk = generate_publickey_from_privatekey(pik)
	ripemd160_key = generate_hashdata(puk)
	hash_21 = generate_hash_data21(ripemd160_key)
	hash_25 = generate_hash_data25(hash_21)
	btc_address = generate_addr(hash_25)
	print(btc_address)

def double_sha256(hash_data_21):
	return hashlib.sha256(hashlib.sha256(unhexlify(hash_data_21)).digest()).digest()

# 1.generate private key
def generate_privatekey():
	return os.urandom(32)


# 2. generate public key
def generate_publickey_from_privatekey(pik):
	sk = ecdsa.SigningKey.from_string(pik, curve=ecdsa.SECP256k1)
	vk = sk.verifying_key
	public_key = b"04" + hexlify(vk.to_string()) # TODO why add 04
	return public_key
# 3. generate hash160 20
def generate_hashdata(puk):
	# 1. SHA256(K) 将公钥通过SHA-256哈希算法处理，
	# 得到32字节的哈希值)(first_hash.digest_size)
	hash256 = hashlib.sha256(unhexlify(puk))
	hash256_key = hash256.digest()
	# 2. RIPEMD160(SHA256(K))
	# 对于得到的哈希值，通过RIPEMD-160算法来得到20字节的哈希值--Hash160
	ripemd160 = hashlib.new('ripemd160')
	ripemd160.update(hash256_key)
	ripemd160_key = ripemd160.digest()
	return ripemd160_key

# 4. 把由版本号+hash160（ripemd160）组成的21字节数据
def generate_hash_data21(ripemd160_key):
	return  b'00' + hexlify(ripemd160_key)
# 5. 得到哈希值的前4字节作为校验和，放置在21字节数据的末尾
def generate_hash_data25(hash_data_21):
	double_sha256_str = double_sha256(hash_data_21)[:4]
	return unhexlify(hash_data_21+hexlify(double_sha256_str))


# 6. 对组成的25字节数组进行Base58编码，得到地址
def generate_addr(hash_data_25):
	return base58.b58encode(hash_data_25)

def main():
	# key = generate_btcaddress('0450863AD64A87AE8A2FE83C1AF1A8403CB53F53E486D8511DAD8A04887E5B23522CD470243453A299FA9E77237716103ABC11A1DF38855ED6F2EE187E9C582BA6')
	# print(key)

	generate_address()

if __name__ == '__main__':
	main()
	# Public key: 0202a406624211f2abbdc68da3df929f938c3399dd79fac1b51b0e4ad1d26a47aa
	# e35f5e5e8f822ba75e86f0c2a973817e6117adbf5598f98766ae66e12d32421f
	# 1CS5vyE4dJjv1dzdrqcsFiWHHdcDPhcXc4
	# address: 1PRTTaJesdNovgne6Ehcdu1fpEdX7913CK
	# 16UwLL9Risc3QfPqBUvKofHmBQ7wMtjvM
