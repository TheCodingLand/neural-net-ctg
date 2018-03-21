import json
with open('data.json') as f:
    data=json.load(f)
    out=[]
    if data['status'] == "success":
        data = data['Ticket']
       
        
        entries = []
        for item in data:
            item=item['data']
            text = ""
            fields= ["Title", "Description",'AssociatedCategory']
            labelfield = "AssociatedCategory"

            for field in fields:
                if field !=labelfield:
                    text = text + item[field]
                if field == labelfield:
                    label = item[field]
            
            entry = {"label":label, "text":text}
            entries.append(entry)
        

        result = { 'entries' : entries }
        f = open('data2.json', 'w')
        json.dump(result, f)