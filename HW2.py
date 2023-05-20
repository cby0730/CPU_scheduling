import copy


change_to_letter = {0 : "0", 1 : "1", 2 : "2", 3 : "3", 4 : "4", 5 : "5", 6 : "6", 7 : "7", 8 : "8", 9 : "9"
                   ,10 : "A", 11 : "B", 12 : "C", 13 : "D", 14 : "E", 15 : "F", 16 : "G", 17 : "H", 18 : "I", 19 : "J", 20 : "K"
                   , 21 : "L", 22 : "M", 23 : "N", 24 : "O", 25 : "P", 26 : "Q", 27 : "R", 28 : "S", 29 : "T", 30 : "U", 31 : "V", 32 : "W"
                   , 33 : "X", 34 : "Y", 35 : "Z" }

class Schedule :

    def __init__(self) :
        self.data = []
        self.method = ""
        self.time_slice = 0
        self.fcfs_list = []
        self.rr_list = []
        self.srtf_list = []
        self.hrrn_list = []
        self.pprr_list = []
        self.output_file = 0
        self.output_name = ""

    def Read_file(self) :

        file_name = str( input( "Please input the file name : \n" ) ) 
        f = open( file_name + ".txt", "r" )

        self.output_name = "out_" + file_name + ".txt"
        self.output_file = open( self.output_name, "w" )

        self.method, self.time_slice = f.readline().split() # get the method and the time slice

        f.readline() # read second line that is no used

        for line in f : # store every process' info
            if line == "\n" : continue
            id, bt, at, pr = [int(x) for x in line.split()]
            self.data.append( { "id" : id, "bt" : bt, "at" : at, "pr" : pr, "ft" : 0, "tr" : 0, "wt" : 0 } )

        self.data = sorted( self.data, key = lambda d:d["id"] )

    def Which_one(self) :

        printer = Pretty_Printer()

        if self.method == "1" :
            self.output_file.write( "FCFS\n==        FCFS==" + "\n" )
            self.FCFS()
            self.output_file.close()
            printer.one_printer( self.output_name, "FCFS", self.fcfs_list )
        elif self.method == "2" :
            self.output_file.write( "RR\n==          RR==" + "\n" )
            self.RR()
            self.output_file.close()
            printer.one_printer( self.output_name, "RR", self.rr_list )
        elif self.method == "3" :
            self.output_file.write( "SRTF\n==        SRTF==" + "\n" )
            self.SRTF()
            self.output_file.close()
            printer.one_printer( self.output_name, "SRTF", self.srtf_list )
        elif self.method == "4" :
            self.output_file.write("Priority RR\n==        PPRR==" + "\n" )
            self.PPRR()
            self.output_file.close()
            printer.one_printer( self.output_name, "PPRR", self.pprr_list )
        elif self.method == "5" :
            self.output_file.write( "HRRN\n==        HRRN==" + "\n" )
            self.HRRN()
            self.output_file.close()
            printer.one_printer( self.output_name, "HRRN", self.hrrn_list )
        elif self.method == "6" :
            self.output_file.write( "All\n" )
            self.output_file.write( "==        FCFS==" + "\n" )
            self.FCFS()
            self.output_file.write( "==          RR==" + "\n" )
            self.RR()
            self.output_file.write( "==        SRTF==" + "\n" )
            self.SRTF()
            self.output_file.write( "==        PPRR==" + "\n" )
            self.PPRR()
            self.output_file.write( "==        HRRN==" + "\n" )
            self.HRRN()
            self.output_file.close()
            printer.all_printer( self.output_name, self.fcfs_list, self.rr_list, self.srtf_list, self.pprr_list, self.hrrn_list )
        else :
            self.output_file.write( "No such method\n" )

    def FCFS(self) :

        time = 0 
        self.fcfs_list = []

        new_data = copy.deepcopy( self.data )

        while new_data :

            cur = min( new_data, key = lambda x:x['at'] ) # pick the first min arrival time

            if time < cur["at"] :
                time = time + 1
                self.output_file.write( "-" )
            elif cur["bt"] == 0 :
                new_data.remove( cur )
                cur["bt"] = next( ( item for item in self.data if item["id"] == cur["id"] ), None )["bt"]
                cur["ft"] = time # finished time
                cur["tr"] = time - cur["at"] # turnaround time
                cur["wt"] = cur["tr"] - cur["bt"] # waiting time
                self.fcfs_list.append( cur )
            else :
                cur["bt"] = cur["bt"] - 1
                time = time + 1
                self.output_file.write( change_to_letter[ cur["id"] ] )

        self.output_file.write( "\n" )

    def RR(self) :

        time = 0
        slice = 0
        self.rr_list = []
        queue = []

        new_data = copy.deepcopy( self.data )

        first = min( new_data, key = lambda x:x['at'] )
        new_data.remove( first )
        queue.append( first ) # pick the first min arrival time

        while queue or new_data :

            if queue : # if queue is not empty, take the first one
                cur = queue[0]
            else : # if there is nothing in waiting queue, print dash
                time = time + 1
                self.output_file.write( "-" )

            if new_data : # if new_data is not empty, take min arrival time
                next_one = min( new_data, key = lambda x:x['at'] )

            while time == next_one["at"] and new_data : # put next_one into queue and get next again
                new_data.remove( next_one )
                queue.append( next_one )
                if new_data :
                    next_one = min( new_data, key = lambda x:x['at'] )

            if cur : # check if really get a cur from queue
                if time < cur["at"] : 
                    time = time + 1
                    self.output_file.write( "-" )
                elif cur["bt"] == 0 : # if this process is done
                    queue.pop( 0 )
                    cur["bt"] = next( ( item for item in self.data if item["id"] == cur["id"] ), None )["bt"]
                    cur["ft"] = time # finished time
                    cur["tr"] = time - cur["at"] # turnaround time
                    cur["wt"] = cur["tr"] - cur["bt"] # waiting time
                    self.rr_list.append( cur )
                    slice = 0 # reset the time slice
                elif slice == int(self.time_slice) : # when time is up
                    queue.pop( 0 )
                    queue.append( cur ) # add this process to the end
                    slice = 0 # reset the time slice
                else : 
                    cur["bt"] = cur["bt"] - 1
                    time = time + 1
                    slice = slice + 1
                    self.output_file.write( change_to_letter[ cur["id"] ] )

            cur = {}
        
        self.output_file.write( "\n" )

    def SRTF(self) :

        time = 0
        waiting = []
        self.srtf_list = []

        new_data = copy.deepcopy( self.data )
        first = min( new_data, key = lambda x:x['at'] )
        new_data.remove( first )
        waiting.append( first )
        cur = {}

        while new_data or waiting :

            if new_data :
                wait = min( new_data, key = lambda x:x['at'] )

            while time == wait["at"] and new_data:
                new_data.remove( wait )
                waiting.append( wait )
                waiting = sorted( waiting, key = lambda d:d["id"] ) # if burst time is equal, take the smallest pid
                if new_data :
                    wait = min( new_data, key = lambda x:x['at'] )

            if waiting :

                temp = self.pick_srtf( waiting )
                if cur and temp["id"] != cur["id"] and temp["bt"] == cur["bt"] : # avoid, for example 11444 become 11442
                    pass                                                         # {id:2, bt:4}, {id:4, bt:4} and pick id:2 first
                elif cur and temp["id"] == cur["id"] :
                    pass
                else :
                    cur = self.pick_srtf( waiting )

            else :
                time = time + 1
                self.output_file.write( "-" )

            if cur :
                if time < cur["at"] :
                    time = time + 1
                    self.output_file.write( "-" )
                elif cur["bt"] == 0 :
                    waiting.remove( cur )
                    cur["bt"] = next( ( item for item in self.data if item["id"] == cur["id"] ), None )["bt"]
                    cur["ft"] = time # finished time
                    cur["tr"] = time - cur["at"] # turnaround time
                    cur["wt"] = cur["tr"] - cur["bt"] # waiting time
                    self.srtf_list.append( cur )
                    cur = {}
                else :
                    cur["bt"] = cur["bt"] - 1
                    time = time + 1
                    self.output_file.write( change_to_letter[ cur["id"] ] )
        
        self.output_file.write( "\n" )

    def pick_srtf( self, waiting ) :

        temp = min( waiting, key = lambda b:b['bt'] )
        result = [ i for i in waiting if i['bt'] == temp["bt"] ]

        if len( result ) == 1 :
            return temp
        else :
            temp = min( result, key = lambda b:b['at'] )
            result = [ i for i in result if i['at'] == temp["at"] ]

            if len( result ) == 1 :
                return temp 
            else :
                return min( result, key = lambda b:b['id'] )

    def HRRN( self ) :

        time = 0 
        self.hrrn_list = []
        cur = {}

        new_data = copy.deepcopy( self.data )
        for i in new_data :
            i["real_bt"] = i["bt"]

        while new_data :

            if not cur :
                cur = self.pick_hrrn( new_data, time )

            if time < cur["at"] :
                time = time + 1
                self.output_file.write( "-" )
                cur = {}
            elif cur["bt"] == 0 :
                new_data.remove( cur )
                cur["bt"] = next( ( item for item in self.data if item["id"] == cur["id"] ), None )["bt"]
                cur["ft"] = time # finished time
                cur["tr"] = time - cur["at"] # turnaround time
                cur["wt"] = cur["tr"] - cur["bt"] # waiting time
                self.hrrn_list.append( cur )
                cur = {}
            else :
                cur["bt"] = cur["bt"] - 1
                time = time + 1
                self.output_file.write( change_to_letter[ cur["id"] ] )

        self.output_file.write( "\n" )

    def pick_hrrn( self, new_data, time ) :

        temp = max( new_data, key = lambda b:( time - b['at'] + b["real_bt"] ) / b["real_bt"] )
        result = [ i for i in new_data if ( time - i['at'] + i["real_bt"] ) / i["real_bt"] == ( time - temp['at'] + temp["real_bt"] ) / temp["real_bt"] ]

        if len( result ) == 1 :
            return temp
        else :
            temp = min( result, key = lambda b:b['at'] )
            result = [ i for i in result if i['at'] == temp["at"] ]

            if len( result ) == 1 :
                return temp 
            else :
                return min( result, key = lambda b:b["id"] )

    def PPRR( self ) :

        time = 0 
        slice = 0
        self.pprr_list = []
        queue = []
        cur = {}

        new_data = copy.deepcopy( self.data )

        while new_data or queue :

            if new_data :
                temp = min( new_data, key = lambda d:d["at"] )
            
            while temp["at"] == time and new_data :
                new_data.remove( temp ) 
                queue.append( temp )
                if new_data :
                    temp = min( new_data, key = lambda d:d["at"] )

            if queue : # if queue is not empty, take the first one
                queue = sorted( queue, key = lambda x:x["pr"] )
                if not cur :
                    cur = queue[0]
                elif cur != queue[0] :
                    queue.remove( cur )
                    queue.append( cur )
                    cur = queue[0]
                    slice = 0 
                else :
                    pass
            else : # if there is nothing in waiting queue, print dash
                time = time + 1
                self.output_file.write( "-" )

            if cur :
                if time < cur["at"] :
                    self.output_file.write( "-" )
                    time = time + 1 
                elif cur["bt"] == 0 :
                    queue.pop( 0 )
                    cur["bt"] = next( ( item for item in self.data if item["id"] == cur["id"] ), None )["bt"]
                    cur["ft"] = time # finished time
                    cur["tr"] = time - cur["at"] # turnaround time
                    cur["wt"] = cur["tr"] - cur["bt"] # waiting time
                    self.pprr_list.append( cur )
                    slice = 0 # reset the time slice
                    cur = {}
                elif slice == int(self.time_slice) : # when time is up
                    queue.pop( 0 )
                    queue.append( cur ) # add this process to the end
                    slice = 0 # reset the time slice
                    cur = {}
                else : 
                    cur["bt"] = cur["bt"] - 1
                    time = time + 1
                    slice = slice + 1
                    self.output_file.write( change_to_letter[ cur["id"] ] )

        self.output_file.write( "\n" )

class Pretty_Printer :

    def one_printer( self, file_name, process_name, process_list ) :
        process_list = sorted( process_list, key = lambda x:x["id"] )
        output = open( file_name, 'a' )
        output.write( "===========================================================\n\n" )

        output.write( "Waiting Time\n" ) 
        output.write( "ID\t" + str( process_name ) + "\n" )
        output.write( "===========================================================\n" )
        for i in process_list :
            output.write( str( i["id"] ) + "\t" + str( i["wt"] ) + "\n" )
        output.write( "===========================================================\n\n" )

        output.write( "Turnaround Time\n" ) 
        output.write( "ID\t" + str( process_name ) + "\n" )
        output.write( "===========================================================\n" )
        for i in process_list :
            output.write( str( i["id"] ) + "\t" + str( i["tr"] ) + "\n" )
        output.write( "===========================================================\n\n" )
        output.close()

    def all_printer( self, file_name, fcfs_list, rr_list, srtf_list, pprr_list, hrrn_list ) :
        fcfs_list = sorted( fcfs_list, key = lambda x:x["id"] )
        rr_list = sorted( rr_list, key = lambda x:x["id"] )
        srtf_list = sorted( srtf_list, key = lambda x:x["id"] )
        pprr_list = sorted( pprr_list, key = lambda x:x["id"] )
        hrrn_list = sorted( hrrn_list, key = lambda x:x["id"] )
        output = open( file_name, 'a' )
        output.write( "===========================================================\n\n" )

        output.write( "Waiting Time\n" ) 
        output.write( "ID	FCFS	RR	SRTF	PPRR	HRRN\n" )
        output.write( "===========================================================\n" )
        for i in range( len( fcfs_list ) ) :
            output.write( str( fcfs_list[i]["id"] ) + "\t" + str( fcfs_list[i]["wt"] ) + "\t" + str( rr_list[i]["wt"] ) + "\t" + str( srtf_list[i]["wt"] )
                    + "\t" + str( pprr_list[i]["wt"] ) + "\t" + str( hrrn_list[i]["wt"] ) + "\n" )
        output.write( "===========================================================\n\n" )

        output.write( "Turnaround Time\n" ) 
        output.write( "ID	FCFS	RR	SRTF	PPRR	HRRN\n" )
        output.write( "===========================================================\n" )
        for i in range( len( fcfs_list ) ) :
            output.write( str( fcfs_list[i]["id"] ) + "\t" + str( fcfs_list[i]["tr"] ) + "\t" + str( rr_list[i]["tr"] ) + "\t" + str( srtf_list[i]["tr"] )
                    + "\t" + str( pprr_list[i]["tr"] ) + "\t" + str( hrrn_list[i]["tr"] ) + "\n" )
        output.write( "===========================================================\n\n" )
        output.close()

test = Schedule()
test.Read_file()
test.Which_one()




    
