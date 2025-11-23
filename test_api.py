
import unittest
import requests
import uuid
from datetime import datetime, timedelta

class TestApiIntegration(unittest.TestCase):
    """
    Testes de Integração para a API Leme.
    Cria, lê, atualiza e deleta entidades para garantir o fluxo completo do CRUD.
    """
    BASE_URL = "http://127.0.0.1:8080"
    created_ids = {} # Dicionário para guardar os IDs do que for criado

    @classmethod
    def setUpClass(cls):
        """
        Prepara o ambiente de teste. Roda uma vez antes de todos os testes.
        """
        print("\nIniciando testes de integração...")
        # 1. Criar Usuário base
        user_id = str(uuid.uuid4())
        user_data = {
            "id_usuario": user_id, "nome": "Integration Test User", "username": "integ_test",
            "email": "integ@test.com", "senha": "password", "area": "it", "acessibilidade": "nenhuma",
            "modulos_concluidos": 0, "xp_total": 0, "data_cadastro": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        response = requests.post(f"{cls.BASE_URL}/usuarios", json=user_data)
        if response.status_code != 201:
            raise Exception(f"FALHA CRÍTICA: Não foi possível criar o usuário base. Testes abortados. Erro: {response.text}")
        cls.created_ids['id_usuario'] = user_id
        print(f"OK: Usuário base criado (ID: {user_id})")

        # 2. Criar Trilha base
        trilha_id = str(uuid.uuid4())
        trilha_data = {
            "id_trilha": trilha_id, "titulo": "Integration Test Trilha", "descricao": "A trilha for testing",
            "area_foco": "testing", "xp_trilha": 100, "data_criacao": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        response = requests.post(f"{cls.BASE_URL}/trilhas", json=trilha_data)
        if response.status_code != 201:
            raise Exception(f"FALHA CRÍTICA: Não foi possível criar a trilha base. Testes abortados. Erro: {response.text}")
        cls.created_ids['id_trilha'] = trilha_id
        print(f"OK: Trilha base criada (ID: {trilha_id})")

    @classmethod
    def tearDownClass(cls):
        """
        Limpa o ambiente de teste após todos os testes.
        """
        print("\nFinalizando testes e limpando banco de dados...")
        headers = {'Content-Type': 'application/json'}
        resources_to_delete = ['id_progresso', 'id_sugestao', 'id_previsao', 'id_modulo']
        endpoints = {'id_progresso': 'progressos', 'id_sugestao': 'sugestoes', 'id_previsao': 'previsoes', 'id_modulo': 'modulos'}

        for resource in resources_to_delete:
            if resource in cls.created_ids:
                res_id = cls.created_ids[resource]
                endpoint = endpoints[resource]
                requests.delete(f"{cls.BASE_URL}/{endpoint}/{res_id}", headers=headers)
        
        if 'id_trilha' in cls.created_ids:
            requests.delete(f"{cls.BASE_URL}/trilhas/{cls.created_ids['id_trilha']}", headers=headers)
        if 'id_usuario' in cls.created_ids:
            requests.delete(f"{cls.BASE_URL}/usuarios/{cls.created_ids['id_usuario']}", headers=headers)
        print("Limpeza concluída.")

    def test_01_health_check(self):
        response = requests.get(f"{self.BASE_URL}/")
        self.assertEqual(response.status_code, 200)

    def test_02_get_all_endpoints(self):
        endpoints = ['usuarios', 'trilhas', 'modulos', 'progressos', 'sugestoes', 'previsoes']
        for endpoint in endpoints:
            with self.subTest(endpoint=endpoint):
                response = requests.get(f"{self.BASE_URL}/{endpoint}")
                self.assertEqual(response.status_code, 200)
                self.assertIsInstance(response.json(), list)

    def test_03_create_modulo(self):
        modulo_id = str(uuid.uuid4())
        data = {
            "id_modulo": modulo_id, "id_trilha": self.created_ids['id_trilha'], "titulo": "Test Modulo",
            "descricao": "Test Description", "tipo": "video", "conteudo": "http://youtube.com/watch/video",
            "xp_recompensa": 50, "adaptacao_necessaria": "nenhuma"
        }
        response = requests.post(f"{self.BASE_URL}/modulos", json=data)
        self.assertEqual(response.status_code, 201, f"Erro ao criar módulo: {response.text}")
        self.__class__.created_ids['id_modulo'] = modulo_id

    def test_04_create_dependencies(self):
        self.assertIn('id_modulo', self.created_ids, "Pré-requisito falhou: Módulo não foi criado.")
        # Progresso
        progresso_id = str(uuid.uuid4())
        prog_data = {"id_progresso": progresso_id, "id_usuario": self.created_ids['id_usuario'], "id_modulo": self.created_ids['id_modulo'], "data_conclusao": datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        response = requests.post(f"{self.BASE_URL}/progressos", json=prog_data)
        self.assertEqual(response.status_code, 201, f"Erro: {response.text}")
        self.__class__.created_ids['id_progresso'] = progresso_id
        # Sugestão
        sugestao_id = str(uuid.uuid4())
        sug_data = {"id_sugestao": sugestao_id, "id_usuario": self.created_ids['id_usuario'], "id_trilha": self.created_ids['id_trilha'], "data_sugestao": datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        response = requests.post(f"{self.BASE_URL}/sugestoes", json=sug_data)
        self.assertEqual(response.status_code, 201, f"Erro: {response.text}")
        self.__class__.created_ids['id_sugestao'] = sugestao_id
        # Previsão
        previsao_id = str(uuid.uuid4())
        prev_data = {"id_previsao": previsao_id, "id_usuario": self.created_ids['id_usuario'], "taxa_sucesso": 0.95, "categoria": "Test", "data_previsao": datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        response = requests.post(f"{self.BASE_URL}/previsoes", json=prev_data)
        self.assertEqual(response.status_code, 201, f"Erro: {response.text}")
        self.__class__.created_ids['id_previsao'] = previsao_id

    def test_05_update_all(self):
        """Testa a atualização (PUT) para todos os recursos criados."""
        self.assertIn('id_modulo', self.created_ids, "Pré-requisito falhou: Entidades dependentes não foram criadas.")
        updated_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')

        # Update Usuário
        # CORRIGIDO: Adicionado 'nova_data_cadastro'
        user_data = {
            'novo_nome': 'Updated Name', 'novo_username': 'updated_user', 'novo_email': 'updated@test.com', 
            'nova_senha': 'newpass', 'nova_area': 'datascience', 'nova_acessibilidade': 'alta', 
            'novo_modulos_concluidos': 1, 'novo_xp_total': 100, 'nova_data_cadastro': updated_date
        }
        response = requests.put(f"{self.BASE_URL}/usuarios/{self.created_ids['id_usuario']}", json=user_data)
        self.assertEqual(response.status_code, 200, f"Erro ao atualizar usuário: {response.text}")

        # Update Trilha
        trilha_data = {'novo_titulo': 'Updated Trilha', 'nova_descricao': 'Updated Desc', 'nova_area_foco': 'updated_area', 'nova_xp_trilha': 250, 'nova_data_criacao': updated_date}
        response = requests.put(f"{self.BASE_URL}/trilhas/{self.created_ids['id_trilha']}", json=trilha_data)
        self.assertEqual(response.status_code, 200, f"Erro ao atualizar trilha: {response.text}")
        
        # Update Módulo
        modulo_data = {'novo_id_trilha': self.created_ids['id_trilha'], 'novo_titulo': 'Updated Modulo', 'nova_descricao': 'Updated Desc', 'novo_tipo': 'leitura', 'novo_conteudo': 'Artigo sobre TDD', 'nova_xp_recompensa': 75, 'nova_adaptacao_necessaria': 'legenda'}
        response = requests.put(f"{self.BASE_URL}/modulos/{self.created_ids['id_modulo']}", json=modulo_data)
        self.assertEqual(response.status_code, 200, f"Erro ao atualizar módulo: {response.text}")

if __name__ == '__main__':
    unittest.main(verbosity=2)
