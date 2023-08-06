import hashlib
import base64
from Crypto.Cipher import AES
from pyDes import des, CBC, PAD_PKCS5
import binascii

import jwt
from datetime import datetime, timedelta

def str2hex(s):
	odata = 0;
	su = s.upper()
	for c in su:
		tmp = ord(c)
		if tmp <= ord('9'):
			odata = odata << 4
			odata += tmp - ord('0')
		elif ord('A') <= tmp <= ord('F'):
			odata = odata << 4
			odata += tmp - ord('A') + 10
	return odata

def md5(s):
	obj = hashlib.md5()
	obj.update(s.encode("UTF-8"))
	secret = obj.hexdigest()
	return secret.lower()


class aescrypt():
	def __init__(self,key,iv,model,encode_):
		self.encode_ = encode_
		self.model =  {'ECB':AES.MODE_ECB,'CBC':AES.MODE_CBC}[model]
		self.key = self.add_16(key)
		if model == 'ECB':
			self.aes = AES.new(self.key,self.model)
		elif model == 'CBC':
			self.aes = AES.new(self.key,self.model,iv)

	def add_16(self,par):
		par = par.encode(self.encode_)
		while len(par) % 16 != 0:
			par += b'\x00'
		return par

	def aesencrypt(self,text):
		text = self.add_16(text)
		self.encrypt_text = self.aes.encrypt(text)
		return base64.encodebytes(self.encrypt_text).decode().strip()

	def aesdecrypt(self,text):
		text = base64.decodebytes(text.encode(self.encode_))
		self.decrypt_text = self.aes.decrypt(text)
		return self.decrypt_text.decode(self.encode_).strip('\0')


def add_to_8(par):
	par = par.encode()
	while len(par) % 8 != 0:
		par += b'\x00'
	return par

def aes_enc(text, password, iv='', model='ECB'):
	pr = aescrypt(password, iv, model, 'gbk')
	en_text = pr.aesencrypt(text)
	return en_text

def aes_dec(text, password, iv='', model='ECB'):
	pr = aescrypt(password, iv, model,'gbk')
	en_text = pr.aesdecrypt(text)
	return en_text


def des_enc(s, key, iv='12345678'):
	des_obj = des(add_to_8(key), CBC, add_to_8(iv), pad=None, padmode=PAD_PKCS5)
	secret_bytes = des_obj.encrypt(s, padmode=PAD_PKCS5)
	return str(binascii.b2a_hex(secret_bytes), 'utf-8')


def des_dec(s, key, iv='12345678'):
	des_obj = des(add_to_8(key), CBC, add_to_8(iv), pad=None, padmode=PAD_PKCS5)
	decrypt_str = des_obj.decrypt(binascii.a2b_hex(s), padmode=PAD_PKCS5)
	return str(decrypt_str, 'utf-8')

def jwt_enc(key, content, algorithm='HS256', exp=2):
	now = datetime.utcnow()
	exp_datatime = now+timedelta(hours=exp)
	access_payload = {
		'exp':exp_datatime,
		'flag':0,
		'iat':now,
		'iss':'qin',
		'ct':content
	}
	access_token = jwt.encode(access_payload, key, algorithm=algorithm)
	return access_token


def jwt_ref(key, content, algorithm='HS256', fresh=30):
	now = datetime.utcnow()
	exp_datatime = now+timedelta(days=fresh)
	refresh_payload = {
		'exp':exp_datatime,
		'flag':1,
		'iat':now,
		'iss':'qin',
		'ct':content
	}
	refresh_payload = jwt.encode(refresh_payload, key, algorithm=algorithm)
	return refresh_payload

def jwt_dec(key, content, verify_exp=False):
	try:
		payload = jwt.decode(content, key, algorithms="HS256", options={'verify_exp':verify_exp})
	except jwt.ExpiredSignatureError:
		print("ExpiredSignatureError")
		return None
	except jwt.InvalidTokenError:
		print("InvalidTokenError")
		return None
	except jwt.InvalidSignatureError:
		print("InvalidSignatureError")
		return None
	else:
		return payload