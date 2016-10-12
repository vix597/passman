import string
import random

class PassGen:
    '''
    Generate a cryptographically random password
    '''
    @staticmethod
    def generate(size=15, exclude_chars=""):
        '''
        Base set of 91 characters. If size=15 with no other excluded 
        characters then:
        
        uppercase + lowercase + digits + punctuation - (',",\) = 91
        
        Entropy = L * log2(N) = 15 * log2(91) ~ 97.616 bits of entropy 
        
        '''
        always_exclude="'\"\\"
        exclude_chars += always_exclude
        valid_chars = string.digits+string.ascii_lowercase+string.punctuation+string.ascii_uppercase
        valid_chars = ''.join(c for c in valid_chars if c not in exclude_chars)        
        
        '''
        SystemRandom() calls os.urandom() which is suitable for cryptographic 
        operations according to the Python documentation.
        On Windows, this will call the underlying CryptGenRandom() function
        and on Unix-like systems it will query /dev/urandom. 
        '''
        rng = random.SystemRandom()
        return ''.join(rng.choice(valid_chars) for x in range(size))