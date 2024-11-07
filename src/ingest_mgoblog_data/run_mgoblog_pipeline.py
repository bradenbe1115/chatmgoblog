from ingest_mgoblog_data.service_layer.services import scrape_mgoblog_data, process_mgoblog_data

def main():
    landed_urls = scrape_mgoblog_data(iterations=2)

    process_mgoblog_data(landed_urls)

if __name__ == "__main__":
    main()