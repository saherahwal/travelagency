from utils import Interest

class FamilyInterestsMarker(object):

    def __init__(self, hotels):
        """
            given batch of hotels to start with
        """
        self.hotels = hotels
        

    def score( self, hotel ):
        """
            score the hotel
        """
        total_score = 0
        
        # split hotel desc_en by spaces - get words list
        word_list = hotel.desc_en.split(" ")

        index = 0
        while index < len(word_list):
            word = word_list[index]
            total_score += self.score_word( word )
            
            if word == "family":
                if index < len(word_list) - 1:
                    nxt_word = word_list[index+1]
                    if (nxt_word == "fun" or
                        nxt_word == "activities" or
                        nxt_word == "entertainment"):
                        total_score += 70

            index+=1

        return total_score
                

    def score_word( self, word ):
        """
            score a word relative to family interest
        """
        if word == "family-friendly":
            return 100
        else:
            return 0
            
        
        
