from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from .models import ScrapedImage
import os
from django.core.files.base import ContentFile

# https://biobags.com/ use

def scrape_images_dow(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        if not url:
            return render(request, 'scrape_down.html', {'error': 'Please enter a URL.'})

        try:
            response = requests.get(url)
            if response.status_code != 200:
                return render(request, 'scrape_down.html', {'error': f'Failed to retrieve content. Status code: {response.status_code}'})

            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')

            saved_images = []
            for img_tag in soup.find_all('img'):
                if 'src' in img_tag.attrs:
                    img_url = img_tag['src']
                    if not img_url.startswith(('http:', 'https:')):
                        img_url = urljoin(url, img_url)

                    # Download the image content
                    img_response = requests.get(img_url)

                    # Check if the request was successful
                    if img_response.status_code == 200:
                        # Save the image to the database
                        content_type = img_response.headers.get('Content-Type', '')
                        if content_type.startswith('image/'):
                            image_obj = ScrapedImage()
                            image_obj.image.save(os.path.basename(img_url), ContentFile(img_response.content))
                            print(image_obj)
                            saved_images.append(image_obj)

            return render(request, 'scrape_down.html', {'images': saved_images})
        except Exception as e:
            return render(request, 'scrape_down.html', {'error': f'An error occurred: {str(e)}'})

    return render(request, 'scrape_down.html')