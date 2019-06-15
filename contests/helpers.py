import os.path
import random
import string

def random_string(size, chars=string.ascii_letters+string.digits):
    return ''.join(random.SystemRandom().choice(chars) for _ in range(size))

def gen_file_name(instance, filename):
    ext = filename.split('.')[-1]
    return 'code/' + random_string(12) + '.' + ext
