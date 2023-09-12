import pandas as pd
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

new_df = pd.DataFrame(columns=['PhoneNumber', 'Temporary', 'permanent'])

phoneNumber_TempAvail = []
phoneNumber_TempNeed = []
phoneNumber_PermAvail = []
phoneNumber_PermNeed = []
permAvail =[]
permNeed =[]
tempAvail = []
tempNeed =[]
for index, value in filtered_df.iterrows():
    if 'temporary' not in value['Message'].lower():
        if 'available' in value['Message'].lower():
            permAvail.append(value['Message'])
            phoneNumber_PermAvail.append(value['PhoneNumber'])
        else:
            permNeed.append(value['Message'])
            phoneNumber_PermNeed.append(value['PhoneNumber'])
    elif all(word in value['Message'].lower() for word in ['temporary', 'permanent', 'available']):
        tempAvail.append(value['Message'])
        phoneNumber_TempAvail.append(value['PhoneNumber'])
        permAvail.append(value['Message'])
        phoneNumber_PermAvail.append(value['PhoneNumber'])
    elif ('temporary' and 'permanent') in value['Message'].lower():
        tempNeed.append(value['Message'])
        phoneNumber_TempNeed.append(value['PhoneNumber'])
        permNeed.append(value['Message'])
        phoneNumber_PermNeed.append(value['PhoneNumber'])
    else:
        if 'available' in value['Message'].lower():
            tempAvail.append(value['Message'])
            phoneNumber_TempAvail.append(value['PhoneNumber'])
        else:
            tempNeed.append(value['Message'])
            phoneNumber_TempNeed.append(value['PhoneNumber'])

df_tempAvail = pd.DataFrame({'Temporary-Available': tempAvail})
df_tempNeed = pd.DataFrame({'Temporary-Needed': tempNeed})
df_permAvail = pd.DataFrame({'Permanent-Available': permAvail})
df_permNeed = pd.DataFrame({'Permanent-Needed': permNeed})
phNoTempAvail = pd.DataFrame({'PhoneNumber-Temporary': phoneNumber_TempAvail})
phNoTempNeed = pd.DataFrame({'PhoneNumber-Temporary': phoneNumber_TempNeed})
phNoPermAvail = pd.DataFrame({'PhoneNumber-Permanent': phoneNumber_PermAvail})
phNoPermNeed = pd.DataFrame({'PhoneNumber-Permanent': phoneNumber_PermNeed})
perm = pd.concat([phNoPermNeed, df_permNeed, phNoPermAvail, df_permAvail ], axis=1)
temp = pd.concat([phNoTempNeed,df_tempNeed,phNoTempAvail,df_tempAvail ], axis=1)
perm.to_csv('xlsxChatPerm.csv')
temp.to_csv('xlsxChatTemp.csv')














