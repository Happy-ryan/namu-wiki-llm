from elasticsearch import Elasticsearch

import yaml, json
import hashlib

class ElasticClient:
    
    def __init__(self, index_name: str, config_yaml_path: str, config_json_path: str):
        with open(config_yaml_path) as f:
            self.conf_yaml = yaml.safe_load(f)
            
        self.url = self.conf_yaml['elastic']['url']
        self.port = self.conf_yaml['elastic']['port']
        
        self.auth_id = self.conf_yaml['basic_auth']['id']
        self.auth_password = self.conf_yaml['basic_auth']['password']
        
        self.index = index_name
        
        self.es = Elasticsearch(f'{self.url}:{self.port}', basic_auth=(self.auth_id, self.auth_password), verify_certs=False)
    
        with open(config_json_path) as f:
            self.conf_json = json.load(f)
            
        self.settings = self.conf_json["settings"]
        self.mappings = self.conf_json['mappings']
        
        # 테이블 생성    
        if not self.es.indices.exists(index=self.index):
            self.es.indices.create(index=self.index, settings=self.settings, mappings=self.mappings)


    # 테이블 삭제
    def delete_index(self, index_name: str):
        if self.es.indices.exists(index= index_name):
            return self.es.indices.delete(index= index_name)


    # 도큐먼트 업데이트 > title은 불변 > content만 변경된다.
    # _id를 통해서 업데이트
    def update(self, document_id, data: dict):
        updata_body = {
            'doc': {
                'content': data['text']
            }
        }
        return self.es.update(index=self.index, id=document_id, body=updata_body)

    # 도큐먼트(피클 형식) - 삽입
    def upsert(self, file: dict):
        title, content = file['title'], file['text']
        
        data = {
            'title': title,
            'content': content
        }
        document_id = hashlib.md5(title.encode()).hexdigest()
        # title의 hash값을 _id로 설정
        # 동일한 title을 가진 document 삽입시 에러 발생 > 업데이트 진행
        # title을 그대로 _id로 설정할 경우 특수문자 등으로 인해서 에러 발생 가능성 존재하므로 안전하게 hash값으로 _id 설정
        try:
            result = self.es.index(index=self.index, body=data, id=document_id, timeout=None)
            return result
        except:
            update_result = self.updatae(document_id, data)
            return update_result


    # 해당 인덱스의 모든 도큐먼트 검색
    def search_all(self):
        body = {
            "query" : {
                "match_all": {}
            }
        }
        return self.es.search(index=self.index, body=body)


    # 쿼리에 따른 관련 도큐먼트 검색
    def search_by_field(self, query: str):
        body = {
            "query": {
                "multi_match": {
                    "query" : query,
                    "fields": ["content"],
                    "operator": "and"
                } 
            }
        }
        return self.es.search(index=self.index, body=body)
    
    
    # title의 hash 값이 _id에 해당함
    def search_by_id(self, title: str):
        document_id = hashlib.md5(title.encode()).hexdigest()
        
        body = {
            "query": {
                "term": {
                    "_id": document_id
                }
            }
        }
        
        return self.es.search(index=self.index, body=body)


    # 특정 필드와 일치하는 도큐먼트 삭제
    def delete_by_id(self, title: str):
        document_id = hashlib.md5(title.encode()).hexdigest()
        
        body = {
            "query": {
                "term": {
                    "_id": document_id
                }
            }
        }
        return self.es.delete_by_query(index=self.index, body=body)


    # 도큐먼트 일괄 삭제
    def delete_all(self):
        body = {
            "query": {
                "match_all": {}
            }
        }
        return self.es.delete_by_query(index=self.index, body=body)
