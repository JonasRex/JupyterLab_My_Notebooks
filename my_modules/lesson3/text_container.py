import string

class TextContainer():
    """First attempt to make a class."""
    
    def __init__(self, my_text):
        """Initialize my_text"""
        self.my_text = my_text
        
    def __repr__(self) -> str:
        return 'TextContainer(%r)' % (self.my_text)
    
    def __str__(self) -> str:
        return '{text}.'.format(
            text=self.my_text)
    
        
    def words_amount(self):
        """Function that returns the amount of words in a text."""
        return len(self.my_text.split(" "))
    
    def chars_amount(self):
        """Function that returns the amount of characters in a text."""
        return len(list(self.my_text))
    
    def letters_amount(self):
        """Function that returns the amount of (ascii) letters in a text."""
        letters = 0
        for char in list(self.my_text):
            for ascii in string.ascii_lowercase:
                if char.lower() == ascii:
                    letters += 1
        
        return letters
    
    def letters_amount_v2(self):
        """Function (version 2) that returns the amount of (ascii) letters in a text, made with a list comprehension instead of double for loop.""" 
        return len([letter 
                   for letter in list(self.my_text) 
                   for ascii in string.ascii_lowercase 
                   if letter.lower() == ascii])
    
    
    def letters_amount_v3(self):
        """Function (version 3) that returns the amount of (ascii) letters in a text, made with a list comprehension and function that check if char is an ascii."""
        def is_ascii(character):
            for ascii in string.ascii_lowercase:
                if character.lower() == ascii:
                    return True
            return False 
        
        return len([letter for letter in list(self.my_text) if is_ascii(letter)])
    
    
    def remove_punctuation(self):
        """Function that removes all punctuation chars and returns a new 'clean' string """
        def is_punctuation(character):
            for punc in string.punctuation:
                if character == punc:
                    return True
            return False 
            
            
        return ''.join([char 
                   for char in list(self.my_text) 
                   if not is_punctuation(char)])
    
    