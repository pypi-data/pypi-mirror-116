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


class AK_AES():
	def __init__(self,key,iv,model,encode_):
		self.encode_ = encode_
		self.model =  {'ECB':AES.MODE_ECB,'CBC':AES.MODE_CBC}[model]
		self.key = self.add_16(key)
		if len(self.key) in [16,24,32]:
			if model == 'ECB':
				self.aes = AES.new(self.key,self.model)
			elif model == 'CBC':
				self.aes = AES.new(self.key,self.model,iv)
		else:
			print("aes 加密密码长度需为16/24/32")

	def add_16(self,par):
		par = par.encode("utf8")
		while len(par) % 16 != 0:
			par += b'\x00'
		return par

	def enc(self,text):
		try:
			text = self.add_16(text)
			encdata = self.aes.encrypt(text)
			enctext = base64.encodebytes(encdata)
			return str(enctext, encoding='utf8').replace('\n', '')
		except Exception as e:
			print(e)
			return ""
		

	def dec(self,text):
		try:
			text = base64.decodebytes(text.encode("utf8"))
			decrypt_bytes = self.aes.decrypt(text)
			dec_text = str(decrypt_bytes, encoding='utf-8')
			return dec_text
		except Exception as e:
			print(e)
			return ""

class AK_DES():
	def add_to_8(par):
		par = par.encode()
		while len(par) % 8 != 0:
			par += b'\x00'
		return par

	def des_enc(self,s, key, iv='12345678'):
		des_obj = des(self.add_to_8(key), CBC, self.add_to_8(iv), pad=None, padmode=PAD_PKCS5)
		secret_bytes = des_obj.encrypt(s, padmode=PAD_PKCS5)
		return str(binascii.b2a_hex(secret_bytes), 'utf-8')


	def des_dec(self,s, key, iv='12345678'):
		des_obj = des(self.add_to_8(key), CBC, self.add_to_8(iv), pad=None, padmode=PAD_PKCS5)
		decrypt_str = des_obj.decrypt(binascii.a2b_hex(s), padmode=PAD_PKCS5)
		return str(decrypt_str, 'utf-8')

class AK_JWT():
	def enc(self, content, key, algorithm='HS256', exp=2):
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


	def ref(self, content, key , algorithm='HS256', fresh=30):
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

	def dec(self,content,key , verify_exp=False):
		try:
			payload = jwt.decode(content, key, algorithms="HS256", options={'verify_exp':verify_exp})
			return payload["ct"]
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


def aes_enc_ecb(text, password, iv=''):
	pr = AK_AES(password, iv, "ECB", 'utf8')
	en_text = pr.enc(text)
	return en_text

def aes_dec_ecb(text, password, iv=''):
	pr = AK_AES(password, iv, "ECB",'utf8')
	en_text = pr.dec(text)
	return en_text

def aes_enc_cbc(text, password, iv=''):
	pr = AK_AES(password, iv, "CBC", 'utf8')
	en_text = pr.enc(text)
	return en_text

def aes_dec_cbc(text, password, iv=''):
	pr = AK_AES(password, iv, "CBC",'utf8')
	en_text = pr.dec(text)
	return en_text


def jwt_enc(text, password):
	pr = AK_JWT()
	return pr.enc(text, password)

def jwt_dec(text, password):
	pr = AK_JWT()
	return pr.dec(text, password)
