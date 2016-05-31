from wrangler import dw
import sys

if(len(sys.argv) < 3):
	sys.exit('Error: Please include an input and output file.  Example python script.py input.csv output.csv')

w = dw.DataWrangler()

# Split data repeatedly on newline  into  rows
w.add(dw.Split(column=["data"],
               table=0,
               status="active",
               drop=True,
               result="row",
               update=False,
               insert_position="right",
               row=None,
               on="\n",
               before=None,
               after=None,
               ignore_between=None,
               which=1,
               max=0,
               positions=None,
               quote_character=None))

# Split data repeatedly on '|\|'
w.add(dw.Split(column=["data"],
               table=0,
               status="active",
               drop=True,
               result="column",
               update=False,
               insert_position="right",
               row=None,
               on="\\|\\|",
               before=None,
               after=None,
               ignore_between=None,
               which=1,
               max=0,
               positions=None,
               quote_character="\""))

# Delete  rows where split1 is null
w.add(dw.Filter(column=[],
                table=0,
                status="active",
                drop=False,
                row=dw.Row(column=[],
             table=0,
             status="active",
             drop=False,
             conditions=[dw.IsNull(column=[],
                table=0,
                status="active",
                drop=False,
                lcol="split1",
                value=None,
                op_str="is null")])))

# Extract from split2 on '.+' before 'director?'
w.add(dw.Extract(column=["split2"],
                 table=0,
                 status="active",
                 drop=False,
                 result="column",
                 update=False,
                 insert_position="right",
                 row=None,
                 on=".+",
                 before="director?",
                 after=None,
                 ignore_between=None,
                 which=1,
                 max=1,
                 positions=None))

# Drop split2
w.add(dw.Drop(column=["split2"],
              table=0,
              status="active",
              drop=True))

# Extract from extract on '.[A-Za-z\.\s]+'
w.add(dw.Extract(column=["extract"],
                 table=0,
                 status="active",
                 drop=False,
                 result="column",
                 update=False,
                 insert_position="right",
                 row=None,
                 on=".[A-Za-z\\\\.\\s]+",
                 before=None,
                 after=None,
                 ignore_between=None,
                 which=1,
                 max=1,
                 positions=None))

# Drop extract
w.add(dw.Drop(column=["extract"],
              table=0,
              status="active",
              drop=True))

# Extract from extract1 on '[A-Za-z\.\s]+'
w.add(dw.Extract(column=["extract1"],
                 table=0,
                 status="active",
                 drop=False,
                 result="column",
                 update=False,
                 insert_position="right",
                 row=None,
                 on="[A-Za-z\\\\.\\s]+",
                 before=None,
                 after=None,
                 ignore_between=None,
                 which=1,
                 max=1,
                 positions=None))

# Drop extract1
w.add(dw.Drop(column=["extract1"],
              table=0,
              status="active",
              drop=True))

# Extract from split4 on '.+' between 'publisher=' and '|'
w.add(dw.Extract(column=["split4"],
                 table=0,
                 status="active",
                 drop=False,
                 result="column",
                 update=False,
                 insert_position="right",
                 row=None,
                 on=".+",
                 before="\\|",
                 after="publisher=",
                 ignore_between=None,
                 which=1,
                 max=1,
                 positions=None))

# Drop split4
w.add(dw.Drop(column=["split4"],
              table=0,
              status="active",
              drop=True))

# Extract from split3 on ' any word ,s any word | any word '
w.add(dw.Extract(column=["split3"],
                 table=0,
                 status="active",
                 drop=False,
                 result="column",
                 update=False,
                 insert_position="right",
                 row=None,
                 on="[A-Za-z]+,\\s[A-Za-z]+|[A-Za-z]+",
                 before=None,
                 after=None,
                 ignore_between=None,
                 which=1,
                 max=1,
                 positions=None))

# Drop split3
w.add(dw.Drop(column=["split3"],
              table=0,
              status="active",
              drop=True))

# Extract from split1 on '.[0-9A-Za-zs]+'
w.add(dw.Extract(column=["split1"],
                 table=0,
                 status="active",
                 drop=False,
                 result="column",
                 update=False,
                 insert_position="right",
                 row=None,
                 on=".[0-9A-Za-z\\s]+",
                 before=None,
                 after=None,
                 ignore_between=None,
                 which=1,
                 max=1,
                 positions=None))

# Drop split1
w.add(dw.Drop(column=["split1"],
              table=0,
              status="active",
              drop=True))

# Extract from extract4 on '[0-9A-Za-zs]+'
w.add(dw.Extract(column=["extract4"],
                 table=0,
                 status="active",
                 drop=False,
                 result="column",
                 update=False,
                 insert_position="right",
                 row=None,
                 on="[0-9A-Za-z\\s]+",
                 before=None,
                 after=None,
                 ignore_between=None,
                 which=1,
                 max=1,
                 positions=None))

# Drop extract4
w.add(dw.Drop(column=["extract4"],
              table=0,
              status="active",
              drop=True))

# Extract from split on '.+' after '[\['
w.add(dw.Extract(column=["split"],
                 table=0,
                 status="active",
                 drop=False,
                 result="column",
                 update=False,
                 insert_position="right",
                 row=None,
                 on=".+",
                 before=None,
                 after="\\[\\[",
                 ignore_between=None,
                 which=1,
                 max=1,
                 positions=None))

# Drop split
w.add(dw.Drop(column=["split"],
              table=0,
              status="active",
              drop=True))

# Extract from extract6 on '.+' before ']]'
w.add(dw.Extract(column=["extract6"],
                 table=0,
                 status="active",
                 drop=False,
                 result="column",
                 update=False,
                 insert_position="right",
                 row=None,
                 on=".+",
                 before="]]",
                 after=None,
                 ignore_between=None,
                 which=1,
                 max=1,
                 positions=None))

# Drop extract6
w.add(dw.Drop(column=["extract6"],
              table=0,
              status="active",
              drop=True))

# Extract from extract7 on '[0-9A-Za-zs]+'
w.add(dw.Extract(column=["extract7"],
                 table=0,
                 status="active",
                 drop=False,
                 result="column",
                 update=False,
                 insert_position="right",
                 row=None,
                 on="[0-9A-Za-z\\s]+",
                 before=None,
                 after=None,
                 ignore_between=None,
                 which=1,
                 max=1,
                 positions=None))

# Drop extract7
w.add(dw.Drop(column=["extract7"],
              table=0,
              status="active",
              drop=True))

# Merge   with glue  , 
w.add(dw.Merge(column=[],
               table=0,
               status="active",
               drop=False,
               result="column",
               update=False,
               insert_position="right",
               row=dw.Row(column=[],
             table=0,
             status="active",
             drop=False,
             conditions=[dw.RowIndex(column=[],
                  table=0,
                  status="active",
                  drop=False,
                  indices=[0,1,2,3,4,5])]),
               glue=", "))

# Drop extract8, extract5, extract, extract3...
w.add(dw.Drop(column=["extract8","extract5","extract","extract3","extract2"],
              table=0,
              status="active",
              drop=True))

w.apply_to_file(sys.argv[1]).print_csv(sys.argv[2])


