import binascii
import base58
import base64
import hashlib
import codecs

class BitcoinStandards:
    primeNumber = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    generatorPointX = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
    generatorPointY = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
    orderOfFieldElements = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
    
    @staticmethod
    def uncompress_wallet_import_format(private_key: hex) -> str:
        key = '80' + private_key
        key_bytes = bytes.fromhex(key)
        hashed_key = hashlib.new('sha256', key_bytes).digest()
        hashed_key = hashlib.new('sha256', hashed_key).digest()
        key = codecs.encode(binascii.unhexlify(key), 'hex') + codecs.encode(hashed_key[:4], 'hex')
        wif = (base58.b58encode(binascii.unhexlify(key))).decode('utf-8')
        if wif[0] == '5':
            return wif
        raise ValueError ('Something went wrong')
    
    @staticmethod
    def compress_wallet_import_format(private_key: hex) -> str:
        key = '80' + private_key + '01'
        key_bytes = bytes.fromhex(key)
        hashed_key = hashlib.new('sha256', key_bytes).digest()
        hashed_key = hashlib.new('sha256', hashed_key).digest()
        key = codecs.encode(binascii.unhexlify(key), 'hex') + codecs.encode(hashed_key[:4], 'hex')
        wif = (base58.b58encode(binascii.unhexlify(key))).decode('utf-8')
        if wif[0] == 'K' or wif[0] == 'L':
            return wif
        raise ValueError ('Something went wrong')
        

    @staticmethod
    def private_key_to_hex(private_key_int: int) -> str:
        return hex(private_key_int)
    
    @staticmethod
    def private_key_base64(private_key_hex: hex = None) -> str:
        private_key_bytes = bytes.fromhex(private_key_hex)
        return (base64.b64encode(private_key_bytes)).decode('utf-8')

    @staticmethod
    def compress_public_key(public_key_x : hex, public_key_y : hex) -> str:
        if int(public_key_y, 16)%2 == 0:
            return ('02' + public_key_x[2:]).upper()
        return ('03' + public_key_x[2:]).upper()
    
    @staticmethod
    def uncompress_public_key(public_key_x : hex, public_key_y : hex) -> str:
        x_y = public_key_x[2:] + public_key_y[2:]
        return ('04' + x_y).upper()

    @staticmethod
    def compressed_public_key_to_wallet_address(compressed_public_key: str) -> str:
        # converting compressed_public_key hex to bytes format
        public_key_bytes = bytes.fromhex(compressed_public_key)

        # hashing public_key_bytes with the sha256 algorithm
        sha_hash = hashlib.new('sha256', public_key_bytes).digest()

        # hashing hashed_sha256_bytes with the ripemd160 algorithm
        mainnet_key = hashlib.new('ripemd160', sha_hash).digest()

        # adding 00(main network identifier) as prefix to hex of hashed ripemd160
        mainnet_key = b'00' + codecs.encode(mainnet_key, 'hex')
        
        # creating copy of extended mainnet_key for future purpose (for checksum)
        mainnet_key_copy = mainnet_key

        # converting extended mainnet_key bytes to ascii characters
        mainnet_key = binascii.unhexlify(mainnet_key)

        # hashing extended mainnet_key format with the sha256 algorithm
        mainnet_key = hashlib.new('sha256', mainnet_key).digest()

        # hashing hashed extended mainnet_key with the sha256 algorithm
        mainnet_key = hashlib.new('sha256', mainnet_key).digest()

        # postfix first 4 bytes of 2nd hashed extended mainnet_key to copy of extended mainnet_key
        address = mainnet_key_copy.decode('utf-8') + codecs.encode(mainnet_key[:4], 'hex').decode('utf-8')

        # converting the result to base58 format
        base_address = base58.b58encode(binascii.unhexlify(address))
        
        return base_address.decode('utf-8')


    @staticmethod
    def uncompressed_public_key_to_wallet_address(uncompressed_public_key: hex) -> str:
        pass

if __name__ == '__main__':
    pass