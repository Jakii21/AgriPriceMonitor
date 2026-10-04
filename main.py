from extract.da_scraper import scrape_all
from transform.data_cleaner import cleanData, validateData
from load.items_loader import load_prices


def main():

    print("Initiating AgriPrice Monitor")

    #Extract
    finalDf = scrape_all()

    finalDf = cleanData(finalDf)

    print("\n Total Scrape records: ", len(finalDf))

    if validateData(finalDf):
        load_prices(finalDf)
    else:
        print("\nETL stopped because validation failed.")


    print("\n ~~ ETL process completed ~~")
    
#-------------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()


"""
main.py
   ↓
scrape_all()
   ↓
clean_data()
   ↓
validate_data()
   ↓
load_prices()
   ↓
insert_price_record()"""