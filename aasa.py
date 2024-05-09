import pandas as pd
import re

def validate_cpf(cpf: str) -> bool:
    """Validate a CPF number."""
    cpf = str(cpf)
    if len(cpf)!= 11 or not cpf.isdigit():
        return False

    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito_1 = (soma % 11)
    digito_1 = 0 if digito_1 < 2 else 11 - digito_1

    if digito_1!= int(cpf[9]):
        return False

    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito_2 = (soma % 11)
    digito_2 = 0 if digito_2 < 2 else 11 - digito_2

    return digito_2 == int(cpf[10])


def extract_number_from_address(address: str) -> tuple:
    """Extract the number from an address."""
    if pd.isna(address) or address == '':
        return None, None

    match = re.search(r'\s+(\d+)$', str(address))
    if match:
        number = match.group(1)
        updated_address = re.sub(r'\s+\d+$', '', str(address)).strip()
        return updated_address, number
    else:
        return address, None


def load_data(file_path: str) -> pd.DataFrame:
    """Load data from an Excel file."""
    try:
        return pd.read_excel(file_path, na_values=['', 'NA', 'nan'])
    except FileNotFoundError as e:
        raise ValueError(f"Error: File not found at {file_path}") from e


def validate_cpf_in_df(df: pd.DataFrame) -> pd.DataFrame:
    """Validate CPF in a DataFrame."""
    df['cpf_valido'] = df['CPF'].apply(validate_cpf)
    return df


def extract_numbers_from_addresses_in_df(df: pd.DataFrame) -> pd.DataFrame:
    """Extract numbers from addresses in a DataFrame."""
    df[['Endereco', 'numero']] = df['Endereco'].apply(extract_number_from_address).apply(pd.Series)
    return df


def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """Process data by validating CPF and extracting numbers from addresses."""
    df = validate_cpf_in_df(df)
    df = extract_numbers_from_addresses_in_df(df)
    return df


def save_data(df: pd.DataFrame, file_path: str) -> None:
    """Save data to an Excel file."""
    try:
        df.to_excel(file_path, index=False, engine='openpyxl')
        print(f"Planilha filtrada salva em {file_path}.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    file_path = 'ENEL ARQ 06.xlsx'
    df = load_data(file_path)
    if df is not None:
        df = process_data(df)
        df_filtrado = df[(df['cpf_valido']) & (df['numero'].notnull())]
        save_data(df_filtrado, 'ENEL ARQ 06_filtrado.xlsx')