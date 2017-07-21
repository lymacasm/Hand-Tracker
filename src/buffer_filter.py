class BufferFilter(object):
    def __init__(self,maxsize):
        self.__list = []
        self.maxsize = maxsize


    def mean(self):
    	if len(self.__list) == 0:
    		return 0
        return sum(self.__list) / len(self.__list)  


    def median(self):
    	if len(self.__list) == 0:
    		return 0
        self.__listsort = sorted(self.__list)
        
        if len(self.__listsort) % 2 == 0: 
            return (self.__listsort[(len(self.__listsort) // 2)] + self.__listsort[(len(self.__listsort) // 2) - 1]) / 2   
        else: 
            return self.__listsort[(len(self.__listsort) - 1) // 2]
           

    def no_filter(self):
    	if len(self.__list) == 0:
    		return 0
        return self.__list[len(self.__list) - 1]

    
    def add_data(self,data):
        if len(self.__list) == 0:
            self.__list = [data]
        elif len(self.__list) >= 1 and len(self.__list) < self.maxsize:
            self.__list.append(data)
        elif len(self.__list) == self.maxsize:
            self.__list.pop(0)
            self.__list.append(data)
            
    def clear_buffer(self):
    	del self.__list[:]

        

        
        

        
