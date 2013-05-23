'''This Script is copied from Wikipedia to check 
  validity of ISBN numbers.  '''

# Check Validity of ISBN-10
def is_isbn10(isbn10):
    if len(isbn10) != 10:
        return False
    r = sum((10 - i) * (int(x) if x != 'X' else 10) for i, x in enumerate(isbn10))
    return r % 11 == 0

# Check Validity of ISBN-13
def is_isbn13(isbn13):
    total = sum(int(num) * weight for num, weight in zip(isbn13, (1, 3) * 6))
    ck = (10 - total) % 10
    return ck == int(isbn13[-1])

