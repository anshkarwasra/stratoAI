import requests
from bs4 import BeautifulSoup
import logging
from typing import List, Dict
import csv

class PCGameBenchmarkScraper:
    def __init__(self, base_url: str, state: str, code: str):
        """
        Initialize the scraper with base configuration
        
        Args:
            base_url (str): Base URL for scraping
            state (str): Website state parameter
            code (str): Website code parameter
        """
        self.base_url = base_url
        self.state = state
        self.code = code
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def fetch_page(self, url: str) -> BeautifulSoup:
        """
        Fetch and parse a webpage
        
        Args:
            url (str): URL to fetch
        
        Returns:
            BeautifulSoup: Parsed HTML content
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            self.logger.error(f"Error fetching {url}: {e}")
            return None

    def scrape_gpu_list(self, num_pages: int) -> List[str]:
        """
        Scrape list of GPUs from paginated results
        
        Args:
            num_pages (int): Number of pages to scrape
        
        Returns:
            List[str]: List of GPU names
        """
        gpus = []
        for page in range(1, num_pages + 1):
            url = f"{self.base_url}/page-{page}?callback=in&code={self.code}&state={self.state}"
            self.logger.info(f"Fetching: {url}")
            
            soup = self.fetch_page(url)
            if not soup:
                continue

            table = soup.find('table', {'id': 'component-table'})
            if not table:
                self.logger.warning(f"No data found on page {page}")
                continue

            gpu_rows = table.find_all('tr')[1:]
            gpus.extend([row.find_all('td')[0].text.strip() for row in gpu_rows if len(row.find_all('td')) > 2])
        gpus = list(map(lambda x:x.replace(" ","-"),gpus))
        return gpus

    def scrape_gpu_benchmarks(self, gpu: str) -> List[Dict]:
        """
        Scrape game benchmarks for a specific GPU
        
        Args:
            gpu (str): GPU name
        
        Returns:
            List[Dict]: Benchmark data for games
        """
        benchmarks = []
        gpu_url = f"https://www.pcgamebenchmark.com/gpu/{gpu}"
        soup = self.fetch_page(gpu_url)
        
        if not soup:
            return benchmarks
        gpu_header = soup.find('h1', class_='gpu-name')
        gpu_name = gpu_header.text.strip() if gpu_header else gpu
        print('gpu name is :',gpu_name)
        pagination = soup.find('div', {'class': 'pages'})
        page_count = len(pagination.find_all('a')) if pagination else 1

        for page in range(1, page_count + 1):
            page_url = f"{gpu_url}?page={page}"
            page_soup = self.fetch_page(page_url)
            
            if not page_soup:
                continue

            table = page_soup.find('table', {'class': 'benchmarking-table'})
            if not table:
                self.logger.warning(f"No benchmark data found for {gpu} on page {page}")
                continue

            for row in table.find_all('tr')[1:]:
                cols = row.find_all('td')
                if len(cols) > 5:
                    avg_fps_elem = cols[4].find('td')
                    avg_fps = int(avg_fps_elem.text[:round(len(avg_fps_elem.text)/2)]) if avg_fps_elem else None
                    
                    # Extract highest FPS
                    highest_fps_elem = cols[4].find_all('td')[1] if len(cols[4].find_all('td')) > 1 else None
                    highest_fps = int(highest_fps_elem.text.strip()) if highest_fps_elem else None
                    benchmarks.append({
                        'game': cols[0].text.strip(),
                        'cpu': cols[1].text.strip(),
                        'gpu': gpu_name,
                        'ram': cols[3].text.strip(),
                        'avrage_fps': avg_fps,
                        'highest_fps': highest_fps,
                    })
        
        return benchmarks

    def scrape_all_benchmarks(self, num_pages: int) -> List[Dict]:
        """
        Scrape benchmarks for all GPUs
        
        Args:
            num_pages (int): Number of pages to scrape for GPU list
        
        Returns:
            List[Dict]: Comprehensive benchmark data
        """
        all_benchmarks = []
        gpus = self.scrape_gpu_list(num_pages)
        
        for gpu in gpus:
            self.logger.info(f"Fetching benchmarks for {gpu}")
            gpu_benchmarks = self.scrape_gpu_benchmarks(gpu)
            all_benchmarks.extend(gpu_benchmarks)
        
        return all_benchmarks
    def export_to_csv(self, data: List[Dict], filename: str = 'gpu_benchmarks.csv'):
        """
        Export scraped benchmark data to a CSV file
        
        Args:
            data (List[Dict]): Benchmark data to export
            filename (str): Output CSV filename
        """
        if not data:
            self.logger.warning("No data to export")
            return

        try:
            # Use the first dictionary's keys as CSV headers
            fieldnames = data[0].keys()
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                # Write header
                writer.writeheader()
                
                # Write data rows
                writer.writerows(data)
            
            self.logger.info(f"Data exported to {filename}")
        except Exception as e:
            self.logger.error(f"Error exporting to CSV: {e}")

def main():
    BASE_URL = "https://pcgamebenchmark.com/graphics-cards"
    STATE = "7fcd6f35c176411e9da6041595a053d6"
    CODE = "ZJG2ZMVLYZKTOGY1NY0ZZDY4LWIYM2ETYJBLNTLIODU2Y2U3"
    
    scraper = PCGameBenchmarkScraper(BASE_URL, STATE, CODE)
    data = scraper.scrape_all_benchmarks(num_pages=1)
    
    # Export to CSV
    scraper.export_to_csv(data, 'gpu_game_benchmarks.csv')
    print(f"Total benchmarks scraped and exported: {data}")


def sampleFetch():
    benchmarks = []
    gpu_url = 'https://www.pcgamebenchmark.com/gpu/nvidia-geforce-rtx-3070'
    res = requests.get(gpu_url)
    soup = BeautifulSoup(res.text, 'html.parser')    
    if not soup:
        return benchmarks
    
    pagination = soup.find('div', {'class': 'pages'})
    page_count = len(pagination.find_all('a')) if pagination else 1
    
    for page in range(1, page_count + 1):
        print(f'on page {page}')
        page_url = f"{gpu_url}?page={page}"
        page_res = requests.get(page_url)
        page_soup = BeautifulSoup(page_res.text, 'html.parser')    
        
        if not page_soup:
            continue
        
        table = page_soup.find('table', {'class': 'benchmarking-table'})
        if not table:
            print(f"No benchmark data found for nvidia-geforce-rtx-3070 on page {page}")
            continue
        
        for row in table.find_all('tr')[1:]:
            cols = row.find_all('td')
            if len(cols) > 5:
                try:
                    # Extract average FPS from the title attribute
                    avg_fps_elem = cols[4].find('td')
                    avg_fps = int(avg_fps_elem.text[:round(len(avg_fps_elem.text)/2)]) if avg_fps_elem else None
                    
                    # Extract highest FPS
                    highest_fps_elem = cols[4].find_all('td')[1] if len(cols[4].find_all('td')) > 1 else None
                    highest_fps = int(highest_fps_elem.text.strip()) if highest_fps_elem else None
                    
                    benchmarks.append({
                        'game': cols[0].text.strip(),
                        'cpu': cols[1].text.strip(),
                        'gpu': cols[2].text.strip(),
                        'ram': cols[3].text.strip(),
                        'average_fps': avg_fps,
                        'highest_fps': highest_fps,
                    })
                except (ValueError, IndexError) as e:
                    print(f"Error processing row: {e}")
    
    return benchmarks

if __name__ == "__main__":
    main()
    # data = sampleFetch()
    # print(data)