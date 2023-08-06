import sys
import inspect
import parser
import logging
import ast
import copy
import csv


#logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)

class NotebookRecorder():
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if NotebookRecorder.__instance == None:
            NotebookRecorder()
        return NotebookRecorder.__instance

    def __init__(self):
        self.recorder = NotebookProvenance()    

        """ Virtually private constructor. """
        if NotebookRecorder.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            NotebookRecorder.__instance = self           

class NotebookProvenance():    
    def __init__(self,log_file="default.log",rewrite=False,record_in_memory=False):
        self.source = {}
        self.vars = {}
        self.var_id = set()
        self.dependency = []
        self.trace = []
        self.previous_frame = {}
                
        self.temp_pon = []
        self.data_graph = []
        #self.log_file = log_file
        
        self.set_log_file(log_file,rewrite)

        self.counter = 0

        self.code_pos = {}
        self.line_stack = {}

        self.record_in_memory = record_in_memory
    
    def set_log_file(self,log_file,rewrite):
        self.log_file = log_file
        self.rewrite = rewrite
        self.prepare_file()

    def prepare_file(self):
        if self.rewrite:
            self.file = open(self.log_file,"w")
        else:
            self.file = open(self.log_file,"a")
        self.csv_writer = csv.writer(self.file)

        
    def parse_vars(self,source):
        result = {"t":[],"v":[]}
        root = ast.parse(source.strip())

        #is_body = False
        for node in ast.walk(root):        
            if isinstance(node, ast.Name):
                if isinstance(node.ctx, ast.Store):
                    result["t"].append(node.id)
                else:
                    result["v"].append(node.id)
            elif isinstance(node, ast.Attribute):
                #yield node.attr
                result["v"].append(node.attr)
            elif isinstance(node, ast.FunctionDef):
                #yield node.name        
                result["v"].append(node.name)
        return result
                
    def get_annotation_var(self,filename):
        try:
            self.vars[filename]
        except:
            self.vars[filename] = {}
            
        for i,x in enumerate(self.source[filename][0]):
            #print(x)
            if x.strip().startswith("#@begin "):
                #print(x)
                yy = x.strip().split(" ")
                try:
                    self.vars[filename][yy[1]]
                except:
                    self.vars[filename][yy[1]] = {}
                    self.vars[filename][yy[1]]["val"] = []
                    self.vars[filename][yy[1]]["start"] = None
                    self.vars[filename][yy[1]]["end"] = None
                self.vars[filename][yy[1]]["val"] = yy[2:]
                self.vars[filename][yy[1]]["start"] = i
            if x.strip().startswith("#@end "):
                yy = x.strip().split(" ")
                try:
                    self.vars[filename][yy[1]]["end"] = i
                except:
                    pass                                

    def record_vars(self,frame):
        var_name = frame.f_locals.keys()
        for x in var_name:
            self.var_id.add((id(frame.f_locals[x]),x))
            
    def add_source(self,filename,frame):
        try:
            self.source[filename]
        except:
            self.source[filename] = inspect.getsourcelines(frame)
            #self.trace[filename] = []
            self.get_annotation_var(filename)
            
    def trace_vars(self,frame):
        if self.previous_frame!=None:
            previous_frame = self.previous_frame
            local_var = previous_frame.f_locals
            previous_line_no = previous_frame.f_lineno
            co = previous_frame.f_code
            func_name = co.co_name
            previous_filename = co.co_filename
            #varname = self.vars[previous_filename]

            local_var = frame.f_locals
            line_no = frame.f_lineno
            co = frame.f_code
            func_name = co.co_name
            filename = co.co_filename
            varname = self.vars[filename]
            for y in varname:
                if (previous_line_no-1)>=self.vars[filename][y]["start"] and (previous_line_no-1)<=self.vars[filename][y]["end"]:                
                    for yy in varname[y]["val"]:                    
                        if self.source[previous_filename][0][previous_line_no-1].find(yy) >= 0:
                            try:
                                print(y,yy)
                                #print(inspect.stack()[:4])

                                floc = local_var[yy].copy()
                                #print(floc)
                                #self.trace[filename].append((filename,func_name,line_no,self.source[filename][0][line_no-1],yy,floc))
                                #self.trace.append((filename,func_name,line_no,self.source[filename][0][line_no-1],yy,floc))
                                self.trace.append((filename,y,func_name,line_no,self.source[previous_filename][0][previous_line_no-1],yy,id(yy),floc))
                            except BaseException as ex:
                                #raise ex
                                pass    
        self.previous_frame = frame
        
    
    def trace_calls(self,frame, event, arg):
        co = frame.f_code
        func_name = co.co_names
        
        if func_name == 'write':
            # Ignore write() calls from print statements
            return

        if event == 'return':
            #print("return",arg)
            pass
        
        if func_name == "CaptureProvenance":
            return
        
        line_no = frame.f_lineno
        filename = co.co_filename

        logging.debug(("call:",event,func_name,arg,line_no,filename))                
        
        # only give attention for function / operations that is called from the python notebook
        if filename.startswith("<ipython-input"):
            return self.trace_lines
        
        return        
    
    def trace_lines(self,frame,event,arg):
        #co = frame.f_code
        #func_name = co.co_names        
        #if (event != 'line') or ("DataFrame" not in func_name):
        #    return
        #print("line",co,co.co_name,func_name,event,arg)    
        co = frame.f_code
        func_name = co.co_name
        line_no = frame.f_lineno
        filename = co.co_filename    
        if filename.startswith("<ipython-input"):
            #logging.debug(("line:",event,func_name,arg,line_no,frame.f_locals.keys()))
            #print(filename,frame.f_locals.keys(),func_name,event,arg,line_no)
            defined_names = set(frame.f_locals.keys())

            self.add_source(filename,frame)

            if event == "line" and func_name!="<module>":
                try:
                    line_code = self.source[frame.f_code.co_filename][0][frame.f_lineno-1]
                except:
                    return
                #line_code = " ".join(self.source[frame.f_code.co_filename][0][frame.f_code.co_firstlineno-1:frame.f_lineno])

                parsable = False
                trace_line = frame.f_lineno

                try:
                    self.code_pos[func_name]
                except:
                    self.code_pos[func_name] = (0,1)
                
                if trace_line >= self.code_pos[func_name][0] and trace_line <= self.code_pos[func_name][1]:
                    return
                
                #if trace_line<self.temp_trace_line:
                #    return

                pvars = {"t":[],"v":[]}

                while not parsable and trace_line<len(self.source[frame.f_code.co_filename][0]):
                    try:
                        pvars = self.parse_vars(line_code.strip())
                        parsable = True
                    except:
                        trace_line+=1
                        line_code = " ".join(self.source[frame.f_code.co_filename][0][frame.f_lineno-1:trace_line])
                        #self.temp_continue = True
                

                self.code_pos[func_name] = (frame.f_lineno-1,trace_line)
                        
                self.temp_trace_line = trace_line

                logging.debug(("pvars_line:",pvars,line_code,frame.f_locals))

                
                try:
                    lstack = copy.deepcopy(self.line_stack[func_name])
                    self.line_stack[func_name] = [pvars,None]                    
                except:
                    lstack = None
                    self.line_stack[func_name] = [pvars,None]
                
                
                new_identifier_val = []
                if lstack!=None:
                    found = []
                    not_found = []
                    #for x in st_com.co_names:
                    for x in lstack[0]["t"]:
                    #for x in pvars["t"]:
                        try:
                            found.append((id(frame.f_locals[x]),x))            
                        except:
                            not_found.append(x)

                    for x in found:
                        try:
                            new_identifier_val.append((x,copy.deepcopy(frame.f_locals[x[1]])))
                        except:
                            continue
                            
                logging.debug(("new_identifier:",new_identifier_val))
                
                """
                try:
                    frame_back = self.previous_frame[func_name]
                except:
                    frame_back = frame.f_locals.copy()
                """
                frame_back = frame.f_locals.copy()
                                    
                    
                """
                if self.previous_frame != None:
                    frame_back = self.previous_frame
                else:
                    frame_back = frame.f_locals.copy()
                """

                #logging.debug((frame_back,frame))

                found = []
                for x in pvars["v"]:
                    try:
                        found.append(((id(frame_back[x]),x),copy.deepcopy(frame_back[x])))
                    except:
                        not_found.append(x)
                
                self.line_stack[func_name][1] = (found,line_code,filename,line_no,func_name)

                #print("new_identifier:",set.difference(set(found),self.var_id))

                #print("used_identifier:",set.intersection(set(found),self.var_id))
                #self.data_graph.append((new_identifier_val,[(x,frame.f_locals[x]) for x in used_identifier],line_code,filename,line_no))
                if len(new_identifier_val)==0:
                    new_identifier_val = found

                if lstack!=None:
                    ffound = lstack[1][0]
                    #ffound = found
                    #self.data_graph.append((new_identifier_val,ffound.copy(),line_code,filename,line_no,func_name))
                    if self.record_in_memory:
                        self.data_graph.append((new_identifier_val,ffound.copy(),lstack[1][1],lstack[1][2],lstack[1][3],lstack[1][4])) 

                    #logging.debug((new_identifier_val,ffound.copy(),lstack[1][1],lstack[1][2],lstack[1][3],lstack[1][4]))

                    for x in new_identifier_val:
                        for y in ffound:
                            temp_write = [x[0][0],x[0][1],str(x[1]),y[0][0],y[0][1],str(y[1]),lstack[1][1],lstack[1][2],lstack[1][3],lstack[1][4]]
                            #temp_write = [x[0][0],x[0][1],str(x[1]),y[0][0],y[0][1],str(y[1]),line_code,filename,line_no,func_name]
                            self.csv_writer.writerow(temp_write)
                    #self.data_graph.append((new_identifier_val,self.temp_pon.copy(),line_code,filename,line_no))
                    
                """
                #if lstack!=None:
                #ffound = lstack[1][0]
                ffound = found
                self.data_graph.append((new_identifier_val,ffound.copy(),line_code,filename,line_no,func_name)) 
                #self.data_graph.append((new_identifier_val,ffound.copy(),lstack[1][1],lstack[1][2],lstack[1][3],lstack[1][4])) 

                #logging.debug((new_identifier_val,ffound.copy(),lstack[1][1],lstack[1][2],lstack[1][3],lstack[1][4]))

                for x in new_identifier_val:
                    for y in ffound:
                        #temp_write = [x[0][0],x[0][1],str(x[1]),y[0][0],y[0][1],str(y[1]),lstack[1][1],lstack[1][2],lstack[1][3],lstack[1][4]]
                        temp_write = [x[0][0],x[0][1],str(x[1]),y[0][0],y[0][1],str(y[1]),line_code,filename,line_no,func_name]
                        self.csv_writer.writerow(temp_write)
                #self.data_graph.append((new_identifier_val,self.temp_pon.copy(),line_code,filename,line_no))
                """

                #print(self.temp_pon)
                #print("new_var:",set.intersection(set(self.temp_pon),defined_names))
                #self.temp_pon.clear()
                #self.previous_frame = frame.f_locals.copy()
                self.previous_frame[func_name] = frame.f_locals.copy()
                
            elif event == "return" and func_name=="<module>":
                try:
                    line_code = " ".join(self.source[frame.f_code.co_filename][0][frame.f_code.co_firstlineno-1:frame.f_lineno])
                except:
                    return
                try:
                    pvars = self.parse_vars(line_code.strip())
                except:
                    pvars = {"t":[],"v":[]}


                found = []
                not_found = []
                #for x in st_com.co_names:
                for x in pvars["t"]:
                    try:
                        found.append((id(frame.f_locals[x]),x))            
                    except:
                        not_found.append(x)

                new_identifier = set.difference(set(found),self.var_id)
                new_identifier_val = []
                for x in new_identifier:
                    try:
                        new_identifier_val.append((x,copy.deepcopy(frame.f_locals[x[1]])))
                    except:
                        continue

                """
                if self.previous_frame != None:
                    frame_back = self.previous_frame
                else:
                    frame_back = frame.f_locals.copy()
                """
                    
                try:
                    frame_back = self.previous_frame[func_name]
                except:
                    frame_back = frame.f_locals.copy()                    

                #logging.debug((frame_back,frame))

                found = []
                for x in pvars["v"]:
                    try:
                        found.append(((id(frame_back[x]),x),copy.deepcopy(frame_back[x])))
                    except:
                        not_found.append(x)                    

                if len(new_identifier_val)==0:
                    new_identifier_val = found                                

                if self.record_in_memory:
                    self.data_graph.append((new_identifier_val,found.copy(),line_code,filename,line_no,func_name))                    
                
                for x in new_identifier_val:
                    for y in found:
                        temp_write = [x[0][0],x[0][1],str(x[1]),y[0][0],y[0][1],str(y[1]),line_code,filename,line_no,func_name]
                        self.csv_writer.writerow(temp_write)
                #self.temp_pon.clear()
                self.previous_frame[func_name] = frame.f_locals.copy()
                

            self.record_vars(frame)    
    
    def start_trace(self):
        sys.settrace(self.trace_calls)
        
    def stop_trace(self):
        sys.settrace(None)
        self.file.close()


from IPython.core.magic import (register_line_magic, register_cell_magic,
                                register_line_cell_magic)


@register_line_magic
def capture_provenance_start(line):    
    args = line.split(" ")
    NotebookRecorder.getInstance().recorder.set_log_file(args[0],eval(args[1]))
    NotebookRecorder.getInstance().recorder.start_trace()


@register_line_magic
def capture_provenance_stop(line):    
    NotebookRecorder.getInstance().recorder.stop_trace()
