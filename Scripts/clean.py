import pandas as pd


def extract_table_from_html(html_table: 'bs4.element.Tag') -> pd.DataFrame:
    """Extracts a table from a BeautifulSoup Tag object.

    Parameters:
        html_table (bs4.element.Tag): The BeautifulSoup Tag, returned by `scrape.scrape_vitibrasil_data` containing the table.

    Returns:
        pd.DataFrame: A pandas DataFrame representing the extracted table.
                      Returns an empty DataFrame if the input is None or not a table.
    """

    data = []
    item_str, subitem_str, subitem_int =  '','',0

    try:
        rows = html_table.find_all('tr') # Table rows
        table_header_tag = html_table.find_all('th')
        col_names = [h.text.strip() for h in table_header_tag if h.get_text().strip() != '']
        n_col = len(col_names)
        
        # Extrai valores das colunas presente em cada linha    
        if n_col == 2:

            col_names = ['Categoria'] + col_names
            for row in rows:
                
                col_item = row.find('td', {'class':'tb_item'})
                col_subitem = row.find_all('td', {'class':'tb_subitem'})
                
                if col_item:
                    item_str = col_item.get_text().strip()

                if col_subitem:
                    subitem_str = col_subitem[0].get_text().strip()
                    subitem_int =  col_subitem[1].get_text().strip()

                row_data = [item_str, subitem_str, subitem_int]
                data.append(row_data)

        else:
            for row in rows:
                columns = row.find_all('td')
                row_data = [col.get_text().strip() for col in columns]
                data.append(row_data)


        df = pd.DataFrame(data)

        # Clean the data
        # Filter out empty rows
        df = df.fillna('')
        keep_rows = ~((df.iloc[:,1] == '') | (df.iloc[:,0] == ''))
        df = df[keep_rows]

        df.columns = col_names

        # Convert numeric coluns to numeric
        num_columns = [('Quantidade' in col_name) or ('Valor' in col_name) for col_name in col_names]
        num_columns_index = [i for i, val in enumerate(num_columns) if val]
       
        if num_columns_index:
            for i in num_columns_index:
                if pd.api.types.is_string_dtype(df[col_names[i]]):
                    df[col_names[i]] = df[col_names[i]].str.replace('.', '', regex=False)
                    df[col_names[i]] = df[col_names[i]].str.replace('-', '0', regex=False)
                    df[col_names[i]] = pd.to_numeric(df[col_names[i]], errors='coerce')
            
        return(df)
    
    except Exception as err:
        print(f'Um erro ocorreu: {err}')
        return None