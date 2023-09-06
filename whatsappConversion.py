import pandas as pd

chat_frame = [] # array to convert to dataframe
txt_file = open("WhatsAppChatUTA.txt", 'r') # open the txt file exported for whatsapp group

text = txt_file.readlines() # to read all the rows in the text file
s
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
df.dropna(inplace=True)  ##not working!!!
df = df.drop(df[df['PhoneNumber'] == 'Messagesandcalls'].index)
df = df.drop(df[df['PhoneNumber'] == 'Groupcreatorcreated'].index)
df = df.drop(df[df['PhoneNumber'] == 'Youjoinedusing'].index)
df.drop_duplicates(subset=['Message'], keep='first', inplace=True)
df = df[df['PhoneNumber'] != 'Yoursecuritycode' ]  ##Adding condition to remove "your security code" rows
df = df[~(df['Message'].str.contains('joined') | df['Message'].str.contains('left') |
        df['Message'].str.contains('added') | df['Message'].str.contains('This message was deleted')|
        df['Message'].str.contains('added')|df['Message'].str.contains('null')|df['Message'].str.contains('Media omitted')|
        df['Message'].str.contains('changed') | df['PhoneNumber'].str.contains('changed'))] ##Removing rows with redundant data
df.to_csv("xlsxChat.csv", index=False)

##STAGE 2a - Bring out the accomodation related messages alone based on patterns

filtered_df = df[df['Message'].str.contains('accommodation', case=False)]
filtered_df.to_csv("xlsxChat.csv", index=False)

##STAGE 2c- Grouping Data as Temporary accomodation available/needed , Permanent accomodation available/needed

tempAccAvail_df = df[df['Message'].str.contains('Temporary Accommodation available', case=False)]
tempaAccNeed_df = df[(df['Message'].str.contains('temporary accommodation needed', case=False)|
                      df['Message'].str.contains('Looking for temporary accommodation', case=False)|
                      df['Message'].str.contains('Need temporary accommodation]', case=False) |
                    df['Message'].str.contains('Need a temporary accommodation]', case=False))]
permAcccAvail_df = df[df['Message'].str.contains('Permanent Accommodation available', case=False)]
permAccNeed_df = df[(df['Message'].str.contains('permanent accommodation needed', case=False)|
                     df['Message'].str.contains('Looking for permanent accommodation')|
                     df['Message'].str.contains('Looking for accommodation')|
                     df['Message'].str.contains('Looking for')|
                     df['Message'].str.contains('Need permanent accommodation ')|
                     df['Message'].str.contains('Need an accommodation'))]
