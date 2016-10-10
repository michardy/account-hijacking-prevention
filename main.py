import logging

log = logging.logger

def fingerprint(request):
    

class receiver()
    def __init__(self):
        self.__fxnList = {}
        self.__maxscores = {}
        self.__scores = {}
        self.__username = ''
        
    def add(self, name, fxn, score):
        self.__fxnList[name] = fxn
        self.__maxscores[name] = score
        self.__scores[name] = -1
        
    def run(self, request)
        name = request.get_argument('name')
        try:
            self.__scores[name] = self.__fxnList[name](request, self.__username)
            return (0)
        except IndexError:
            log.debug('Client input error: Could not find handler with name of ' +name + '.  ')
            return(1)

    def gTrust(self):
        total = 0
        actmax = 0
        for i in fxnList.keyes():
            if self.__scores[i] > -1:
                actmax += self.__maxscores[i]
                total += self.__scores[i]
        return(total/actmax)
