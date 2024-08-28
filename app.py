import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import csv
import time
async def scrape_properties_from_realtor():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Set headless=True if you do not need to see the browser
        page = await browser.new_page()

        # Go to the Bing News search page
        await page.goto('https://www.realtor.com/realestateandhomes-search/USAF-Academy_CO', timeout=600000)

        data = []
        base_url = "https://www.realtor.com"
        

        up = True
        while up:
            await page.wait_for_timeout(5000)  # Here is a timeout  for the new content to load
            
            # Extract content
            content = await page.content()
            soup = BeautifulSoup(content, 'lxml')
            # properties = soup.find_all('div', class_='BasePropertyCard_propertyCard__N5tuo')


           
    
            # for item in properties:
            #     Propertie_Url= item.find('a', class_='LinkComponent_anchor__TetCm')
            #     if Propertie_Url:
            #         Propertie_Url = base_url +  Propertie_Url.get("href")
            #         print(Propertie_Url)
            #         Propertie_Title = base_url + item.find('a', class_='ipc-metadata-list-summary-item__t').get("href")
                    
            #         Movie_Cover = item.find('img')
            #     else:
            #         continue
            
            # Scrape property details
            properties = soup.find_all('div', class_='BasePropertyCard_propertyCard__N5tuo')
            for property in properties:
                property_url= property.find('a', class_='LinkComponent_anchor__TetCm')
                if property_url:
                    image_url = property.find('img').get('data-src')
                    broker_title = property.find('div', {'data-testid': 'broker-title'}).text
                    property_url = base_url + property.find('a', class_='LinkComponent_anchor__TetCm')['href']
                    property_price = property.find('div', {'data-testid': 'card-price'}).text
                    property_status = property.find('div', class_='base__StyledType-sc-fdbaf2d6-0 jibrmh message')
                    property_status = property_status.text if property_status else ''
                    property_beds = property.find('li', {'data-testid': 'property-meta-beds'})
                    property_beds = property_beds.text if property_beds else ''
                    property_baths = property.find('li', {'data-testid': 'property-meta-baths'})
                    property_baths = property_baths.text if property_baths else ''
                    property_sqft = property.find('li', {'data-testid': 'property-meta-sqft'})
                    property_sqft = property_sqft.text if property_sqft else ''
                    property_lot_size = property.find('li', {'data-testid': 'property-meta-lot-size'})
                    property_lot_size = property_lot_size.text if property_lot_size else ''
                    address_street = property.find('div', {'data-testid': 'card-address-1'})
                    address_street = address_street.text if address_street else ''
                    address_city_state_zip = property.find('div', {'data-testid': 'card-address-2'})
                    address_city_state_zip = address_city_state_zip.text if address_city_state_zip else ''
                    
                    # Print or store the scraped data
                    print(f"Image URL: {image_url}")
                    print(f"Broker: {broker_title}")
                    print(f"Property URL: {property_url}")
                    print(f"Price: {property_price}")
                    print(f"Status: {property_status}")
                    print(f"Beds: {property_beds}")
                    print(f"Baths: {property_baths}")
                    print(f"Square Footage: {property_sqft}")
                    print(f"Lot Size: {property_lot_size}")
                    print(f"Address: {address_street}, {address_city_state_zip}")
                    print()
                        
                
                
            
                    data.append({
                        'Broker': broker_title,
                        'Property URL': property_url,
                        'Price': property_price,
                        'Status': property_status,
                        'Beds': property_beds,
                        "Baths": property_baths,
                        "Square Footage" : property_sqft,
                        "Lot Size" : property_lot_size,
                        "Address Street": address_street,
                        "Address City State Zip" : address_city_state_zip,
                        "Image Url" : image_url,                        
                    })
                
            # Now we can update up value in order to stop the while loop
            up = False

        # Save data to CSV
        
        if len(data) > 0:
            with open('properties_from_realtor.csv', 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Broker',"Property URL","Price","Status","Beds", "Baths","Square Footage", "Lot Size", "Address Street", "Address City State Zip", "Image Url"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for row in data:
                    writer.writerow(row)

            print(f'Scraped {len(data)} properties. Data saved to movies_from_imdb.csv.')
            
        else:
            print(f'Scraped {len(data)} properties.')

        # Close the browser
        await browser.close()

# Run the scrape function
asyncio.run(scrape_properties_from_realtor())





