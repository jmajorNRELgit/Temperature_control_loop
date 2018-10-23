import pickle
    
class PID_tuning():
    
    def __init__(self, data, p, i,):
        
        self.data = data
        self.p = p
        self.i = i
        
        
###change the name of the pickle file here
#with open(r'C:\Users\jmajor\Desktop\github\Temperature_control_loop\graph_data.pkl', 'wb') as output:
#    for o in obj:
#        pickle.dump(o, output, pickle.HIGHEST_PROTOCOL)
#        
#        


        
obj = []
b = 0
with open(r'C:\Users\jmajor\Desktop\github\Temperature_control_loop\graph_data.pkl', 'rb') as i:
    while True:
            
        obj.append(None)
        try:
            obj[b] = pickle.load(i)
        except EOFError:
               break
        b += 1