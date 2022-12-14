# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    #Set up executable path
    executable_path={'executable_path': ChromeDriverManager().install()}
    browser=Browser('chrome', **executable_path, headless=False)
    news_title, news_paragraph=mars_news(browser)

    #Run all scraping functions and store results in dictonary
    data={
        'news_title':news_title,
        'news_paragraph': news_paragraph,
        'featured_image': featured_image(browser),
        'facts': mars_facts(),
        'last_modified':dt.datetime.now()
    }
    #stop webdriver and return data
    browser.quit()
    return data

#Create a function
def mars_news(browser):

    #visit the mars nasa news site
    url="https://data-class-mars.s3.amazonaws.com/Mars/index.html"
    browser.visit(url)
    #Optional Delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)


    #Set up html parser
    html=browser.html
    news_soup=soup(html, 'html.parser')

    #Add try/except for error handling
    try:
        slide_elem=news_soup.select_one('div.list_text')


        #Scrape the data for latest article
        #slide_elem.find('div', class_='content_title')


        #Use the parent element to find the first 'a' tag and save it as a 'news_title'
        news_title=slide_elem.find('div', class_='content_title').get_text()
        #news_title


        #Use parent element to find the paragraph text
        news_p=slide_elem.find('div', class_='article_teaser_body').get_text()
        #news_p

    except AttributeError:
        return None, None


    return news_title, news_p

# ### Featured Images

def featured_image(browser):

    # Visit URL
    url="https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(url)


    #Find and click the full image button
    full_image_elem=browser.find_by_tag('button')[1]
    full_image_elem.click()


    # Parse the resulting html with soup
    html=browser.html
    img_soup=soup(html, 'html.parser')

    #Add the try/except for error handling
    try:

        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        #img_url_rel
    
    except AttributeError:
        return None


    # Use the base URL to create an absolute URL
    img_url=f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url

def mars_facts():
    try:

        # Set up to scrape table using pandas
        df=pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
        #df.columns=['description', 'Mars', 'Earth']
        #df.set_index('description', inplace=True)
        #df
    except BaseException:
        return None

    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Add the df to a web application
    return df.to_html(classes="table table-striped")


# end auotmated browsing session
#browser.quit()
#return data

if __name__ == '__main__':
    #if running as script, print scraped data
    print(scrape_all())






