# main.py - Versão Corrigida e Melhorada

from flask import Flask, request, jsonify, Response
import json
import os

app = Flask(__name__)

# Nome do arquivo que vai armazenar os dados da pesquisa
DATA_FILE = 'data.json'

# --- Funções Auxiliares para Manipular o Arquivo de Dados ---

def read_data():
    """Lê os dados do arquivo JSON. Se o arquivo não existir, retorna uma lista vazia."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        # Se o arquivo estiver vazio ou corrompido, começa do zero
        return []

def write_data(data):
    """Escreve os dados no arquivo JSON."""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# --- Definição das Rotas da Aplicação ---

@app.route('/')
def home():
    """Exibe a página principal com o formulário da pesquisa."""
    
    # O HTML abaixo é a nova versão do formulário, com validações, melhor usabilidade e design.
    html_content = """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Pesquisa de Ostomia - Participe</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { background-color: #f8f9fa; }
            .container { max-width: 700px; }
            .card { margin-top: 2rem; }
            .form-group label { font-weight: 500; }
            .hidden { display: none; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="card shadow-sm">
                <div class="card-body p-4">
                    <h2 class="card-title text-center mb-4">Pesquisa sobre a Vida com Ostomia</h2>
                    <p class="text-center text-muted">Sua participação é anônima e muito importante para nós. Leva apenas alguns minutos.</p>
                    <hr>

                    <!-- Formulário Corrigido -->
                    <form id="surveyForm">
                        <!-- Informações Pessoais -->
                        <div class="mb-3 form-group">
                            <label for="idade" class="form-label">Qual a sua idade?</label>
                            <input type="number" class="form-control" id="idade" name="idade" required>
                        </div>

                        <div class="mb-3 form-group">
                            <label for="genero" class="form-label">Com qual gênero você se identifica?</label>
                            <select class="form-select" id="genero" name="genero" required>
                                <option value="" selected disabled>Selecione...</option>
                                <option value="Masculino">Masculino</option>
                                <option value="Feminino">Feminino</option>
                                <option value="Outro">Outro</option>
                                <option value="Prefiro não informar">Prefiro não informar</option>
                            </select>
                        </div>

                        <div class="mb-3 form-group">
                            <label for="email" class="form-label">Qual o seu email? (Opcional - para contato futuro)</label>
                            <input type="email" class="form-control" id="email" name="email" placeholder="seuemail@exemplo.com">
                        </div>

                        <!-- Detalhes da Ostomia -->
                        <h5 class="mt-4">Sobre a Ostomia</h5>
                        <div class="mb-3 form-group">
                            <label class="form-label">Qual o tipo da sua ostomia? (Escolha única)</label>
                            <div class="form-check">
                                <input class="form-check-input" type="radio" name="tipo_ostomia" id="colostomia" value="Colostomia" required>
                                <label class="form-check-label" for="colostomia">Colostomia</label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input" type="radio" name="tipo_ostomia" id="ileostomia" value="Ileostomia">
                                <label class="form-check-label" for="ileostomia">Ileostomia</label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input" type="radio" name="tipo_ostomia" id="urostomia" value="Urostomia">
                                <label class="form-check-label" for="urostomia">Urostomia</label>
                            </div>
                        </div>

                        <div class="mb-3 form-group">
                            <label for="tempo_ostomia" class="form-label">Há quanto tempo você tem a ostomia?</label>
                            <input type="text" class="form-control" id="tempo_ostomia" name="tempo_ostomia" placeholder="Ex: 2 anos e 6 meses" required>
                        </div>

                        <!-- Produtos -->
                        <h5 class="mt-4">Produtos e Cuidados</h5>
                        <div class="mb-3 form-group">
                            <label class="form-label">Você utiliza algum produto específico (bolsas, placas, etc.)?</label>
                            <div class="form-check">
                                <input class="form-check-input" type="radio" name="usa_produto_especifico" id="usa_produto_sim" value="Sim" required>
                                <label class="form-check-label" for="usa_produto_sim">Sim</label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input" type="radio" name="usa_produto_especifico" id="usa_produto_nao" value="Não">
                                <label class="form-check-label" for="usa_produto_nao">Não</label>
                            </div>
                        </div>

                        <div class="mb-3 form-group hidden" id="produtos_especificos_div">
                            <label for="produtos_especificos" class="form-label">Se sim, quais produtos você mais utiliza?</label>
                            <textarea class="form-control" id="produtos_especificos" name="produtos_especificos" rows="3"></textarea>
                        </div>

                        <!-- Desafios e Suporte -->
                        <h5 class="mt-4">Desafios e Suporte</h5>
                         <div class="mb-3 form-group">
                            <label for="desafios" class="form-label">Quais são seus maiores desafios no dia a dia?</label>
                            <textarea class="form-control" id="desafios" name="desafios" rows="3" required></textarea>
                        </div>

                        <div class="mb-3 form-group">
                            <label for="sugestoes" class="form-label">Você tem alguma sugestão de melhoria ou gostaria de compartilhar algo mais?</label>
                            <textarea class="form-control" id="sugestoes" name="sugestoes" rows="3"></textarea>
                        </div>
                        
                        <!-- Feedback e Botão de Envio -->
                        <div id="form-feedback" class="mt-3"></div>
                        
                        <div class="d-grid gap-2 mt-4">
                            <button type="submit" class="btn btn-primary btn-lg" id="submit-button">Enviar Resposta</button>
                        </div>
                    </form>
                </div>
            </div>
            <footer class="text-center my-4 text-muted">
                <p>© 2024 Pesquisa de Ostomia. Todos os direitos reservados.</p>
            </footer>
        </div>

        <script>
            // Lógica para mostrar/ocultar campo de produtos
            const radioUsaProduto = document.querySelectorAll('input[name="usa_produto_especifico"]');
            const produtosDiv = document.getElementById('produtos_especificos_div');
            const produtosTextarea = document.getElementById('produtos_especificos');

            radioUsaProduto.forEach(radio => {
                radio.addEventListener('change', (event) => {
                    if (event.target.value === 'Sim') {
                        produtosDiv.classList.remove('hidden');
                        produtosTextarea.required = true;
                    } else {
                        produtosDiv.classList.add('hidden');
                        produtosTextarea.required = false;
                        produtosTextarea.value = ''; // Limpa o campo ao esconder
                    }
                });
            });

            // Lógica de envio do formulário
            const form = document.getElementById('surveyForm');
            const submitButton = document.getElementById('submit-button');
            const formFeedback = document.getElementById('form-feedback');

            form.addEventListener('submit', async (event) => {
                event.preventDefault(); // Impede o envio padrão do formulário

                submitButton.disabled = true;
                submitButton.textContent = 'Enviando...';
                formFeedback.innerHTML = '';

                // Coleta os dados do formulário
                const formData = new FormData(form);
                const data = {};
                formData.forEach((value, key) => {
                    data[key] = value;
                });

                try {
                    const response = await fetch('/submit', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(data)
                    });

                    if (response.ok) {
                        form.reset(); // Limpa o formulário
                        form.classList.add('hidden'); // Esconde o formulário
                        formFeedback.innerHTML = `
                            <div class="alert alert-success">
                                <h4>Obrigado!</h4>
                                <p>Sua resposta foi enviada com sucesso e nos ajudará muito.</p>
                            </div>`;
                    } else {
                        throw new Error('Falha no envio.');
                    }

                } catch (error) {
                    formFeedback.innerHTML = `
                        <div class="alert alert-danger">
                            <strong>Erro!</strong> Não foi possível enviar sua resposta. Por favor, tente novamente mais tarde.
                        </div>`;
                    submitButton.disabled = false;
                    submitButton.textContent = 'Enviar Resposta';
                }
            });
        </script>
    </body>
    </html>
    """
    return Response(html_content, mimetype='text/html')

@app.route('/admin')
def admin_page():
    """Exibe o painel do administrador para visualizar as respostas."""
    
    # O HTML abaixo é a nova versão da página de admin, que mostra os dados em uma tabela organizada.
    html_content = """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Admin - Respostas da Pesquisa</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { background-color: #f8f9fa; }
            .table-responsive {
                max-height: 80vh; /* Para tabelas muito grandes */
            }
            th, td {
                white-space: nowrap; /* Impede que o texto quebre linha */
                vertical-align: middle;
            }
            td {
                white-space: normal; /* Permite que respostas longas quebrem linha */
            }
        </style>
    </head>
    <body>
        <div class="container-fluid mt-4">
            <h1 class="text-center mb-4">Painel Administrativo - Respostas</h1>
            
            <div id="loading" class="text-center">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Carregando...</span>
                </div>
                <p>Carregando respostas...</p>
            </div>

            <div id="error" class="alert alert-danger d-none">
                Não foi possível carregar os dados. Verifique o console para mais detalhes.
            </div>
            
            <div class="table-responsive">
                <table class="table table-striped table-bordered table-hover d-none" id="responses-table">
                    <thead class="table-dark">
                        <!-- O cabeçalho da tabela será gerado dinamicamente -->
                    </thead>
                    <tbody>
                        <!-- As linhas de dados serão inseridas aqui -->
                    </tbody>
                </table>
            </div>
        </div>

        <script>
            // Função para autenticar e buscar os dados
            async function authenticateAndFetch() {
                const password = prompt("Por favor, insira a senha de administrador:", "");
                if (password !== "admin123") {
                    alert("Senha incorreta!");
                    document.getElementById('loading').innerHTML = '<p class="text-danger">Acesso Negado</p>';
                    return;
                }

                try {
                    const response = await fetch('/data'); // Endpoint que fornece os dados
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    const data = await response.json();
                    displayDataAsTable(data);
                } catch (e) {
                    console.error("Erro ao buscar dados:", e);
                    document.getElementById('loading').classList.add('d-none');
                    document.getElementById('error').classList.remove('d-none');
                }
            }

            function displayDataAsTable(data) {
                const table = document.getElementById('responses-table');
                const thead = table.querySelector('thead');
                const tbody = table.querySelector('tbody');

                document.getElementById('loading').classList.add('d-none'); // Esconde o loading

                if (!data || data.length === 0) {
                    document.getElementById('loading').innerHTML = '<p class="text-info">Nenhuma resposta foi recebida ainda.</p>';
                    document.getElementById('loading').classList.remove('d-none');
                    return;
                }

                // Cria o cabeçalho da tabela com base nas chaves do primeiro objeto
                const headers = Object.keys(data[0]);
                let headerHtml = '<tr>';
                headers.forEach(header => {
                    headerHtml += `<th>${header.replace(/_/g, ' ').toUpperCase()}</th>`;
                });
                headerHtml += '</tr>';
                thead.innerHTML = headerHtml;

                // Preenche o corpo da tabela com os dados
                data.forEach(response => {
                    let rowHtml = '<tr>';
                    headers.forEach(header => {
                        // Usa (response[header] || '-') para mostrar um traço se o campo estiver vazio
                        rowHtml += `<td>${response[header] || '-'}</td>`;
                    });
                    rowHtml += '</tr>';
                    tbody.innerHTML += rowHtml;
                });

                table.classList.remove('d-none'); // Mostra a tabela
            }

            // Inicia o processo ao carregar a página
            document.addEventListener('DOMContentLoaded', authenticateAndFetch);
        </script>
    </body>
    </html>
    """
    return Response(html_content, mimetype='text/html')

@app.route('/submit', methods=['POST'])
def submit():
    """Recebe os dados do formulário (em JSON) e salva no arquivo."""
    new_entry = request.get_json()
    if not new_entry:
        return jsonify({"status": "error", "message": "Nenhum dado recebido"}), 400
    
    all_data = read_data()
    all_data.append(new_entry)
    write_data(all_data)
    
    return jsonify({"status": "success"}), 200

@app.route('/data')
def get_data():
    """Fornece todos os dados salvos em formato JSON."""
    data = read_data()
    return jsonify(data)

# --- Execução da Aplicação ---

if __name__ == '__main__':
    # Esta configuração é importante para o Render.com
    # Ele usa a variável de ambiente PORT para saber em qual porta rodar.
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
