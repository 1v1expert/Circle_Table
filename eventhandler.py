class PrinterEventHandler:
    '''
    Defines a skeletton of an event-handler for printer events. It
    allows attaching to the printcore and will be triggered for
    different events.
    '''
    
    def __init__(self):
        '''
        Constructor.
        '''
        pass
    
    def on_init(self):
        '''
        Called whenever a new printcore is initialized.
        '''
        pass
    
    def on_send(self, command, gline):
        '''
        Called on every command sent to the printer.

        @param command: The command to be sent.
        @param gline: The parsed high-level command.
        '''
        pass
    
    def on_recv(self, line):
        '''
        Called on every line read from the printer.

        @param line: The data has been read from printer.
        '''
        pass
    
    def on_connect(self):
        '''
        Called whenever printcore is connected.
        '''
        pass
    
    def on_disconnect(self):
        '''
        Called whenever printcore is disconnected.
        '''
        pass
    
    def on_error(self, error):
        '''
        Called whenever an error occurs.

        @param error: The error that has been triggered.
        '''
        pass
    
    def on_online(self):
        '''
        Called when printer got online.
        '''
        pass
    
    def on_temp(self, line):
        '''
        Called for temp, status, whatever.

        @param line: Line of data.
        '''
        pass
    
    def on_start(self, resume):
        '''
        Called when printing is started.

        @param resume: If true, the print is resumed.
        '''
        pass
    
    def on_end(self):
        '''
        Called when printing ends.
        '''
        pass
    
    def on_layerchange(self, layer):
        '''
        Called on layer changed.

        @param layer: The new layer.
        '''
        pass
    
    def on_preprintsend(self, gline, index, mainqueue):
        '''
        Called pre sending printing command.

        @param gline: Line to be send.
        @param index: Index in the mainqueue.
        @param mainqueue: The main queue of commands.
        '''
        pass
    
    def on_printsend(self, gline):
        '''
        Called whenever a line is sent to the printer.

        @param gline: The line send to the printer.
        '''
        pass
