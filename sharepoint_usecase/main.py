from sqlalchemy import create_engine
from config import connection_string
from src.extract import extract
from src.transform import transform
from src.load import load

def main():
    engine = create_engine(connection_string)

    raw_rows = extract()
    df = transform(raw_rows)
    load(engine, df)


if __name__ == "__main__":
    main()
