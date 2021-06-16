from curve import *
from bitcoin_standards import *
import secrets
from time import sleep

class VanityAddress:

    @staticmethod
    def address_generator(pattern = None):
        generator_point = Super256Point(BitcoinStandards.generatorPointX, BitcoinStandards.generatorPointY)
        priv_key = secrets.randbelow(BitcoinStandards.primeNumber)

        while True:
            public_key = priv_key*generator_point
            compressed_pub_key = BitcoinStandards.compress_public_key(hex(public_key.x), hex(public_key.y))
            address = BitcoinStandards.compressed_public_key_to_wallet_address(compressed_pub_key)
            if pattern :
                if address.startswith('1' + pattern):
                    print('Wallet Add : ', address, 'Private Key : ', hex(priv_key)[2:])
            else:
                print('Wallet Add : ', address, 'Private Key : ', hex(priv_key)[2:])

            priv_key += 1
            sleep(0.5)

if __name__ == '__main__':
    pass