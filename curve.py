from bitcoin_standards import *

prime_number = BitcoinStandards.primeNumber

class ValidFieldElement:
    def __init__(self, num=None, prime=prime_number):
        if num >= prime or num < 0:
            error = f'{num} is not in range {prime}'
            raise ValueError(error)
        self.num = num
        self.prime = prime
        
    def __eq__(self, other):
        if other.num is None or other.prime is None:
            return False
        return self.num == other.num and self.prime == other.prime

class Super256Field(ValidFieldElement):

    def __init__(self, num, prime=None):
        super().__init__(num, prime=prime_number)

    def __repr__(self):
        return '{:x}'.format(self.num).zfill(64)

class ValidPoint:
    def __init__(self, x, y, a=0, b=7):
        self.x = x.num if x else None        
        self.y = y.num if y else None
        self.a = a
        self.b = b

        if x is not None:
            if pow(self.y, 2, prime_number) != (pow(self.x, 3, prime_number) + 7)%prime_number:
                raise ValueError(f'({self.x}, {self.y}) not on the curve')
        
    def __add__(self, other):
        
        if self.a != other.a or self.b != other.b:
            raise TypeError(f'Points {(self.x, self.y)}, {(other.x, other.y)} are not the curve.')

        elif self.x is None:
            return other

        elif other.x is None:
            return self

        elif self == other and self.y == 0*self.x:
            return self.__class__(None, None)

        elif self.x == other.x:
            s = ((3*pow(self.x, 2, prime_number))*(pow(2*self.y, prime_number-2, prime_number)))
            x_final = ((s**2) - ((2*(self.x%prime_number))%prime_number))%prime_number
            y_final = (((s*((self.x - x_final)%prime_number))%prime_number - (self.y%prime_number))%prime_number)%prime_number
            other_x = int(x_final)%prime_number
            other_y = int(y_final)%prime_number
            return self.__class__(other_x, other_y)

        else:
            s = (((other.y - self.y)%prime_number) * (pow((other.x - self.x), prime_number-2, prime_number)))%prime_number
            x_final = ((s**2) - (self.x + other.x))%prime_number
            y_final = (s*(self.x - x_final) - (self.y))%prime_number
            other_x = int(x_final)%prime_number
            other_y = int(y_final)%prime_number
            return self.__class__(other_x, other_y)

    def __eq__(self, other):
        return self.y == other.y and self.x == other.x

    def __rmul__(self, coefficient):
        coef = coefficient
        current = self
        result =  self.__class__(None, None, 0, 7)

        while coef:
            if coef & 1:
                result = current + result
            current += current
            coef >>= 1
        return result


class Super256Point(ValidPoint):
    
    def __init__(self, x, y, a=0, b=7):
        a, b = Super256Field(a), Super256Field(b)
        if type(x) == int:
            super().__init__(x=Super256Field(x), y=Super256Field(y), a=a, b=b)
        else:
            super().__init__(x, y, a, b)

    def __rmul__(self, coefficient):
        coef = (coefficient % prime_number)

        return super().__rmul__(coef)

if __name__ == '__main__':
    pass