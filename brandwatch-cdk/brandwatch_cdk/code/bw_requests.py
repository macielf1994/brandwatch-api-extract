import requests
import json
import time
from datetime import datetime
import boto3

class BWRequests:

    def get_token(email_brandwatch, pass_brandwatch):
        json_token = requests.post(
            'https://api.brandwatch.com/oauth/token',
            params = {
                'username': email_brandwatch,
                'password': pass_brandwatch,
                'grant_type': 'api-password',
                'client_id': 'brandwatch-api-client'
            }
        ).json()

        access_token = json_token['access_token']

        print('Token de acesso:', access_token)
        
        return access_token

    def get_projects(access_token: str, list_project_ids_filter: list = None):
        json_projects = requests.get(
            'https://api.brandwatch.com/projects/summary',
            headers = {
                'Authorization': 'bearer {}'.format(access_token)
            }   
        ).json()

        field_results = json_projects['results']
        list_project_ids = []
        list_project_names = []

        if list_project_ids_filter:
            for project in field_results:
                if project['id'] in list_project_ids_filter:
                    list_project_ids.append(project['id'])
                    list_project_names.append(project['name'])
        else:
            for project in field_results:
                list_project_ids.append(project['id'])
                list_project_names.append(project['name'])

        return list_project_ids

    def get_queries(access_token: str, project_list_id: list):
        
        list_tuples_project_query_id = []

        for project_id in project_list_id:
            time.sleep(5)
            json_queries = requests.get(
                    'https://api.brandwatch.com/projects/{}/queries/summary'.format(project_id),
                    headers = {
                    'Authorization': 'bearer {}'.format(access_token)
                }
            ).json()


            field_results = json_queries['results']
            list_queries_ids = [querie_id['id'] for querie_id in field_results]
            list_tuples_project_query_id.append((project_id, list_queries_ids))

        print('Project ID:', list_tuples_project_query_id[0][0], 'Lista de Querie IDs do projeto:', list_tuples_project_query_id[0][1])

        return list_tuples_project_query_id

    def get_mentions(access_token: str, list_tuples_project_query_id: list, start_date: str, end_date: str, page_size: int):
        date_today = datetime.today().strftime('%Y%m%d%H%M%S')
        s3 = boto3.client('s3')

        for project_id in list_tuples_project_query_id:
            for querie_id in project_id[1]:
                time.sleep(5)

                json_mentions = requests.get(
                    'https://api.brandwatch.com/projects/{}/data/mentions?queryId={}&startDate={}&endDate={}&pageSize={}&orderBy=date&orderDirection=asc'.format(
                        project_id[0], 
                        querie_id, 
                        start_date,
                        end_date, 
                        page_size
                        ),
                    headers = {
                        'Authorization': 'bearer {}'.format(access_token)
                    }
                ).json()

                s3.put_object(
                    Body=str(json.dumps(json_mentions)),
                    Bucket='data-lake-brandtest',
                    Key='landing/social/brandwatch_mentions/P_{}_Q_{}_PG_{}_DATEHRMS_{}.json'.format(project_id[0], querie_id, json_mentions['resultsPage'], date_today)
                )

                if 'nextCursor' in json_mentions:
                    next_cursor = json_mentions['nextCursor']
                    print('Página', json_mentions['resultsPage'], 'de menções, para a querie id', querie_id, 'o cursor para a próxima pagina é:', next_cursor)
                    while next_cursor != None:
                        next_page_json_mentions = requests.get(
                            'https://api.brandwatch.com/projects/{}/data/mentions?queryId={}&startDate={}&endDate={}&pageSize={}&orderBy=date&orderDirection=asc&cursor={}'.format(
                                project_id[0],
                                querie_id, 
                                start_date,
                                end_date, 
                                page_size,
                                next_cursor
                                ),
                            headers = {
                                'Authorization': 'bearer {}'.format(access_token)
                            }
                        ).json()

                        s3.put_object(
                            Body=str(json.dumps(next_page_json_mentions)),
                            Bucket='data-lake-brandtest',
                            Key='landing/social/brandwatch_mentions/P_{}_Q_{}_PG_{}_DATEHRMS_{}.json'.format(project_id[0], querie_id, next_page_json_mentions['resultsPage'], date_today)
                        )

                        if 'nextCursor' in next_page_json_mentions:
                            next_cursor = next_page_json_mentions['nextCursor']
                            print('Página', next_page_json_mentions['resultsPage'], 'de menções, para a querie id', querie_id, 'o cursor para a próxima pagina é:', next_cursor)
                        else:
                            print('Página', next_page_json_mentions['resultsPage'], 'de menções, não há mais páginas para a querie id', querie_id)
                            next_cursor = None
                else:
                    print('Página', json_mentions['resultsPage'], 'de menções, não há mais páginas para a querie id', querie_id)