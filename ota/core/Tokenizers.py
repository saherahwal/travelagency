from utils import LandmarkObj, CityObj, HotelObj, AirportObj, RegionObj, HotelScoreObj

class DbConnection(object):
    """
    This encapsulates necessary fields for database connection
    """    
    def __init__(self, host, port, user, pwd, dbname):
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd
        self.dbname = dbname

class Tokenizer(object):
    """
        Responsible for reading files and tokenize lines based on delimiter
    """
    
    def __init__(self, delimiter, skip_first_line):        
        self.delimiter = delimiter
        self.skip_first_line = skip_first_line

    def gen_lines( self, filename ):
        lineNum = 0
        with open( filename, 'r') as f:
            for line in f:
                if (lineNum == 0 and self.skip_first_line):
                    lineNum+=1
                    continue
                lineNum+=1
                yield line

    def tokenize( self, line ):
        sp = line.split( self.delimiter )
        return sp        

class LandmarkTokenizer(Tokenizer):

    def __init__(self, delimiter, files, skip_first_line):
        super( LandmarkTokenizer, self ).__init__(delimiter, skip_first_line)
        self.files = files        

    def gen_landmark_objs( self ):
        for _file in self.files:
            for line in self.gen_lines(_file):
                # tokenize the line
                tk_line = self.tokenize( line )

                # construct landmark obj and yield
                landmarkObj = LandmarkObj( tk_line[0], tk_line[1], tk_line[2], tk_line[3], tk_line[4] )
                yield landmarkObj
     
class CityTokenizer(Tokenizer):

    def __init__(self, delimiter, files, skip_first_line):
        super( CityTokenizer, self).__init__(delimiter, skip_first_line)
        self.files = files

    def gen_city_objs( self ):
        for _file in self.files:
            for line in self.gen_lines(_file):
                # tokenize the line
                tk_line = self.tokenize( line )

                # construct city obj and yield
                cityObj = CityObj( tk_line[0], tk_line[1], tk_line[2], tk_line[3], tk_line[4])
                yield cityObj

class AirportTokenizer(Tokenizer):

    def __init__(self, delimiter, files, skip_first_line):
        super( AirportTokenizer, self).__init__(delimiter, skip_first_line)
        self.files = files

    def gen_airport_objs(self):
        for _file in self.files:
            for line in self.gen_lines(_file):
                # tokenize the line
                tk_line = self.tokenize( line )

                # construct city obj and yield
                airportObj = AirportObj( tk_line[0], tk_line[1], tk_line[2], tk_line[3], tk_line[4])
                yield airportObj


class HotelScoresTokenizer(Tokenizer):

    def __init__(self, delimiter, files, skip_first_line):
        super( HotelScoresTokenizer, self).__init__(delimiter, skip_first_line)
        self.files = files    

    def gen_hotelscores_objs(self):
        for _file in self.files:
            print "processing file", _file
            for line in self.gen_lines(_file):
                
                # tokenize the line
                tk_line = self.tokenize( line )

                hotel_booking_id = tk_line[0]
                scores_line = tk_line[1:]
                scores_dict = {}
                
                for _score in scores_line:
                    spColon = _score.split(":")
                    scores_dict[spColon[0]] = spColon[1]

                # construct hotel score obj and yield
                hotelScoreObj = HotelScoreObj( tk_line[0], scores_dict )

                yield hotelScoreObj                

class HotelTokenizer(Tokenizer):

    def __init__(self, delimiter, files, skip_first_line):
        super( HotelTokenizer, self).__init__(delimiter, skip_first_line)
        self.files = files

    def gen_hotel_objs(self):
        for _file in self.files:
            print "processing file", _file
            for line in self.gen_lines(_file):
                # tokenize the line
                tk_line = self.tokenize( line )

                # skip malformed line
                if (len(tk_line) != 39):                    
                    continue
                
                # construct city obj and yield
                hotelObj = HotelObj( tk_line[0], tk_line[1], tk_line[2], tk_line[3], tk_line[4], 
                                     tk_line[5], tk_line[6], tk_line[7], tk_line[8], tk_line[9], 
                                     tk_line[10], tk_line[11], tk_line[12], tk_line[13], tk_line[14],
                                     tk_line[15], tk_line[16], tk_line[17], tk_line[18], tk_line[19],
                                     tk_line[20], tk_line[21], tk_line[22], tk_line[23], tk_line[24],
                                     tk_line[25], tk_line[26], tk_line[27], tk_line[28], tk_line[29],
                                     tk_line[30], tk_line[31], tk_line[32], tk_line[33], tk_line[34],
                                     tk_line[35], tk_line[36], tk_line[37])                
                yield hotelObj                                          
               
class RegionTokenizer(Tokenizer):

    def __init__(self, delimiter, files, skip_first_line):
        super( RegionTokenizer, self).__init__(delimiter, skip_first_line)
        self.files = files

    def gen_region_objs( self ):
        for _file in self.files:
            for line in self.gen_lines(_file):
                # tokenize the line
                tk_line = self.tokenize( line )

                # construct city obj and yield
                regionObj = RegionObj( tk_line[0], tk_line[1], tk_line[2], tk_line[3], tk_line[4], tk_line[5])
                yield regionObj


