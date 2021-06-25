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
        # adding 80 as prefix to key to state that the wif is valid for mainnet purpose
        key = '80' + private_key
        
        # converting extended private key to bytes from hex
        key_bytes = bytes.fromhex(key)
        
        # hashing extended key in bytes format with the sha256 algorithm
        hashed_key = hashlib.new('sha256', key_bytes).digest()
        
        # again hashing the hashed key with the sha256 algorithm for checksum purpose
        hashed_key = hashlib.new('sha256', hashed_key).digest()
        
        # adding checksum as postfix to extended key for base58 encoding
        key = codecs.encode(binascii.unhexlify(key), 'hex') + codecs.encode(hashed_key[:4], 'hex')
        
        # base58 encoding the extended secret key and converting back to string format
        wif = (base58.b58encode(binascii.unhexlify(key))).decode('utf-8')
        
        # verification of key
        if wif[0] == '5':
            return wif
        raise ValueError ('Something went wrong')
    
    @staticmethod
    def compress_wallet_import_format(private_key: hex) -> str:
        
        # adding 80 as prefix to key and postfix 01 to state that the wif is valid for mainnet purpose
        key = '80' + private_key + '01'
        
        # converting extended private key to bytes from hex
        key_bytes = bytes.fromhex(key)
        
        # hashing extended key in bytes format with the sha256 algorithm
        hashed_key = hashlib.new('sha256', key_bytes).digest()
        
        # again hashing the hashed key with the sha256 algorithm for checksum purpose
        hashed_key = hashlib.new('sha256', hashed_key).digest()
        
        # adding checksum as postfix to extended key for base58 encoding
        key = codecs.encode(binascii.unhexlify(key), 'hex') + codecs.encode(hashed_key[:4], 'hex')
        
        # base58 encoding the extended secret key and converting back to string format
        wif = (base58.b58encode(binascii.unhexlify(key))).decode('utf-8')
        
        # verification of key
        if wif[0] == 'K' or wif[0] == 'L':
            return wif
        raise ValueError ('Something went wrong')
        
    @staticmethod
    def private_key_to_hex(private_key_int: int) -> str:
        # convert private key (int) to hex
        return hex(private_key_int)
    
    @staticmethod
    def private_key_base64(private_key_hex: hex = None) -> str:
        # convert private key to bytes format
        private_key_bytes = bytes.fromhex(private_key_hex)
        
        # convert bytes to base64
        return (base64.b64encode(private_key_bytes)).decode('utf-8')

    @staticmethod
    def compress_public_key(public_key_x : hex, public_key_y : hex) -> str:
        # check whether the y co-ordinate of public key (hex) is even or odd
        if int(public_key_y, 16)%2 == 0:

            # adding prefix '02' to x co-ordinate of public key (hex)
            return ('02' + public_key_x[2:]).upper()
        
        # adding prefix '03' to x co-ordinate of public key (hex)
        return ('03' + public_key_x[2:]).upper()
    
    @staticmethod
    def uncompress_public_key(public_key_x : hex, public_key_y : hex) -> str:
        # concatenate both the x and y co-ordinate of public key
        x_y = public_key_x[2:] + public_key_y[2:]
        
        # adding prefix '04' to concatenated public key
        return ('04' + x_y).upper()

    @staticmethod
    def compressed_public_key_to_wallet_address(compressed_public_key: str) -> str:
        # converting compressed_public_key hex to bytes format
        if len(compressed_public_key)%2 != 0:
            compressed_public_key = '0' + compressed_public_key

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
    def decompress_public_key(comp_pubkey: str) -> str:
        # Cipolla's algorithm (https://en.wikipedia.org/wiki/Cipolla%27s_algorithm)
        # check whether the y_coordinate is even or odd
        prefix = int(comp_pubkey[:2]) - 2

        # extract x coordinate from compressed public key
        pubkey = int(comp_pubkey[2:], 16)

        # use elliptical curve to generate y
        y_square = (pow(pubkey, 3 , BitcoinStandards.primeNumber) + 7) % BitcoinStandards.primeNumber

        # find the square root of the generated y2
        y_coordinate = pow(y_square, (BitcoinStandards.primeNumber + 1)//4, BitcoinStandards.primeNumber)

        # check whether the generated y coordinate is even or odd
        if (y_coordinate % 2) != prefix:
            # if generated y coordinate is odd then the diff between primeNumber and generated y coordinate is required answer
            # else generated y coordinate is correct
            y_coordinate = (-y_coordinate) % BitcoinStandards.primeNumber

        return str(hex(y_coordinate)[2:])

    @staticmethod
    def uncompressed_public_key_to_wallet_address(uncompressed_public_key: hex) -> str:
        pass

if __name__ == '__main__':
    pass
