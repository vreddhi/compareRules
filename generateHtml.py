'''
This is authored by Vreddhi Bhat. You can reach out to
vbhat@akamai.com in case of any assistance regarding this code.
'''

import os

class htmlWriter(object):
    #Class Variable Section Starts
    start_data = """
        <head>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
          <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
          <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
        </head>
        <body>
        """
    div_start_data = """
        <div class="container col-sm-4">
        <table class="table">
    """

    div_end_data = """
        </table>
        </div>
    """

    end_data = """
        </body>
    """
    #Class Variable Section Ends

    def __init__(self,filename):
        try:
            os.remove(filename)
        except FileNotFoundError:
            pass
        self.filehandler = open(filename,'a')

    def writeData(self,data):
        self.filehandler.write(data)

    def writeParentRule(self,data):
        table_row = """
            <tbody class="lead">
                <tr class="info">
                    <td>%s</td>
                </tr>
            </tbody>
        """ % (data)
        self.filehandler.write(table_row)

    def writeChildRules(self,data):
        table_row = """
            <tbody class="small">
                <tr class="active">
                    <td>%s</td>
                </tr>
            </tbody>
        """ % (data)
        self.filehandler.write(table_row)

    def writeTableHeader(self,data):
        table_heading = """
        <thead>
          <tr>
            <th>%s</th>
          </tr>
        </thead>
        """ % (data)
        self.filehandler.write(table_heading)
