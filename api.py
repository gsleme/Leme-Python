
from flask import Flask, jsonify, request
from usuarios import create_usuario, read_usuario, update_usuario, delete_usuario
from modulos import create_modulo, read_modulo, update_modulo, delete_modulo
from trilhas import create_trilha, read_trilha, update_trilha, delete_trilha
from previsoes import create_previsao, read_previsao, update_previsao, delete_previsao
from progressos import create_progresso, read_progresso, update_progresso, delete_progresso
from sugestoes import create_sugestao, read_sugestao, update_sugestao, delete_sugestao

app = Flask(__name__)

# Health check endpoint
@app.route('/')
def health_check():
    return jsonify({"status": "healthy"}), 200

# --- Endpoints de USUÁRIOS ---
@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    return jsonify(read_usuario() or [])

@app.route('/usuarios', methods=['POST'])
def post_usuario():
    dados = request.get_json()
    if not dados or not all(k in dados for k in ['id_usuario', 'nome', 'username', 'email', 'senha', 'area', 'acessibilidade', 'modulos_concluidos', 'xp_total', 'data_cadastro']):
        return jsonify({'error': 'Dados incompletos para criar usuário'}), 400
    if create_usuario(**dados):
        return jsonify({'message': 'Usuário criado com sucesso'}), 201
    return jsonify({'error': 'Erro ao criar usuário'}), 500

@app.route('/usuarios/<string:id_usuario>', methods=['PUT'])
def put_usuario(id_usuario):
    dados = request.get_json()
    if not dados or not all(k in dados for k in ['novo_nome', 'novo_username', 'novo_email', 'nova_senha', 'nova_area', 'nova_acessibilidade', 'novo_modulos_concluidos', 'novo_xp_total', 'nova_data_cadastro']):
        return jsonify({'error': 'Dados incompletos para atualizar usuário'}), 400
    if update_usuario(id_usuario, **dados):
        return jsonify({'message': 'Usuário atualizado com sucesso'})
    return jsonify({'error': 'Usuário não encontrado ou erro na atualização'}), 404

@app.route('/usuarios/<string:id_usuario>', methods=['DELETE'])
def delete_usuario_endpoint(id_usuario):
    if delete_usuario(id_usuario):
        return jsonify({'message': 'Usuário deletado com sucesso'})
    return jsonify({'error': 'Usuário não encontrado ou erro ao deletar'}), 404

# --- Endpoints de MÓDULOS ---
@app.route('/modulos', methods=['GET'])
def get_modulos():
    return jsonify(read_modulo() or [])

@app.route('/modulos', methods=['POST'])
def post_modulo():
    dados = request.get_json()
    if not dados or not all(k in dados for k in ['id_modulo', 'id_trilha', 'nome', 'descricao', 'conteudo', 'duracao_horas']):
        return jsonify({'error': 'Dados incompletos para criar módulo'}), 400
    if create_modulo(**dados):
        return jsonify({'message': 'Módulo criado com sucesso'}), 201
    return jsonify({'error': 'Erro ao criar módulo'}), 500

@app.route('/modulos/<string:id_modulo>', methods=['PUT'])
def put_modulo(id_modulo):
    dados = request.get_json()
    if not dados or not all(k in dados for k in ['novo_nome', 'nova_descricao', 'novo_conteudo', 'nova_duracao_horas']):
        return jsonify({'error': 'Dados incompletos para atualizar módulo'}), 400
    if update_modulo(id_modulo, **dados):
        return jsonify({'message': 'Módulo atualizado com sucesso'})
    return jsonify({'error': 'Módulo não encontrado ou erro na atualização'}), 404

@app.route('/modulos/<string:id_modulo>', methods=['DELETE'])
def delete_modulo_endpoint(id_modulo):
    if delete_modulo(id_modulo):
        return jsonify({'message': 'Módulo deletado com sucesso'})
    return jsonify({'error': 'Módulo não encontrado ou erro ao deletar'}), 404

# --- Endpoints de TRILHAS ---
@app.route('/trilhas', methods=['GET'])
def get_trilhas():
    return jsonify(read_trilha() or [])

@app.route('/trilhas', methods=['POST'])
def post_trilha():
    dados = request.get_json()
    if not dados or not all(k in dados for k in ['id_trilha', 'nome', 'descricao', 'area_principal']):
        return jsonify({'error': 'Dados incompletos para criar trilha'}), 400
    if create_trilha(**dados):
        return jsonify({'message': 'Trilha criada com sucesso'}), 201
    return jsonify({'error': 'Erro ao criar trilha'}), 500

@app.route('/trilhas/<string:id_trilha>', methods=['PUT'])
def put_trilha(id_trilha):
    dados = request.get_json()
    if not dados or not all(k in dados for k in ['novo_nome', 'nova_descricao', 'nova_area_principal']):
        return jsonify({'error': 'Dados incompletos para atualizar trilha'}), 400
    if update_trilha(id_trilha, **dados):
        return jsonify({'message': 'Trilha atualizada com sucesso'})
    return jsonify({'error': 'Trilha não encontrada ou erro na atualização'}), 404

@app.route('/trilhas/<string:id_trilha>', methods=['DELETE'])
def delete_trilha_endpoint(id_trilha):
    if delete_trilha(id_trilha):
        return jsonify({'message': 'Trilha deletada com sucesso'})
    return jsonify({'error': 'Trilha não encontrada ou erro ao deletar'}), 404

# --- Endpoints de PROGRESSOS ---
@app.route('/progressos', methods=['GET'])
def get_progressos():
    return jsonify(read_progresso() or [])

@app.route('/progressos', methods=['POST'])
def post_progresso():
    dados = request.get_json()
    if not dados or not all(k in dados for k in ['id_progresso', 'id_usuario', 'id_modulo', 'data_conclusao']):
        return jsonify({'error': 'Dados incompletos para criar progresso'}), 400
    if create_progresso(**dados):
        return jsonify({'message': 'Progresso criado com sucesso'}), 201
    return jsonify({'error': 'Erro ao criar progresso'}), 500

@app.route('/progressos/<string:id_progresso>', methods=['PUT'])
def put_progresso(id_progresso):
    dados = request.get_json()
    if not dados or not all(k in dados for k in ['novo_id_usuario', 'novo_id_modulo', 'nova_data_conclusao']):
        return jsonify({'error': 'Dados incompletos para atualizar progresso'}), 400
    if update_progresso(id_progresso, **dados):
        return jsonify({'message': 'Progresso atualizado com sucesso'})
    return jsonify({'error': 'Progresso não encontrado ou erro na atualização'}), 404

@app.route('/progressos/<string:id_progresso>', methods=['DELETE'])
def delete_progresso_endpoint(id_progresso):
    if delete_progresso(id_progresso):
        return jsonify({'message': 'Progresso deletado com sucesso'})
    return jsonify({'error': 'Progresso não encontrado ou erro ao deletar'}), 404

# --- Endpoints de SUGESTÕES ---
@app.route('/sugestoes', methods=['GET'])
def get_sugestoes():
    return jsonify(read_sugestao() or [])

@app.route('/sugestoes', methods=['POST'])
def post_sugestao():
    dados = request.get_json()
    if not dados or not all(k in dados for k in ['id_sugestao', 'id_usuario', 'id_trilha', 'data_sugestao']):
        return jsonify({'error': 'Dados incompletos para criar sugestão'}), 400
    if create_sugestao(**dados):
        return jsonify({'message': 'Sugestão criada com sucesso'}), 201
    return jsonify({'error': 'Erro ao criar sugestão'}), 500

@app.route('/sugestoes/<string:id_sugestao>', methods=['PUT'])
def put_sugestao(id_sugestao):
    dados = request.get_json()
    if not dados or not all(k in dados for k in ['novo_id_usuario', 'novo_id_trilha', 'nova_data_sugestao']):
        return jsonify({'error': 'Dados incompletos para atualizar sugestão'}), 400
    if update_sugestao(id_sugestao, **dados):
        return jsonify({'message': 'Sugestão atualizada com sucesso'})
    return jsonify({'error': 'Sugestão não encontrada ou erro na atualização'}), 404

@app.route('/sugestoes/<string:id_sugestao>', methods=['DELETE'])
def delete_sugestao_endpoint(id_sugestao):
    if delete_sugestao(id_sugestao):
        return jsonify({'message': 'Sugestão deletada com sucesso'})
    return jsonify({'error': 'Sugestão não encontrada ou erro ao deletar'}), 404

# --- Endpoints de PREVISÕES ---
@app.route('/previsoes', methods=['GET'])
def get_previsoes():
    return jsonify(read_previsao() or [])

@app.route('/previsoes', methods=['POST'])
def post_previsao():
    dados = request.get_json()
    if not dados or not all(k in dados for k in ['id_previsao', 'id_usuario', 'taxa_sucesso', 'categoria', 'data_previsao']):
        return jsonify({'error': 'Dados incompletos para criar previsão'}), 400
    if create_previsao(**dados):
        return jsonify({'message': 'Previsão criada com sucesso'}), 201
    return jsonify({'error': 'Erro ao criar previsão'}), 500

@app.route('/previsoes/<string:id_previsao>', methods=['PUT'])
def put_previsao(id_previsao):
    dados = request.get_json()
    if not dados or not all(k in dados for k in ['novo_id_usuario', 'nova_taxa_sucesso', 'nova_categoria', 'nova_data_previsao']):
        return jsonify({'error': 'Dados incompletos para atualizar previsão'}), 400
    if update_previsao(id_previsao, **dados):
        return jsonify({'message': 'Previsão atualizada com sucesso'})
    return jsonify({'error': 'Previsão não encontrada ou erro na atualização'}), 404

@app.route('/previsoes/<string:id_previsao>', methods=['DELETE'])
def delete_previsao_endpoint(id_previsao):
    if delete_previsao(id_previsao):
        return jsonify({'message': 'Previsão deletada com sucesso'})
    return jsonify({'error': 'Previsão não encontrada ou erro ao deletar'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)