import os
from yandex_tracker_client import TrackerClient


def handler(event, context):
    client = TrackerClient(token=os.environ['TOKEN'], cloud_org_id=os.environ['ORG_ID'])

    queryParams = event['queryStringParameters']
    issueKey = queryParams['key'] # ?key={{issue.key}} в квери параметрах запроса к CF

    currentIssue = client.issues[issueKey] # REPLACE ON {{ISSUE.KEY}}
    subtasksList = client.issues.find(f'Relates: {issueKey} Queue: HEART') # REPLACE ON {{ISSUE.KEY}}

    openTaskCount = 0

    try:
        for subtask in subtasksList:
            status = subtask['status']
            if status.name != 'Закрыт':
                openTaskCount +=  1
            else:
                pass
    except BaseException as Error:
        print("Задача отсутствуют в фильтре!")

    try:
        if openTaskCount > 0 or currentIssue.status.name == 'Закрыт':
            print(f'Функция не может быть выполнена по ряду причин: \nИсходная задача {currentIssue.key} находится в статусе "Закрыт"\nНе решены связанные задачи\nПодзадачи отсутствуют.')
        else:
            currentIssue.transitions['close'].execute(resolution='fixed', comment='Задача переведа в статус "Закрыта", так как работы над связанной задачей завершены!')
    except BaseException as BaseError:
        print("Как ты сюда вообше попал, ебик??")
    
    return {'statusCode':200}
  
