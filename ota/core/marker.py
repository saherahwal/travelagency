from utils import *
from nltk import word_tokenize 

MIN_SCORE = 10
MAX_SCORE = 300

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
        word_list = word_tokenize(hotel.desc_en)       
      
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
    length1_dict = { 'spa' : MAX_SCORE, 'fitness' : MAX_SCORE, 'massage' : 0.9 * MAX_SCORE, 'bowling' : 0.8 * MAX_SCORE,
                     'tennis' : 0.9 * MAX_SCORE, 'gym' : MAX_SCORE, 'sauna':0.9 * MAX_SCORE, 'hammam':0.9 * MAX_SCORE }
    length2_dict = { 'wellness centre' : MAX_SCORE, 'wellness center' : MAX_SCORE, 'wellness facilities' : MAX_SCORE,
                     'outdoor pool' : MAX_SCORE, 'relaxation area' : 0.6 * MAX_SCORE }

class SkiingInterestsMarker(BaseAbstractMarker):

    name = SKIING
    length1_dict = { 'skiing' : MAX_SCORE, 'ski': MAX_SCORE, 'ski-run': MAX_SCORE }
    length2_dict = { 'skiing trail' : MAX_SCORE, 'ski area': MAX_SCORE, 'ski trails': MAX_SCORE }

class ShoppingInterestsMarker(BaseAbstractMarker):

    name = SHOPPING
    length1_dict = { 'shops' : MAX_SCORE, 'malls' : MAX_SCORE, 'shop' : 0.7 * MAX_SCORE, 'mall' : MAX_SCORE, 'shopping' : MAX_SCORE, 'restaurant': 0.8 * MAX_SCORE,
                     'restaurants' : 0.9 * MAX_SCORE, 'cafes' : 0.85 * MAX_SCORE, 'souvenir' : 0.9 * MAX_SCORE,
                     'souvenirs':0.9 * MAX_SCORE, 'souks':MAX_SCORE, 'vineyards': 0.8 * MAX_SCORE }
    length2_dict = { 'shopping center' : 0.9 * MAX_SCORE, 'shopping centre' : 0.9 * MAX_SCORE, 'shopping centers' : MAX_SCORE,
                     'city center': 0.85 * MAX_SCORE, 'city centre': 0.85 * MAX_SCORE, 'business centre': 0.75 * MAX_SCORE,
                     'shopping mall' : MAX_SCORE, 'shopping venues' : MAX_SCORE, 'shopping centres' : MAX_SCORE,
                     'dining options': 0.8 * MAX_SCORE, 'main square': 0.95 * MAX_SCORE, 'town centre': MAX_SCORE }

class RomanceInterestsMarker(BaseAbstractMarker):

    name = ROMANCE
    length1_dict = { 'couples' : 0.8 * MAX_SCORE, 'romantic' : MAX_SCORE, 'romance' : 0.95 * MAX_SCORE, 'honeymooners' : MAX_SCORE,
                     'spa': 0.7 * MAX_SCORE, 'scenic': 0.8 * MAX_SCORE, 'sunset': 0.9 * MAX_SCORE, 'stunning': 0.9 * MAX_SCORE, 'intimate' : 0.8 * MAX_SCORE,
                     'lagoon': 0.85 * MAX_SCORE, 'views': 0.9 * MAX_SCORE, 'panoramic': 0.9 * MAX_SCORE, 'villa': 0.5 * MAX_SCORE }
    length2_dict = { 'scenic park' : 0.8 * MAX_SCORE, 'sea views' : 0.8 * MAX_SCORE, 'sea view' : 0.7 * MAX_SCORE, 'ocean views': 0.8 * MAX_SCORE,
                     'stunning views': 0.9 * MAX_SCORE, 'sunset views': 0.95 * MAX_SCORE, 'spectacular views': 0.95 * MAX_SCORE, 'beautiful views': 0.9 * MAX_SCORE,
                     'panoramic views': 0.9 * MAX_SCORE, 'countryside walks': 0.7 * MAX_SCORE }

class ClubbingInterestsMarker(BaseAbstractMarker):

    name = CLUBBING
    length1_dict = { 'nightlife' : MAX_SCORE, 'restaurants' : 0.9 * MAX_SCORE, 'bars' : 0.95 * MAX_SCORE, 'bar': 0.6 * MAX_SCORE,
                     'music': 0.8 * MAX_SCORE, 'shops': 0.65 * MAX_SCORE, 'karaoke': 0.7 * MAX_SCORE, 'clubbing': MAX_SCORE }
    length2_dict = { 'live music' : 0.9 * MAX_SCORE, 'night life' : MAX_SCORE, 'dance club':MAX_SCORE, 'dance clubs': MAX_SCORE, 'games room': 0.85 * MAX_SCORE,
                     'night entertainment': MAX_SCORE }

class HistoryAndCultureInterestsMarker(BaseAbstractMarker):

    name = HISTORY_CULTURE
    length1_dict = { 'museum' : 0.8 * MAX_SCORE, 'history' : 0.95 * MAX_SCORE, 'museums' : MAX_SCORE, 'culture': 0.95 * MAX_SCORE,
                     'historic': 0.90 * MAX_SCORE, 'traditional': 0.85 * MAX_SCORE }
    length2_dict = { 'arts culture' : 0.9 * MAX_SCORE, 'town centre': 0.75 * MAX_SCORE, 'historic centre': 0.9 * MAX_SCORE }

class CasinoInterestsMarker(BaseAbstractMarker):

    name = CASINOS
    length1_dict = { 'casino' : MAX_SCORE, 'casinos': MAX_SCORE, 'gambling': MAX_SCORE }
    length2_dict = { 'gambling thrills': MAX_SCORE, 'gambling venue': MAX_SCORE, 'gambling house': MAX_SCORE, 'gambling area': MAX_SCORE }

class BeachAndSunInterestsMarker(BaseAbstractMarker):

    name = BEACH_AND_SUN
    length1_dict = { 'beach' : 0.95 * MAX_SCORE, 'beaches' : MAX_SCORE, 'swimming' : 0.85 * MAX_SCORE }
    length2_dict = { 'private beach': 0.75 * MAX_SCORE }

class AdventureInterestsMarker(BaseAbstractMarker):

    name = ADVENTURE
    length1_dict = { 'adventure': 0.85 * MAX_SCORE, 'diving': 0.9 * MAX_SCORE, 'rafting': 0.9 * MAX_SCORE, 'canoeing' : 0.9 * MAX_SCORE, 'trekking':0.9 * MAX_SCORE,
                     'fishing' : 0.9 * MAX_SCORE, 'hiking' : 0.9 * MAX_SCORE, 'parachuting' : MAX_SCORE, 'rappel' : MAX_SCORE, 'caving' : MAX_SCORE, 'kayaking':0.9 * MAX_SCORE,
                     'snorkeling' : 0.9 * MAX_SCORE, 'cycling' : 0.85 * MAX_SCORE, 'surfing':0.85 * MAX_SCORE, 'snorkelling' : 0.85 * MAX_SCORE, 'canyoning': 0.95 * MAX_SCORE,
                     'biking' : 0.85 * MAX_SCORE, 'skiing' : 0.9 * MAX_SCORE, 'windsurfing' : 0.9 * MAX_SCORE, 'boating' : 0.85 * MAX_SCORE, 'rappelling' : MAX_SCORE }
    length2_dict = { 'boat trips': 0.7 * MAX_SCORE, 'adventure sports' : 0.75 * MAX_SCORE , 'whale watching' :0.4 * MAX_SCORE, 'rock climbing': 0.9 * MAX_SCORE,
                     'horse riding' : 0.75 * MAX_SCORE, 'outdoor excursions' : 0.8 * MAX_SCORE, 'horseback riding': 0.8 * MAX_SCORE, 'whitewater rafting': 0.9 * MAX_SCORE,
                     'shark-cage diving' : MAX_SCORE, 'mountain biking' : 0.9 * MAX_SCORE, 'national park': 0.75 * MAX_SCORE }

    def __init__(self, hotels):      
        super( AdventureInterestsMarker, self ).__init__(hotels)

class FamilyInterestsMarker(BaseAbstractMarker):

    name = FAMILY
    #
    # keyword score dict
    #

    length1_dict = { 'family-friendly': MAX_SCORE, 'playground': 0.7 * MAX_SCORE, 'garden': 0.5 * MAX_SCORE, 'gardens': 0.55 * MAX_SCORE, 'park' : 0.6 * MAX_SCORE,
                     'beach' : 0.5 * MAX_SCORE, 'pool': 0.6 * MAX_SCORE, 'bowling' : 0.7 * MAX_SCORE }
    length2_dict = { 'family fun' : MAX_SCORE, 'family activities' : 0.85 * MAX_SCORE, 'relaxation area' : 0.4 * MAX_SCORE,
                     'family entertainment' : MAX_SCORE, 'kids club' : 0.9 * MAX_SCORE, 'family atmosphere': 0.95 * MAX_SCORE,
                     "kids' club" : 0.9 * MAX_SCORE, 'water activities' : 0.9 * MAX_SCORE, 'holiday home': 0.9 * MAX_SCORE,
                     'outdoor pool' : 0.4 * MAX_SCORE, 'swimming pool' : 0.7 * MAX_SCORE, 'scenic park': 0.5 * MAX_SCORE,
                     'whale watching' : 0.8 * MAX_SCORE}    

    def __init__(self, hotels):      
        super( FamilyInterestsMarker, self ).__init__(hotels)                  

