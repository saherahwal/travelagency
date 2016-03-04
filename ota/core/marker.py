from utils import Interest

MIN_FAMILY_SCORE = 10

class BaseAbstractMarker(object):

    length1_dict = {}
    length2_dict = {}
    
    def __init__(self, hotels):
        """
            given batch of hotels to start with
        """
        self.hotels = hotels

    def clean_phrase( self, phrase ):
        """
            TODO:Should clean words from apostrophes, dashes and periods ...etc
            Now it only returns same phrase (lower case)
        """
        return phrase.lower()

    def score_word( self, word ):
        """
            score a word relative to family interest
        """        
        if word not in self.length1_dict:
            return 0
        else:
            return self.length1_dict[word]

    def score_phrase( self, phrase ):
        """
            score phrase consisting of 2 or more words
        """          
        if phrase not in self.length2_dict:
            return 0
        else:
            return self.length2_dict[phrase]

    def clean_phrase( self, phrase ):
        """
            TODO:Should clean words from apostrophes, dashes and periods ...etc
            Now it only returns same phrase (lower case)
        """
        return phrase.lower()


class FamilyInterestsMarker(BaseAbstractMarker):

    #
    # keyword score dict
    #

    length1_dict = { 'family-friendly': 100, 'playground': 65, 'garden': 45,
                     'beach' : 30, 'pool': 55 }
    length2_dict = { 'family fun' : 85, 'family activities' : 85,
                     'family entertainment' : 85, 'kids club' : 85,
                     "kids' club" : 85, 'water activities' : 70,
                     'outdoor pool' : 30, 'swimming pool' : 30 }    

    def __init__(self, hotels):      
        super( FamilyInterestsMarker, self ).__init__(hotels)                  

    def score( self, hotel ):
        """
            score the hotel
        """
        total_score = 0
        
        # split hotel desc_en by spaces - get words list
        word_list = hotel.desc_en.split(" ")

        # iterate over length1_dict to find key 1-word lengths
        index = 0
        while index < len(word_list):
            word = word_list[index]
            total_score += self.score_word( self.clean_phrase(word) )            
            index+=1

        # reset index
        index = 0
        
        # start loop for 2-word phrases 
        while index < (len(word_list)-1):
            phrase = word_list[index] + " " + word_list[index+1]
            total_score += self.score_phrase( self.clean_phrase(phrase) )            
            index+=1

        # avoid returning 0 for results search purposes
        if total_score == 0:
            return MIN_FAMILY_SCORE

        return total_score 
            
        
        
