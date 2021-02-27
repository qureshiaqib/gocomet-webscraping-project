from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import xlsxwriter
#-----------------Driver initializations------------------------------------#
amazon_driver=webdriver.Chrome(ChromeDriverManager().install())
flipkart_driver=webdriver.Chrome(ChromeDriverManager().install())

#------------------get url---------------------#
amazon_url="https://www.amazon.in"
amazon_driver.get(amazon_url)

flipkart_url="https://www.flipkart.com/"
flipkart_driver.get(flipkart_url)

#------------search using keywords-------------#
def search_amazon(keyword):
    url="https://www.amazon.in/s?k="+keyword+"&ref=nb_sb_noss_2"
    return url
def search_flipkart(keyword):
    url="https://www.flipkart.com/search?q="+keyword+"&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    return url

#------------search Amazon-------------#
def amazon_search_results(item):
    #product_name
    name=item.h2.text.strip()
    source="amazon"
    #url
    url=amazon_url+item.h2.a['href']
    
    #rating and review
    try:
        rating=item.find('span',class_="a-icon-alt").text
    except AttributeError:
        rating='Not Rated'
        
        
        
        
    #price
    try:
        price_details=item.find('span',class_='a-price')
        price=price_details.find('span',class_='a-offscreen').text
        
    except AttributeError:
         price='₹0000'
            
    try:
        delivery_date=item.find('span',{'class':"a-text-bold", "dir":"auto"}).text
        
    except AttributeError:
         delivery_date='depends'
    
    details=[name,url,source,price,rating,delivery_date]  
    
    return details


#------------search flipkart-------------#

def flipkart_search_results(item):
    
    parent=item.find('a')
    
    # name
    name=parent.find("div",class_="_4rR01T").text
    
    
    
    
    #url
    url=flipkart_url+parent['href']
    
     #rating and review
    review="-"
    try:
        rating=parent.find('div',class_='_3LWZlK').text
        
    except AttributeError:
        rating='Not Rated'
        
        
        
#     #price
    try:
        price=item.find('div',class_='_30jeq3 _1_WHN1').text
        
    except AttributeError:
        price='₹0000'
            
    delivery_date='On working days'
    
    source="flipkart"
    
    details=[name,url,source,price,rating,delivery_date]
    
    return details

#------ Web scraping begins-------#

temp=[["name",'url','source','price','rating','delivery']]

def for_amazon(keyword):
    
    search_url=search_amazon(keyword)

    amazon_driver.get(search_url)
    
    soup=BeautifulSoup(amazon_driver.page_source,'html.parser')

    results=soup.find_all('div',{"data-component-type":"s-search-result"})
    for item in results:
        details=amazon_search_results(item)
        if details:
            
            temp.append(details)
            
    
#---------------------------------------------------------------#         
            
def for_flipkart(keyword):
    
    search_url=search_flipkart(keyword)
    
    flipkart_driver.get(search_url)
    
    soup=BeautifulSoup(flipkart_driver.page_source,'html.parser')
    
    results=soup.find_all('div',class_="_13oc-S")
    
    for item in results:
        details=flipkart_search_results(item)
        if details:
            
            temp.append(details)

 #----------main--------------
def main():
    keyword=input("Enter Product: ")
    for_amazon(keyword)
    for_flipkart(keyword)
            
    
    workbook = xlsxwriter.Workbook('search.xlsx')



    worksheet = workbook.add_worksheet("My sheet") 

    row=0
    col=0

    for name, url,source,price,rating,delivery in (temp): 
        worksheet.write(row, col, name) 
        worksheet.write(row, col + 1,url) 
        worksheet.write(row, col + 2,source)
        worksheet.write(row, col + 3,price)
        worksheet.write(row, col + 4,rating)
        worksheet.write(row, col + 5,delivery) 
        row += 1



    workbook.close()   
    
#### calling main ######

main()
    
    




