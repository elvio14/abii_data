import pandas as pd
import inquirer

pd.set_option('display.max_columns', None)   #Always display all columns
pd.set_option('display.max_rows', None)    #Always display all rows
pd.set_option('display.width', 500)

# Load the CSV file
df = pd.read_csv('mock_data.csv')
df_usr = pd.read_csv('sync_user_profiles.csv')

df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.drop(columns=['id', 'lesson_id', 'is_external', 'is_preassessment','lesson_type']) #Exclude columns  
df = df[df['timestamp'] > '2025-05-31T23:59:59Z']   #After May 31st Only

def getAllData():      
    return df

# UPID is User Profile ID
# CLID is Cloud Learner ID (One per username)
def getDataByUPID(id):
    data = df[df['user_profile_id'] == int(id)]
    return data

def getDataByCLID(id):
    data = df[df['cloud_learner_id'] == int(id)]
    return data

def getDataByUsername(user):
    row = df_usr[df_usr['username'] == user].iloc[0]
    print("Cloud Learner ID: " + str(row['cloud_learner__id']))
    data = getDataByCLID(row['cloud_learner__id'])
    return data

def getLessonsAndDurationsByUPID(id):
    data = getDataByUPID(id)
    dataFiltered = data[['lesson_name', 'duration_ms']]
    return dataFiltered

def promptCsvOut(df):
    print(df)
    outPrompt = [inquirer.List('out', message="Output to csv?", choices=['No', 'Yes'])]
    out = inquirer.prompt(outPrompt)
    if out and out['out'] == 'Yes':
        filePrompt = [inquirer.Text('filename', message="Csv filename (without .csv)")]
        filename = inquirer.prompt(filePrompt)

        if filename:
            name = 'outputs/' + filename['filename'] + '.csv'
            df.to_csv(name, index=False)
            print("Created " + name)


def main():
    print("Welcome to the CLI tool. Press Ctrl+D or type 'exit' to quit.")
    
    while True:
        questions = [
            inquirer.List(
                'command',
                message="Select a command",
                choices=['Get All Data', 'Get Data by Cloud Learner ID', 'Get Data by Username', 'Exit'],
            ),
        ]
        answer = inquirer.prompt(questions)
        if answer is None or answer['command'] == 'Exit':
            print("Byeee!")
            break
        cmd = answer['command']

        if cmd == 'Get All Data':
            print(getAllData())
        elif cmd == 'Get Data by Cloud Learner ID':
            answer = inquirer.prompt([
                inquirer.Text('clid', message='Enter the CLID')
            ])
            if answer and 'clid' in answer:
                print("Data of CLID: " + answer['clid'])
                print(getDataByCLID(answer['clid']))
        elif cmd == 'Get Data by Username':
            answer = inquirer.prompt([
                inquirer.Text('username', message='Enter the Username')
            ])
            if answer and 'username' in answer:
                print("Data of username: " + answer['username'])
                data = getDataByUsername(answer['username'])
                promptCsvOut(data)

if __name__ == "__main__":
    main()