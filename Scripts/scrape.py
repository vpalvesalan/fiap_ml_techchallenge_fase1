import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from typing import Literal, Optional

def scrape_vitibrasil_data(
    aba: Literal["Produção", "Processamento", "Comercialização", "Importação", "Exportação"],
    ano: int,
    sub_aba: Optional[Literal["Viníferas", "Americanas e híbridas","Uvas de mesa", "Sem classificação", "Vinhos de mesa", "Espumantes", "Uvas frescas", "Uvas passas","Suco de uva"]] = None,
):
    """Scrapes data from the Vitibrasil website and returns an HTML table.

    Parameters:
        aba: A string representing the tab to scrape:
                [Produção, Processamento, Comercialização, Importação, Exportação]
        sub_aba: A string representing the sub tab from page if it exists. I.e:
                for aba 'Processamento': ['Viníferas', 'Americanas e híbridas','Uvas de mesa', 'Sem classificação']
                for aba 'Importação': ['Vinhos de mesa', 'Espumantes', 'Uvas frescas', 'Uvas passas','Suco de uva']
                for aba 'Exportação': ['Vinhos de mesa', 'Espumantes', 'Uvas frescas','Suco de uva']
        ano: An integer repsenting the year from which get the data

    Returns:
        table_html: A bs4.element.Tag type contaning the HTML table
    """

    try:
        # Constrói o url da página a ser raspada
        aba = aba.capitalize().strip()
        sub_aba = sub_aba.capitalize().strip() if sub_aba is not None else sub_aba

        opcs = ['Produção', 'Processamento', 'Comercialização', 'Importação', 'Exportação']

        sub_opcs_process = ['Viníferas', 'Americanas e híbridas','Uvas de mesa', 'Sem classificação']
        sub_opcs_import = ['Vinhos de mesa', 'Espumantes', 'Uvas frescas', 'Uvas passas','Suco de uva']
        sub_opcs_export = ['Vinhos de mesa', 'Espumantes', 'Uvas frescas','Suco de uva']
        
        try:
            opt = opcs.index(aba) + 2
            opt_string = 'opt_0'+str(opt)
        except:
            print(f"A aba `{aba}` não faz parte das opções disponíveis de raspagem.\nPor favor, selecionar uma das opções seguintes: {', '.join(opcs)}.")
            return None


        if opt in [2,4]:
            url = f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao={opt_string}'
        
        else:
            try:
                if opt == 3:
                    sub_opt = sub_opcs_process.index(sub_aba) + 1
                elif opt == 5:
                    sub_opt = sub_opcs_import.index(sub_aba) + 1
                elif opt == 6:
                    sub_opt = sub_opcs_export.index(sub_aba) + 1
                
                sub_opt_string = 'subopt_0'+str(sub_opt)
                url = f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao={opt_string}&subopcao={sub_opt_string}'
            except:
                sub_abas_disponivel = ', '.join(sub_opcs_process) if opt == 3 else ', '.join(sub_opcs_import) if opt == 5 else ', '.join(sub_opcs_export)
                
                if sub_aba is None:
                    print(f"A aba {aba} exige que seja seleciona uma das opções seguintes como subaba: {sub_abas_disponivel}.")
                    return None
                else:
                    print(f"A opção `{sub_aba}` não faz parte das opções disponíveis de raspagem para a aba `{aba}`. Por favor, selecionar uma das opções seguintes: {sub_abas_disponivel}")
                    return None

        # Raspa a página
        # Define agentes de usuário para simular requisições de diferentes navegadores
        ua = UserAgent()
        headers = {'User-Agent': ua.random}

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
        else:
            print('Servidor indisponível')
            return {'aba':aba, 'ano':ano, 'status_code':response.status_code} 

        # Verifica se foi encontrada a tabela de dados
        table_html = soup.find('table',{'class':'tb_base tb_dados'})

        if table_html:
            print('Raspagem com a tabela de dados extraída com sucesso!')
            return table_html
        else: 
            print('Foi procurado pela class "tb_base tb_dados", na tag Table, mas nada foi encontrado. Foi retornado dicionário com dados da raspagem')
            return {'soup':soup, 'url':url, 'headers':headers}
    
    except requests.exceptions.ConnectionError as err:
        print(f'Não foi possível acessar o site. Erro de conexão: {err}')
        return None
    
    except Exception as err:
        print(f'Um erro foi encontrado: {err}')
        return None