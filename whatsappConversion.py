import pandas as pd
import re
import numpy as np
chat_frame = [] # array to convert to dataframe
txt_file = open("WhatsAppChatUTA.txt", 'r') # open the txt file exported for whatsapp group

text = txt_file.readlines() # to read all the rows in the text file

for txt in text:
    text_value = txt.split("-")
    try:
        if "/" == txt[2]:
            phone_number = text_value[1].strip().split(" ")[0] + text_value[1].strip().split(" ")[1] + text_value[1].strip().split(" ")[2]
            message = text_value[1].strip()[15:]
            chat_frame.append([phone_number, message])
    except:
        phone_number = " "
        message = txt.strip()
        chat_frame.append([phone_number, message])
##STAGE 2a - Removing unwanted data
df = pd.DataFrame(chat_frame, columns=['PhoneNumber', 'Message'])
df.dropna(inplace=True)  ##removing missing cells
df = df.drop(df[df['PhoneNumber'] == 'Messagesandcalls'].index)
df = df.drop(df[df['PhoneNumber'] == 'Groupcreatorcreated'].index)
df = df.drop(df[df['PhoneNumber'] == 'Youjoinedusing'].index)
df.drop_duplicates(subset=['Message'], keep='first', inplace=True)
df = df[df['PhoneNumber'] != 'Yoursecuritycode' ]  ##Adding condition to remove "your security code" rows
df = df[~(df['Message'].str.contains('joined') | df['Message'].str.contains('left') |
        df['Message'].str.contains('added') | df['Message'].str.contains('This message was deleted')|
        df['Message'].str.contains('added')|df['Message'].str.contains('null')|df['Message'].str.contains('Media omitted')|
        df['Message'].str.contains('changed') | df['PhoneNumber'].str.contains('changed'))] ##Removing rows with redundant data
#df.to_csv("xlsxChat.csv", index=False)

##STAGE 2a - Bring out the accomodation related messages alone based on patterns

filtered_df = df[df['Message'].str.contains('accommodation', case=False)]
filtered_df.to_csv("xlsxChat.csv", index=False)

##STAGE 2c- Grouping Data as Temporary accomodation and Permanent Accomodation needed/available along with contact details
##Stage 2c-ii - Added columns by parsing through message
#NOTE: skipping temporary acc processing for first stage of project
new_df = pd.DataFrame(columns=['PhoneNumber', 'Temporary', 'permanent'])

phoneNumber_PermAvail = []
phoneNumber_PermNeed = []
gender_avail=[]
gender_need=[]
noAvail = []
noNeed = []
rentAvail =[]
rentNeed = []
for index, value in filtered_df.iterrows():
    if 'temporary' not in value['Message'].lower():
        if 'available' in value['Message'].lower():
            for val in ['boy', 'boys', 'girl', 'girls', 'male', 'males', 'female', 'females', 'guy', 'guys']:
                if val in value['Message'].lower():
                    gender_avail.append(val)
                    phoneNumber_PermAvail.append(value['PhoneNumber'])
                    pattern = r'(\d+)\s*(girl|girls|boy|boys|male|males|female|females|guy|guys)'

                    # Use re.findall to find all matches in the string
                    matches = re.findall(pattern, value['Message'])

            # Initialize a variable to store the total number of girls
                    total = 0

            # Iterate through the matches and add up the number of girls
                    for match in matches:
                        number, _ = match
                        total += int(number)
                    noAvail.append(total)
                    pattern1 = r'\$(\d+)'
                    match1 = re.search(pattern1, value['Message'])
                    pattern2 = r'(\d+)\$'
                    match2 = re.search(pattern2, value['Message'])

                    if match1:
                        rentAvail.append(match1.group(1))
                    elif match2:
                        rentAvail.append(match2.group(1))

                    else:
                        rentAvail.append("350")
        else:
            for val in ['boy', 'boys', 'girl', 'girls', 'male', 'males', 'female', 'females', 'guy', 'guys']:
                if val in value['Message'].lower():
                    gender_need.append(val)
                    phoneNumber_PermNeed.append(value['PhoneNumber'])
                    pattern = r'(\d+)\s*(girl|girls|boy|boys|male|males|female|females|guy|guys)'

                    # Use re.findall to find all matches in the string
                    matches = re.findall(pattern, value['Message'])

                    # Initialize a variable to store the total number of girls
                    total = 0

                    # Iterate through the matches and add up the number of girls
                    for match in matches:
                       number, _ = match
                       total += int(number)
                    noNeed.append(total)
                    pattern1 = r'\$(\d+)'
                    match1 = re.search(pattern1, value['Message'])
                    pattern2 = r'(\d+)\$'
                    match2 = re.search(pattern2, value['Message'])

                    if match1:
                        rentNeed.append(match1.group(1))
                    elif match2:
                        rentNeed.append(match2.group(1))

                    else:
                        rentNeed.append("350")
    elif all(word in value['Message'].lower() for word in ['temporary', 'permanent', 'available']):
        for val in ['boy', 'boys', 'girl', 'girls', 'male', 'males', 'female', 'females', 'guy', 'guys']:
            if val in value['Message'].lower():
                gender_avail.append(val)
                phoneNumber_PermAvail.append(value['PhoneNumber'])
                pattern = r'(\d+)\s*(girl|girls|boy|boys|male|males|female|females|guy|guys)'

                # Use re.findall to find all matches in the string
                matches = re.findall(pattern, value['Message'])

                # Initialize a variable to store the total number of girls
                total = 0

             # Iterate through the matches and add up the number of girls
                for match in matches:
                  number, _ = match
                  total += int(number)
                noAvail.append(total)
                pattern1 = r'\$(\d+)'
                match1 = re.search(pattern1, value['Message'])
                pattern2 = r'(\d+)\$'
                match2 = re.search(pattern2, value['Message'])

                if match1:
                    rentAvail.append(match1.group(1))
                elif match2:
                    rentAvail.append(match2.group(1))

                else:
                    rentAvail.append("350")

    elif ('temporary' and 'permanent') in value['Message'].lower():
        for val in ['boy', 'boys', 'girl', 'girls', 'male', 'males', 'female', 'females', 'guy', 'guys']:
            if val in value['Message'].lower():
                gender_need.append(val)
                phoneNumber_PermNeed.append(value['PhoneNumber'])
                pattern = r'(\d+)\s*(girl|girls|boy|boys|male|males|female|females|guy|guys)'

                # Use re.findall to find all matches in the string
                matches = re.findall(pattern, value['Message'])
                # Initialize a variable to store the total number of girls
                total = 0
                # Iterate through the matches and add up the number of girls
                for match in matches:
                    number, _ = match
                    total += int(number)
                noNeed.append(total)
                pattern1 = r'\$(\d+)'
                match1 = re.search(pattern1, value['Message'])
                pattern2 = r'(\d+)\$'
                match2 = re.search(pattern2, value['Message'])

                if match1:
                    rentNeed.append(match1.group(1))
                elif match2:
                    rentNeed.append(match2.group(1))

                else:
                    rentNeed.append("350")




df_phAvail = pd.DataFrame({'PhNumber-Available': phoneNumber_PermAvail})
df_genAvail = pd.DataFrame({'GenderAvail': gender_avail})
df_noAvail = pd.DataFrame({'no': noAvail})
df_noAvail.loc[df_noAvail['no'] == 0, 'no'] = 1   #ADD CONDITION FOR EMPTY CELLS ALSO AS DEFAULT 1
df_rentAvail = pd.DataFrame({'Rent': rentAvail})
df_phNeed = pd.DataFrame({'PhNumber-Needed': phoneNumber_PermNeed})
df_genNeed = pd.DataFrame({'GenderNeed': gender_need})
df_noNeed = pd.DataFrame({'no': noNeed})
df_noNeed.loc[df_noNeed['no'] == 0, 'no'] = 1    #ADD CONDITION FOR EMPTY CELLS ALSO AS DEFAULT 1
df_rentNeed = pd.DataFrame({'Rent': rentNeed})
df_permAvail = pd.concat([df_phAvail , df_genAvail,df_noAvail,df_rentAvail], axis=1)
df_permNeed = pd.concat([df_phNeed , df_genNeed,df_noNeed,df_rentNeed], axis=1)

df_permAvail.to_csv("permAvail.csv", index=False)

df_permNeed.to_csv("permNeed.csv", index=False)