from config import connection_string
from sqlalchemy import create_engine
from src.extract import extract_data
from src.transform import transform_data
from src.load import load_data 




def main():

    engine = create_engine(connection_string)


    pdf_files = extract_data()

    df = transform_data(pdf_files)
    load_data(engine,df)
    print('etl done')
    



if __name__ == "__main__":
    main()
