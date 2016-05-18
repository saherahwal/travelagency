from utils import *
from nltk import word_tokenize 

MIN_SCORE = 10

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
   

class GeneralMarker(object):

    def __init__(self, markerList):
        """
            init with list of markers
        """
        self.scores = {}
        self.markerList = markerList

        # init scores
        for marker in markerList:
            self.scores[ marker.name ] = MIN_SCORE

    def isNoScoreAssigned( self ):
        """
            Returns true if only scores assigned was minimum. Returns false otherwise 
        """
        for marker in self.markerList:
            if self.scores[ marker.name ] > MIN_SCORE:
                return False
        return True
                
    def reset_scores( self ):

        # init scores
        for marker in self.markerList:
            self.scores[ marker.name ] = MIN_SCORE        

    def clean_phrase( self, phrase ):
        """
            TODO:Should clean words from apostrophes, dashes and periods ...etc
            Now it only returns same phrase (lower case)
        """
        return phrase.lower()

    def __str__( self ):
        st = ""
        for m in self.markerList:
            subst = m.name + ":" + str(self.scores[m.name])
            st += (subst + ",")

        #remove last comma
        return st[:-1]
        
    def score( self, hotel ):
        """
            score the hotel
        """
        # reset scores
        self.reset_scores()

        # keep track of seen phrases/words to avoid duplicate scoring
        seen_terms = {}
        
        # tokenize words using ntlk lib       
        word_list = word_tokenize(hotel.desc_en.decode('utf8'))       
      
        # iterate over length1_dict to find key 1-word lengths
        index = 0
        while index < len(word_list):
            word = self.clean_phrase(word_list[index])
            if word not in seen_terms:

                # update all scores
                for marker in self.markerList:
                    self.scores[marker.name] += marker.score_word(word)                
                
                seen_terms[word] = True
            index+=1

        # reset index
        index = 0
        
        # start loop for 2-word phrases 
        while index < (len(word_list)-1):
            phrase =  self.clean_phrase(word_list[index] + " " + word_list[index+1])
            if phrase not in seen_terms:                

                # update all scores
                for marker in self.markerList:
                    self.scores[marker.name] += marker.score_phrase(word)
                    
                seen_terms[phrase] = True
            index+=1
 
        return self.scores   

class WellnessInterestsMarker(BaseAbstractMarker):

    name = WELLNESS
    length1_dict = { 'spa' : 100, 'fitness' : 100, 'massage' : 100, 'bowling' : 80, 'tennis' : 100, 'gym' : 100, 'sauna':100, 'hammam':100 }
    length2_dict = { 'wellness centre' : 120, 'wellness center' : 120, 'wellness facilities' : 120,
                     'outdoor pool' : 110, 'relaxation area' : 60 }

class SkiingInterestsMarker(BaseAbstractMarker):

    name = SKIING
    length1_dict = { 'skiing' : 120, 'ski': 100 }
    length2_dict = { 'skiing trail' : 150, 'ski area': 150 }

class ShoppingInterestsMarker(BaseAbstractMarker):

    name = SHOPPING
    length1_dict = { 'shops' : 80, 'malls' : 80, 'shop' : 80, 'mall' : 80, 'shopping' : 90, 'restaurant': 80, 'restaurants' : 90, 'cafes' : 90, 'souvenir' : 90,
                     'souvenirs':90, 'souks':90, 'vineyards': 80 }
    length2_dict = { 'shopping center' : 120, 'shopping centre' : 120, 'shopping centers' : 120, 'city center': 100, 'city centre': 100, 'business centre': 75,
                     'shopping mall' : 120, 'shopping venues' : 120, 'shopping centres' : 120, 'dining options': 80, 'main square': 100, 'town centre': 100 }

class RomanceInterestsMarker(BaseAbstractMarker):

    name = ROMANCE
    length1_dict = { 'couples' : 90, 'romantic' : 140, 'romance' : 130, 'honeymooners' : 160, 'spa': 85, 'scenic': 90, 'sunset': 90, 'stunning': 80, 'lagoon': 80, 'views': 80, 'panoramic': 90,
                     'villa': 55 }
    length2_dict = { 'scenic park' : 60, 'sea views' : 60, 'sea view' : 60, 'ocean views': 60, 'stunning views': 60, 'sunset views': 60, 'spectacular views': 60, 'beautiful views': 60,
                     'panoramic views': 60, 'countryside walks': 60 }

class ClubbingInterestsMarker(BaseAbstractMarker):

    name = CLUBBING
    length1_dict = { 'nightlife' : 120, 'restaurants' : 90, 'bars' : 100, 'bar': 65, 'music': 80, 'shops': 65, 'karaoke': 70 }
    length2_dict = { 'live music' : 100, 'night life' : 120, 'dance club':120, 'dance clubs': 120, 'games room': 80 }

class HistoryAndCultureInterestsMarker(BaseAbstractMarker):

    name = HISTORY_CULTURE
    length1_dict = { 'museum' : 100, 'history' : 120, 'museums' : 145, 'culture': 120, 'historic': 100 }
    length2_dict = { 'arts culture' : 110, 'town centre': 90, 'historic centre': 100 }

class CasinoInterestsMarker(BaseAbstractMarker):

    name = CASINOS
    length1_dict = { 'casino' : 120 }

class BeachAndSunInterestsMarker(BaseAbstractMarker):

    name = BEACH_AND_SUN
    length1_dict = { 'beach' : 120, 'beaches' : 150, 'swimming' : 80 }
    length2_dict = { 'private beach': 60 }

class AdventureInterestsMarker(BaseAbstractMarker):

    name = ADVENTURE
    length1_dict = { 'adventure': 90, 'diving': 85, 'rafting': 85, 'canoeing' : 85, 'trekking':80,
                     'fishing' : 85, 'hiking' : 85, 'parachuting' : 85, 'rappel' : 85, 'caving' : 85,
                     'snorkeling' : 85, 'cycling' : 80, 'surfing':80, 'snorkelling' : 85,
                     'biking' : 85, 'skiing' : 85, 'windsurfing' : 85, 'boating' : 85 }
    length2_dict = { 'boat trips': 80, 'adventure sports' : 85 , 'whale watching' :30,
                     'horse riding' : 80, 'outdoor excursions' : 80, 'horseback riding':80,
                     'shark-cage diving' : 100, 'mountain biking' : 70, 'national park': 80 }

    def __init__(self, hotels):      
        super( AdventureInterestsMarker, self ).__init__(hotels)

class FamilyInterestsMarker(BaseAbstractMarker):

    name = FAMILY
    #
    # keyword score dict
    #

    length1_dict = { 'family-friendly': 100, 'playground': 65, 'garden': 45, 'gardens': 55, 'park' : 60,
                     'beach' : 30, 'pool': 55, 'bowling' : 60 }
    length2_dict = { 'family fun' : 85, 'family activities' : 85, 'relaxation area' : 50,
                     'family entertainment' : 85, 'kids club' : 85, 'family atmosphere': 85,
                     "kids' club" : 85, 'water activities' : 70, 'holiday home': 90,
                     'outdoor pool' : 30, 'swimming pool' : 30, 'scenic park': 50,
                     'whale watching' : 60}    

    def __init__(self, hotels):      
        super( FamilyInterestsMarker, self ).__init__(hotels)                  

    
            
        
        
