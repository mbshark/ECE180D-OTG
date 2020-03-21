# Describes how to write a real-time server in Python / for C look at my Github @pholur
# This describes a NAIVE system design: please modify to improve robustness and client adds

def declareServer(profiles):
    # enter your codes here
    return None

def perfect_grid(mapping):
    # enter some code here to decide if rectangle
    return False

def optimize(mapping):
    if perfect_grid(mapping):
        return some_order # with PRIORITY?
  
    else:
        return another_order

def execute_to_client(order):
  # PREFERABLY MULTI-THREADED
  # ON/OFF preferably on what is in order
  # client would read output and turn LED ON/OFF
    [send_response_to_client(ord) for ord in order]
    return True
  
  
def runServer(debug = False):
    declareServer(profiles)
    
    # build a buffer to capture all inputs from clients
    # Assume we have i random clients CONN with n total clients
    buffer = []
    mapping = {}
    tik_tok = 1000
    tic = 0
    wait = 0
    
    # setting up a real-time system. NOTE: You can and potentially should use
    # multi-threading to decrease latency and improve performance
    while True:
        if wait == 0:
            tic += 1
        # enter the filestream data as you get it. NOTE: You may not get it
        try:
            fer.append(filestream.entry())
      
        # assume that the ENTRY: <IP, x, y, state>
        # if the buffer has clients that want to connect to it
        if not buffer:
            for elem in buffer:
                if elem[3] == 0:
                    ping[elem[0]] = elem[[1,2]]
                    cute_to_client([elem[0], "CONFIRM"])
          
        # reset the buffer to capture new strings
            buffer = []
      
        # only if I have some clients, optimize and send response
        if mapping and tic > tik_tok:
            wait = 1
            er = optimize(mapping)
            execute_to_client(order)
        
if __name__ == "__main__":
    runServer(debug = True)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    