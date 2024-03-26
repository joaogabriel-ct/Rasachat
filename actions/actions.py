from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import aiohttp
import requests

class ActionBuscarPregoes(Action):
    def name(self) -> Text:
        return "action_buscar_licitacoes"

    async def run(self, dispatcher, tracker, domain):
        estado = tracker.latest_message['text'].split()[-1].upper()
        url = 'http://157.230.94.133:7209/api/licitacoes'
        response = requests.get(url=url)
        data = response.json()
        resposta_licitacoes = []
        for i in data:
            resposta_licitacoes.append(f"""
        informações sobre o edital {i['edital']}
        id: {i['id']}
        codigo: {i['codigo']}
        situação: {i['situacao']}
        """)
        
        if response:
            dispatcher.utter_message(text="\n".join(resposta_licitacoes))  # Convertendo a lista em uma única string
        else:
            dispatcher.utter_message(text='Deu erro ao buscar dados na API')
        
        return []

class ActionBuscarPregoesPorEstado(Action):
    def name(self) -> Text:
        return "action_buscar_licitacoes_estado"

    async def run(self, dispatcher, tracker, domain):
        estado = tracker.latest_message['text'].split()[-1].lower()
        url = f'http://157.230.94.133:7209/api/licitacoes?uf={estado}'
        response = requests.get(url=url)
        data = response.json()
        resposta_licitacoes = []
        for i in data:
            resposta_licitacoes.append(f"""
            informações sobre o edital {i['edital']}
            estado: {i['orgao_uf']}
            id: {i['id']}
            codigo: {i['codigo']}
            situação: {i['situacao']}
            """)
        
        if response:
            dispatcher.utter_message(text="\n".join(resposta_licitacoes))  # Convertendo a lista em uma única string
        else:
            dispatcher.utter_message(text='Deu erro ao buscar dados na API')
        
        return []

class ActionBuscarPregoesPorOrgao(Action):
    def name(self) -> Text:
        return "action_buscar_orgao"

    async def run(self, dispatcher, tracker, domain):
        orgao = tracker.latest_message['text'].split()[-1].lower()
        url = f'http://157.230.94.133:7209/api/licitacoes?orgao_nome={orgao}'
        response = requests.get(url=url)
        data = response.json()
        resposta_licitacoes = []

        if response.status_code == 200:
            for licitacao in data:
                resposta_licitacoes.append(f"""
                    Informações sobre o edital: {licitacao['edital']}
                    Estado: {licitacao['orgao_uf']}
                    ID: {licitacao['id']}
                    Código: {licitacao['codigo']}
                    Situação: {licitacao['situacao']}
                    Modalidade: {licitacao['modalidade']}
                    Objeto: {licitacao['objeto']}
                    Data do Certame: {licitacao['data_certame']}
                    Valor Estimado: R${licitacao['valor_estimado']}
                    Valor Homologado: R${licitacao['valor_homologado']}
                    Orgão: {licitacao['orgao_nome']}
                    Cidade: {licitacao['orgao_cidade']}
                    Observação: {licitacao['observacao']}
                """)

            dispatcher.utter_message(text="\n".join(resposta_licitacoes))
        else:
            dispatcher.utter_message(text='Desculpe, não foi possível acessar os dados no momento. Tente novamente mais tarde.')

        return []


class ActionBuscarPregoesDetalhado(Action):
    def name(self) -> Text:
        return "action_detalhes_pregao"

    async def run(self, dispatcher, tracker, domain):
        codigo = tracker.latest_message['text'].split()[-1].lower()
        url = f'http://157.230.94.133:7209/api/licitacoes/{codigo}/itens'
        print(url)
        response = requests.get(url=url)
        data = response.json()
        resposta_licitacoes = []
        for i in data:
            resposta_licitacoes.append(f"""
            Numero: {i["numero"]},\n
            Descrição: {i['descricao']},\n
            Tipo: {i["tipo"]},\n
            Valor estimado: {i["valor_uitario_estimado"]},\n
            Valor Total: {i["valor_total"]},\n
            Quantidade: {i["quantidade"]},\n
            Unidade de medida: {i["unidade_medida"]},\n
            Orçamento sigiloso: {i["orcamento_sigiloso"]},\n
            Categoria: {i["categoria"]},\n
            Criterio Julgamento: {i["criterio_julgamento"]},\n
            Situação de Compra: {i["situacao_compra"]},\n
            Tipo de Beneficio: {i["tipo_beneficio"]},\n
            Incentivo produtivo basico: {i["incentivo_produtivo_basico"]}
            """)
        
        if response:
            dispatcher.utter_message(text="\n".join(resposta_licitacoes))  # Convertendo a lista em uma única string
        else:
            dispatcher.utter_message(text='Deu erro ao buscar dados na API')
        
        return []

class ActionBuscarPregoesPorModalidadeEEstado(Action):
    def name(self) -> Text:
        return "action_buscar_pregoes_por_modalidade_e_estado"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Extrair entidades de modalidade e estado da mensagem do usuário
        modalidade = next(tracker.get_latest_entity_values("modalidade"), None)
        estado = next(tracker.get_latest_entity_values("estado"), None)

        if modalidade and estado:
            # Construir a URL da API com os critérios de pesquisa
            url = f'http://157.230.94.133:7209/api/licitacoes?modalidade={modalidade}&uf={estado}'
            # Substitua "sua_api.com" pela URL real da sua API de licitações

            # Fazer a requisição à API
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()

                if data:
                    # Formatar e enviar a mensagem de resposta com os resultados da pesquisa
                    resposta_licitacoes = [f"""
                        Informações sobre o pregão:\n
                        - Modalidade: {licitacao['modalidade']}\n
                        - Estado: {licitacao['orgao_uf']}\n
                        - Objeto: {licitacao['objeto']}\n
                        - Edital: {licitacao['edital']}\n
                        - Situação: {licitacao['situacao']}
                        """ for licitacao in data]
                    dispatcher.utter_message(text="\n".join(resposta_licitacoes))
                else:
                    dispatcher.utter_message(text="Nenhum pregão encontrado para os critérios informados.")
            else:
                dispatcher.utter_message(text="Erro ao consultar a API de licitações.")
        else:
            dispatcher.utter_message(text="Por favor, forneça tanto a modalidade quanto o estado para a pesquisa.")

        return []


class ActionBuscarPregoesPorFiltros(Action):
    def name(self) -> Text:
        return "action_buscar_pregoes_por_filtros"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Extrair entidades dos filtros da mensagem do usuário
        modalidade = next(tracker.get_latest_entity_values("modalidade"), None)
        estado = next(tracker.get_latest_entity_values("estado"), None)
        cidade = next(tracker.get_latest_entity_values("cidade"), None)
        objeto = next(tracker.get_latest_entity_values("objeto"), None)

        # Construir a URL da API com os filtros de pesquisa
        url = 'http://sua_api.com/api/licitacoes?'
        if modalidade:
            url += f'modalidade={modalidade}&'
        if estado:
            url += f'uf={estado}&'
        if cidade:
            url += f'cidade={cidade}&'
        if objeto:
            url += f'objeto={objeto}&'

        # Remover o último caractere '&' da URL, se estiver presente
        if url[-1] == '&':
            url = url[:-1]

        # Fazer a requisição à API
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            if data:
                # Formatar e enviar a mensagem de resposta com os resultados da pesquisa
                resposta_licitacoes = [f"""
                    Informações sobre o pregão:
                    - Modalidade: {licitacao['modalidade']}
                    - Estado: {licitacao['orgao_uf']}
                    - Objeto: {licitacao['objeto']}
                    - Edital: {licitacao['edital']}
                    - Situação: {licitacao['situacao']}
                    """ for licitacao in data]
                dispatcher.utter_message(text="\n".join(resposta_licitacoes))
            else:
                dispatcher.utter_message(text="Nenhum pregão encontrado para os critérios informados.")
        else:
            dispatcher.utter_message(text="Erro ao consultar a API de licitações.")

        return []