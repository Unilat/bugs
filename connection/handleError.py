def handleError():  
    import sys
    stop = 1 
    line = []
    line.append(sys.exc_info()[2].tb_lineno)
    tb = sys.exc_info()[2].tb_next
    while stop:
        if tb == None:
            stop = 0
        else:
            line.append(tb.tb_lineno)
            tb = tb.tb_next
    print "\t", sys.exc_info()[0], sys.exc_info()[1],
    print "\n\t line no: ", line[-1], "\n\t traceback: ", line

