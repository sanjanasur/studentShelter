import pandas as pd
import numpy as np
chat_frame = [] # array to convert to dataframe
txt_file = open("WhatsAppChatUTA.txt", 'r') # open the txt file exported for whatsapp group

text = txt_file.readlines() # to read all the rows in the text file

for txt in text:
    print('************',txt)
    text_value = txt.split("-") #splitting the lines using "-" to separate
    print('000000000000000000000',text_value)
    try:
        if "/" == txt[2]:  #This ocndition is to check whether the coming txt line is having the Date ex: 08/08/2023
            phone_number = text_value[1].strip().split(" ")[0] + text_value[1].strip().split(" ")[1] + text_value[1].strip().split(" ")[2]
            message = text_value[1].strip()[15:] #15 is because till 14 phonenumber is here
            chat_frame.append([phone_number, message])
    except: #This except will assume all the messages without the Date at starting as message and put phone number as empty string
        phone_number = " "
        message = txt.strip()
        chat_frame.append([phone_number, message])
##STAGE 2a - Removing unwanted data
df = pd.DataFrame(chat_frame, columns=['PhoneNumber', 'Message'])
# df.dropna(inplace=True)  ##removing missing cells
# df = df.drop(df[df['PhoneNumber'] == 'Messagesandcalls'].index)
# df = df.drop(df[df['PhoneNumber'] == 'Groupcreatorcreated'].index)
# df = df.drop(df[df['PhoneNumber'] == 'Youjoinedusing'].index)
# df.drop_duplicates(subset=['Message'], keep='first', inplace=True)
# df = df[df['PhoneNumber'] != 'Yoursecuritycode' ]  ##Adding condition to remove "your security code" rows
# df = df[~(df['Message'].str.contains('joined') | df['Message'].str.contains('left') |
#         df['Message'].str.contains('added') | df['Message'].str.contains('This message was deleted')|
#         df['Message'].str.contains('added')|df['Message'].str.contains('null')|df['Message'].str.contains('Media omitted')|
#         df['Message'].str.contains('changed') | df['PhoneNumber'].str.contains('changed'))] ##Removing rows with redundant data
# df.to_csv("xlsxChat.csv", index=False)
#
# ##STAGE 2a - Bring out the accomodation related messages alone based on patterns
#
# filtered_df = df[df['Message'].str.contains('accommodation', case=False)]
# filtered_df.to_csv("xlsxChat.csv", index=False)
#
# ##STAGE 2c- Grouping Data as Temporary accomodation and Permanent Accomodation along with contact details
#
# new_df = pd.DataFrame(columns=['PhoneNumber', 'Temporary', 'permanent'])
# permList = []
# tempList = []
# phoneNumber_Temp = []
# phoneNumber_Perm = []
# for index, value in filtered_df.iterrows():
#     if 'temporary' not in value['Message'].lower():
#         permList.append(value['Message'])
#         phoneNumber_Perm.append(value['PhoneNumber'])
#     elif ('temporary' and 'permanent') in value['Message'].lower():
#         tempList.append(value['Message'])
#         phoneNumber_Temp.append(value['PhoneNumber'])
#         permList.append(value['Message'])
#         phoneNumber_Perm.append(value['PhoneNumber'])
#     else:
#         tempList.append(value['Message'])
#         phoneNumber_Temp.append(value['PhoneNumber'])
#
# df_temp = pd.DataFrame({'Temporary': tempList})
# df_perm = pd.DataFrame({'Permanent': permList})
# phoneNumberTemp = pd.DataFrame({'PhoneNumber-Temporary': phoneNumber_Temp})
# phoneNumberPerm = pd.DataFrame({'PhoneNumber-Permanent': phoneNumber_Perm})
# result = pd.concat([phoneNumberTemp,df_temp,phoneNumberPerm, df_perm], axis=1)
# result.to_csv('xlsxChat.csv')

#
new_df = pd.DataFrame(columns=['PhoneNumber', 'Temporary', 'Permanent'])
for index, value in df.iterrows():
    print('**********', value['Message'])
    if 'accommodation' in value['Message']:
        # new_df['PhoneNumber'] = value['PhoneNumber']
        phone = value['PhoneNumber']
        permanent_value = ''
        temp_value = ''
        if 'permanent' in value['Message'].lower():
            # print('entered poermanent', ['Message'])
            # new_df['permanent'] = df['Message']
            permanent_value = value['Message']
        elif 'temporary' in value['Message'].lower():
            # new_df['Temporary'] = df['Message']
            temp_value = value['Message']
        else:
            # new_df['permanent'] = None
            # new_df['Temporary'] = None
            permanent_value = None
            temp_value = None
        if permanent_value is not None and temp_value is not None:
            new_df = new_df._append({'PhoneNumber': phone, 'Temporary': temp_value, 'Permanent': permanent_value}, ignore_index = True)

new_df.to_csv('new_df.csv')





