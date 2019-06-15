import random
from string import ascii_letters, digits

def random_string(size, chars=ascii_letters+digits):
    return ''.join(random.SystemRandom().choice(chars) for _ in range(size))

def gen_file_name(instance, filename):
    ext = filename.split('.')[-1]
    return 'code/' + random_string(12) + '.' + ext
